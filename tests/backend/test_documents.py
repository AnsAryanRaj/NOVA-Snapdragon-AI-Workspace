"""Comprehensive unit and integration test suite for Phase 4 Document Intelligence."""

import os
import fitz
import pytest
from pathlib import Path
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.db.database import Base, get_db
from app.core.config import settings
from app.core.path_security import get_workspace_root
from app.documents.extractor import (
    extract_text_from_file,
    ExtractedData,
    is_extension_supported,
    get_mime_type
)
from app.documents.chunker import chunk_extracted_data, _split_text_into_chunks
from app.documents.index import index_workspace_documents, generate_doc_id
from app.documents.service import search_documents, list_documents, get_document_stats, get_document_detail
from app.tools.registry import tool_registry

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

# Setup test DB
TEST_DB_URL = "sqlite:///:memory:"
test_engine = create_engine(
    TEST_DB_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)



def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_test_db():
    from app.db import models  # noqa: F401
    Base.metadata.create_all(bind=test_engine)
    app.dependency_overrides[get_db] = override_get_db
    yield
    Base.metadata.drop_all(bind=test_engine)
    app.dependency_overrides.pop(get_db, None)



@pytest.fixture
def workspace_dir():
    root = get_workspace_root()
    root.mkdir(parents=True, exist_ok=True)
    return root


def test_extractor_supported_extensions():
    assert is_extension_supported(".txt") is True
    assert is_extension_supported(".md") is True
    assert is_extension_supported(".py") is True
    assert is_extension_supported(".pdf") is True
    assert is_extension_supported(".exe") is False
    assert is_extension_supported(".dll") is False


def test_extractor_mime_types():
    assert get_mime_type(".pdf") == "application/pdf"
    assert get_mime_type(".json") == "application/json"
    assert get_mime_type(".md") == "text/markdown"
    assert get_mime_type(".py") == "text/x-code"


def test_extract_text_file(workspace_dir):
    test_file = workspace_dir / "test_extract.md"
    test_file.write_text("# Title\nThis is a test document for extraction.", encoding="utf-8")

    try:
        extracted = extract_text_from_file(test_file)
        assert extracted.status == "SUCCESS"
        assert extracted.page_count == 1
        assert "This is a test document" in extracted.full_text
    finally:
        if test_file.exists():
            test_file.unlink()


def test_extract_pdf_file(workspace_dir):
    pdf_path = workspace_dir / "sample.pdf"
    doc = fitz.open()
    page1 = doc.new_page()
    page1.insert_text((50, 50), "Hello Snapdragon NPU Page 1")
    page2 = doc.new_page()
    page2.insert_text((50, 50), "Hello Privacy Intelligence Page 2")
    doc.save(str(pdf_path))
    doc.close()

    try:
        extracted = extract_text_from_file(pdf_path)
        assert extracted.status == "SUCCESS"
        assert extracted.page_count == 2
        assert "Snapdragon NPU" in extracted.full_text
        assert "Privacy Intelligence" in extracted.full_text
    finally:
        if pdf_path.exists():
            pdf_path.unlink()


def test_chunker_splitting():
    extracted = ExtractedData(
        full_text="Line " * 400,  # ~2000 chars
        pages=[{"page_number": 1, "text": "Line " * 400}],
        page_count=1,
        status="SUCCESS"
    )

    chunks = chunk_extracted_data(extracted, target_chunk_size=500, chunk_overlap=100)
    assert len(chunks) >= 2
    assert chunks[0].chunk_index == 0
    assert chunks[0].page_number == 1
    assert chunks[0].token_count > 0


def test_indexing_workspace(workspace_dir):
    db = TestingSessionLocal()
    sub_dir = workspace_dir / "idx_test_dir"
    sub_dir.mkdir(exist_ok=True)

    try:
        # Create test documents inside sub_dir
        doc1 = sub_dir / "doc1.txt"
        doc1.write_text("NOVA AI workspace privacy assistant with local NPU processing.", encoding="utf-8")
        doc2 = sub_dir / "doc2.md"
        doc2.write_text("# Security\nPath traversal protection and audit logging.", encoding="utf-8")

        summary = index_workspace_documents(db, subpath="idx_test_dir", force_reindex=True)
        assert summary.indexed_new == 2
        assert summary.total_chunks >= 2

        stats = get_document_stats(db)
        assert stats.total_documents == 2
        assert stats.total_chunks >= 2

        # Verify search
        search_res = search_documents(db, query="privacy assistant")
        assert search_res.total_matches > 0
        assert "doc1.txt" in search_res.matches[0].relative_path

    finally:
        db.close()
        for f in sub_dir.glob("*"):
            f.unlink()
        sub_dir.rmdir()


