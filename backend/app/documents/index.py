"""Workspace Document Indexer Service for incremental indexing and database sync."""

import os
import hashlib
import time
from datetime import datetime
from pathlib import Path
from typing import List, Set, Tuple, Optional
from sqlalchemy.orm import Session

from app.core.path_security import validate_workspace_path, get_workspace_root
from app.db.models import DocumentModel, DocumentChunkModel
from app.documents.extractor import extract_text_from_file, is_extension_supported, get_mime_type
from app.documents.chunker import chunk_extracted_data
from app.documents.schemas import IndexingSummary


IGNORED_DIRS = {
    ".git", ".venv", "venv", "node_modules", "__pycache__",
    ".pytest_cache", ".idea", ".vscode", "dist", "build"
}


def generate_doc_id(clean_relative_path: str, content_hash: Optional[str] = None) -> str:
    """Generate a stable, deterministic document ID from relative path and content hash."""
    clean_rel = clean_relative_path.strip().replace("\\", "/").lstrip("/")
    if content_hash:
        key = f"{clean_rel.lower()}:{content_hash}"
    else:
        key = clean_rel.lower()
    return hashlib.sha256(key.encode("utf-8")).hexdigest()[:32]


def compute_file_hash(abs_path: Path) -> str:
    """Compute sha256 hash of file content."""
    sha = hashlib.sha256()
    with open(abs_path, "rb") as f:
        while chunk := f.read(65536):
            sha.update(chunk)
    return sha.hexdigest()


def index_workspace_documents(
    db: Session,
    subpath: str = "",
    force_reindex: bool = False
) -> IndexingSummary:
    """
    Scan workspace directory incrementally and index documents into SQLite DB.
    """
    start_time = time.time()
    summary = IndexingSummary()

    # Validate security boundary for target root
    target_abs, clean_subpath = validate_workspace_path(subpath)

    if not target_abs.exists():
        summary.duration_ms = int((time.time() - start_time) * 1000)
        return summary

    workspace_root = get_workspace_root()

    # Gather candidate files
    scanned_relative_paths: Set[str] = set()
    candidate_files: List[Tuple[Path, str]] = []

    if target_abs.is_file():
        if is_extension_supported(target_abs.suffix):
            rel_str = str(target_abs.relative_to(workspace_root)).replace("\\", "/")
            candidate_files.append((target_abs, rel_str))
            scanned_relative_paths.add(rel_str)
    else:
        for root, dirs, files in os.walk(target_abs):
            # Prune ignored directories
            dirs[:] = [d for d in dirs if d not in IGNORED_DIRS and not d.startswith(".")]

            for file_name in files:
                if file_name.startswith("."):
                    continue
                file_abs = Path(root) / file_name
                if is_extension_supported(file_abs.suffix):
                    rel_str = str(file_abs.relative_to(workspace_root)).replace("\\", "/")
                    candidate_files.append((file_abs, rel_str))
                    scanned_relative_paths.add(rel_str)

    summary.total_found = len(candidate_files)

    # Process each candidate file
    for file_abs, rel_path in candidate_files:
        try:
            stat = file_abs.stat()
            file_size = stat.st_size
            mtime = datetime.fromtimestamp(stat.st_mtime)
            content_hash = compute_file_hash(file_abs)
            doc_id = generate_doc_id(rel_path, content_hash)

            # Check existing record in DB by relative path or doc_id
            existing_doc = db.query(DocumentModel).filter(
                (DocumentModel.relative_path == rel_path) | (DocumentModel.id == doc_id)
            ).first()

            if existing_doc and not force_reindex:
                # If unchanged, skip
                if (
                    existing_doc.content_hash == content_hash and
                    existing_doc.size_bytes == file_size and
                    existing_doc.extraction_status == "SUCCESS"
                ):
                    summary.skipped_unchanged += 1
                    continue

            # Extract text
            extracted = extract_text_from_file(file_abs)
            ext = file_abs.suffix.lower()
            mime = get_mime_type(ext)

            # Split into chunks
            chunks = chunk_extracted_data(extracted) if extracted.status == "SUCCESS" else []

            # Remove old chunks if updating
            if existing_doc:
                db.query(DocumentChunkModel).filter(DocumentChunkModel.doc_id == existing_doc.id).delete()
                db.flush()
                summary.updated += 1
            else:
                summary.indexed_new += 1

            # Update or create document record
            doc_record = existing_doc or DocumentModel(id=doc_id)
            doc_record.id = doc_id
            doc_record.relative_path = rel_path
            doc_record.file_name = file_abs.name
            doc_record.file_extension = ext
            doc_record.mime_type = mime
            doc_record.size_bytes = file_size
            doc_record.content_hash = content_hash
            doc_record.page_count = extracted.page_count
            doc_record.chunk_count = len(chunks)
            doc_record.indexed_at = datetime.utcnow()
            doc_record.last_modified = mtime
            doc_record.extraction_status = extracted.status
            doc_record.error_message = extracted.error_message

            if not existing_doc:
                db.add(doc_record)


            # Insert chunks
            for chk in chunks:
                chunk_record = DocumentChunkModel(
                    chunk_id=f"{doc_id}_c{chk.chunk_index}",
                    doc_id=doc_id,
                    chunk_index=chk.chunk_index,
                    content=chk.content,
                    start_char=chk.start_char,
                    end_char=chk.end_char,
                    page_number=chk.page_number,
                    token_count=chk.token_count
                )
                db.add(chunk_record)

            summary.total_chunks += len(chunks)

            if extracted.status != "SUCCESS":
                summary.failed += 1

            db.commit()

        except Exception as e:
            db.rollback()
            summary.failed += 1



    # Prune stale DB records if scanning the full workspace or a folder
    if clean_subpath == "":
        existing_db_docs = db.query(DocumentModel).all()
        for doc in existing_db_docs:
            if doc.relative_path not in scanned_relative_paths:
                db.query(DocumentChunkModel).filter(DocumentChunkModel.doc_id == doc.id).delete()
                db.delete(doc)
                summary.pruned_deleted += 1
        db.commit()

    summary.duration_ms = int((time.time() - start_time) * 1000)
    return summary
