"""Automated Test Suite for Phase 3 Workspace Intelligence & Path Security."""

import os
from pathlib import Path
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.path_security import validate_workspace_path, get_workspace_root
from app.workspace.classifier import classify_file_extension, is_safe_text_file
from app.workspace.service import workspace_service
from app.tools.registry import tool_registry

client = TestClient(app)


# 1. Valid workspace path
def test_path_security_valid_root():
    candidate, rel_str = validate_workspace_path("")
    assert candidate.resolve() == get_workspace_root().resolve()
    assert rel_str == ""


# 2. Empty/root workspace path
def test_path_security_empty_path():
    candidate, rel_str = validate_workspace_path("   ")
    assert candidate.resolve() == get_workspace_root().resolve()
    assert rel_str == ""


# 3. Nested workspace path
def test_path_security_nested_path():
    candidate, rel_str = validate_workspace_path("Documents/sample_report.txt")
    assert rel_str == "Documents/sample_report.txt"
    assert candidate.name == "sample_report.txt"


# 4. ../ traversal rejection
def test_path_security_slash_traversal_rejection():
    response = client.get("/api/v1/workspace/files?path=../")
    assert response.status_code == 400
    assert "Security Violation" in response.json()["detail"]


# 5. ..\ traversal rejection
def test_path_security_backslash_traversal_rejection():
    response = client.get("/api/v1/workspace/files?path=..\\..\\")
    assert response.status_code == 400
    assert "Security Violation" in response.json()["detail"]


# 6. Absolute outside path rejection
def test_path_security_absolute_outside_rejection():
    response = client.get("/api/v1/workspace/files?path=C:/Windows/System32")
    assert response.status_code == 400
    assert "Security Violation" in response.json()["detail"]


# 7. Windows drive escape rejection
def test_path_security_drive_escape_rejection():
    response = client.get("/api/v1/workspace/files?path=E:/some_outside_folder")
    assert response.status_code == 400
    assert "Security Violation" in response.json()["detail"]


# 8. Outside workspace path rejection
def test_path_security_direct_outside_rejection():
    response = client.get("/api/v1/workspace/content?path=../../backend/app/main.py")
    assert response.status_code == 400
    assert "Security Violation" in response.json()["detail"]


# 9. File listing
def test_workspace_file_listing():
    response = client.get("/api/v1/workspace/files?path=Documents")
    assert response.status_code == 200
    data = response.json()
    assert data["path"] == "Documents"
    assert data["total_count"] >= 1
    assert any(item["name"] == "sample_report.txt" for item in data["items"])


# 10. Directory listing (root)
def test_workspace_root_directory_listing():
    response = client.get("/api/v1/workspace/files")
    assert response.status_code == 200
    data = response.json()
    assert data["total_count"] >= 5
    names = [item["name"] for item in data["items"]]
    assert "Documents" in names
    assert "Code" in names
    assert "Data" in names


# 11. Search
def test_workspace_file_search():
    response = client.get("/api/v1/workspace/search?q=report")
    assert response.status_code == 200
    data = response.json()
    assert data["total_matches"] >= 1
    assert any("sample_report.txt" in item["name"] for item in data["results"])


# 12. Metadata
def test_workspace_file_metadata():
    response = client.get("/api/v1/workspace/metadata?path=Code/sample.py")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "sample.py"
    assert data["category"] == "Code"
    assert data["item_type"] == "file"
    assert data["extension"] == ".py"


# 13. SHA-256
def test_workspace_file_sha256_hash():
    response = client.get("/api/v1/workspace/hash?path=Documents/sample_report.txt")
    assert response.status_code == 200
    data = response.json()
    assert data["relative_path"] == "Documents/sample_report.txt"
    assert len(data["sha256_hash"]) == 64  # Hex SHA256 length


# 14. Safe text reading
def test_workspace_safe_text_reading():
    response = client.get("/api/v1/workspace/content?path=Documents/sample_report.txt")
    assert response.status_code == 200
    data = response.json()
    assert "NOVA Test Workspace Report" in data["content"]
    assert data["is_truncated"] is False


# 15. Unsupported / binary file rejection
def test_workspace_unsupported_file_rejection(tmp_path):
    # Create binary file inside test_workspace to test extension rejection
    root = get_workspace_root()
    binary_file = root / "Misc" / "test_binary.bin"
    binary_file.write_bytes(b"\x00\x01\x02\x03\xff")
    try:
        response = client.get("/api/v1/workspace/content?path=Misc/test_binary.bin")
        assert response.status_code == 400
        assert "not supported" in response.json()["detail"]
    finally:
        if binary_file.exists():
            binary_file.unlink()


# 16. File classification
def test_file_classification_logic():
    assert classify_file_extension(".py") == "Code"
    assert classify_file_extension(".txt") == "Document"
    assert classify_file_extension(".csv") == "Data"
    assert classify_file_extension(".png") == "Image"
    assert classify_file_extension(".unknown") == "Other"

    assert is_safe_text_file(".py") is True
    assert is_safe_text_file(".txt") is True
    assert is_safe_text_file(".exe") is False


# 17. Workspace statistics
def test_workspace_stats():
    response = client.get("/api/v1/workspace/stats")
    assert response.status_code == 200
    data = response.json()
    assert data["total_files"] >= 4
    assert data["total_directories"] >= 5
    assert data["code_count"] >= 2
    assert data["document_count"] >= 1
    assert data["data_count"] >= 1


# 18. API responses validation
def test_workspace_stats_schema():
    stats = workspace_service.get_stats()
    assert stats.total_files >= 4
    assert isinstance(stats.recent_files, list)


# 19. Existing /api/health sanity verification
def test_existing_health_check_still_works():
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["security_policy"]["shell_execution_blocked"] is True


# 20. Tool Registry contains workspace tools
def test_tool_registry_workspace_tools():
    tools = tool_registry.list_tools()
    tool_names = [t["name"] for t in tools]
    assert "workspace.list_files" in tool_names
    assert "workspace.search_files" in tool_names
    assert "workspace.get_metadata" in tool_names
    assert "workspace.get_hash" in tool_names
    assert "workspace.read_text" in tool_names
    assert "workspace.get_stats" in tool_names

    # Verify all workspace tools are non-destructive and low risk
    for t in tools:
        if t["category"] == "workspace":
            assert t["is_destructive"] is False
            assert t["scope"] == "test_workspace"