def test_indexing_incremental_skip(workspace_dir):
    db = TestingSessionLocal()
    sub_dir = workspace_dir / "inc_test_dir"
    sub_dir.mkdir(exist_ok=True)

    try:
        doc = sub_dir / "inc_test.txt"
        doc.write_text("Incremental test content for document indexing.", encoding="utf-8")

        # First scan
        sum1 = index_workspace_documents(db, subpath="inc_test_dir", force_reindex=False)
        assert sum1.indexed_new == 1

        # Second scan without changes
        sum2 = index_workspace_documents(db, subpath="inc_test_dir", force_reindex=False)
        assert sum2.skipped_unchanged == 1
        assert sum2.indexed_new == 0

    finally:
        db.close()
        for f in sub_dir.glob("*"):
            f.unlink()
        sub_dir.rmdir()


def test_api_index_and_search_endpoints(workspace_dir):
    sub_dir = workspace_dir / "api_test_dir"
    sub_dir.mkdir(exist_ok=True)
    doc_file = sub_dir / "api_test.py"
    doc_file.write_text("def nova_workspace_agent():\n    return 'Snapdragon AI'\n", encoding="utf-8")

    try:
        # Trigger index API
        resp = client.post("/api/v1/documents/index", json={"subpath": "api_test_dir", "force_reindex": True})
        assert resp.status_code == 200, f"Error: {resp.text}"
        data = resp.json()
        assert data["total_found"] >= 1, f"Data: {data}"
        assert data["total_chunks"] >= 1, f"Data: {data}"



        # List API
        resp_list = client.get("/api/v1/documents/list?subpath=api_test_dir")
        assert resp_list.status_code == 200
        docs = resp_list.json()
        assert any(d["file_name"] == "api_test.py" for d in docs)

        # Search API
        resp_search = client.get("/api/v1/documents/search?q=Snapdragon")
        assert resp_search.status_code == 200
        search_data = resp_search.json()
        assert search_data["total_matches"] >= 1

        # Stats API
        resp_stats = client.get("/api/v1/documents/stats")
        assert resp_stats.status_code == 200
        stats_data = resp_stats.json()
        assert stats_data["total_documents"] >= 1

    finally:
        for f in sub_dir.glob("*"):
            f.unlink()
        sub_dir.rmdir()


def test_api_path_traversal_rejection():
    # Attempt indexing subpath outside workspace boundary
    resp = client.post("/api/v1/documents/index", json={"subpath": "../../secret_dir"})
    assert resp.status_code == 400
    assert "Security Violation" in resp.json()["detail"]


def test_tool_registry_document_tools():
    expected_tools = [
        "document.list",
        "document.get_metadata",
        "document.get_content",
        "document.search",
        "document.index",
        "document.get_stats"
    ]
    for tool_name in expected_tools:
        tool = tool_registry.get_tool(tool_name)
        assert tool is not None, f"Tool '{tool_name}' not registered"
        assert tool.category == "document"
        assert tool.is_destructive is False
        assert tool.requires_confirmation is False


def test_api_get_documents_root_and_content_endpoint(workspace_dir):
    sub_dir = workspace_dir / "api_root_test_dir"
    sub_dir.mkdir(exist_ok=True)
    doc_file = sub_dir / "sample_code.kt"
    doc_file.write_text("fun main() { println(\"Hello Snapdragon\") }", encoding="utf-8")

    try:
        # Index document
        resp_idx = client.post("/api/v1/documents/index", json={"subpath": "api_root_test_dir", "force_reindex": True})
        assert resp_idx.status_code == 200

        # Test GET /api/v1/documents root list endpoint
        resp_root = client.get("/api/v1/documents?subpath=api_root_test_dir")
        assert resp_root.status_code == 200
        docs = resp_root.json()
        assert len(docs) >= 1
        doc_id = docs[0]["id"]

        # Test GET /api/v1/documents/{doc_id}/content endpoint
        resp_content = client.get(f"/api/v1/documents/{doc_id}/content")
        assert resp_content.status_code == 200
        content_data = resp_content.json()
        assert content_data["doc_id"] == doc_id
        assert "Hello Snapdragon" in content_data["full_text"]
        assert len(content_data["chunks"]) >= 1

    finally:
        for f in sub_dir.glob("*"):
            f.unlink()
        sub_dir.rmdir()


def test_document_id_content_hash_sensitivity():
    rel_path = "docs/guide.md"
    hash1 = "a1b2c3d4e5f6"
    hash2 = "f6e5d4c3b2a1"

    id1 = generate_doc_id(rel_path, hash1)
    id2 = generate_doc_id(rel_path, hash2)
    id1_again = generate_doc_id(rel_path, hash1)

    assert id1 == id1_again, "Same path and same content must produce same document ID"
    assert id1 != id2, "Same path with changed content hash must produce distinct version-safe document ID"


def test_kotlin_and_java_extension_support(workspace_dir):
    assert is_extension_supported(".kt") is True
    assert is_extension_supported(".java") is True

    kt_file = workspace_dir / "TestCode.kt"
    kt_file.write_text("class TestCode { fun run() {} }", encoding="utf-8")
    try:
        extracted = extract_text_from_file(kt_file)
        assert extracted.status == "SUCCESS"
        assert "TestCode" in extracted.full_text
    finally:
        if kt_file.exists():
            kt_file.unlink()

