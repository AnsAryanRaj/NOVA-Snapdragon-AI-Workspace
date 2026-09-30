"""Document Intelligence Service providing search, retrieval, and stats."""

import re
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import or_, func

from app.db.models import DocumentModel, DocumentChunkModel
from app.documents.schemas import (
    DocumentMetadata,
    DocumentDetail,
    DocumentContentResponse,
    DocumentChunkSchema,
    SearchMatch,
    DocumentSearchResult,
    DocumentStats
)
from app.documents.index import generate_doc_id


def search_documents(
    db: Session,
    query: str,
    limit: int = 20
) -> DocumentSearchResult:
    """
    Perform lexical search over indexed workspace document chunks.
    Scores and ranks matches based on term frequency and document title relevance.
    """
    clean_query = query.strip()
    if not clean_query:
        return DocumentSearchResult(query=query, total_matches=0, matches=[])

    query_terms = [t.lower() for t in re.split(r"\s+", clean_query) if len(t.strip()) > 0]
    if not query_terms:
        return DocumentSearchResult(query=query, total_matches=0, matches=[])

    # Build SQL ILIKE filters for each query term
    chunk_filters = [DocumentChunkModel.content.ilike(f"%{term}%") for term in query_terms]

    # Query matching chunks
    matching_chunks = (
        db.query(DocumentChunkModel, DocumentModel)
        .join(DocumentModel, DocumentChunkModel.doc_id == DocumentModel.id)
        .filter(or_(*chunk_filters))
        .limit(200)
        .all()
    )

    scored_matches: List[SearchMatch] = []

    for chunk, doc in matching_chunks:
        content_lower = chunk.content.lower()
        matched_terms = [t for t in query_terms if t in content_lower]
        if not matched_terms:
            continue

        # Calculate score
        term_freq_score = sum(content_lower.count(t) for t in matched_terms)
        title_bonus = 3.0 if any(t in doc.file_name.lower() for t in query_terms) else 0.0
        path_bonus = 1.5 if any(t in doc.relative_path.lower() for t in query_terms) else 0.0
        coverage_score = len(matched_terms) / float(len(query_terms)) * 5.0

        total_score = round(term_freq_score + title_bonus + path_bonus + coverage_score, 2)

        # Generate snippet
        snippet = _generate_snippet(chunk.content, matched_terms)

        scored_matches.append(
            SearchMatch(
                doc_id=doc.id,
                relative_path=doc.relative_path,
                file_name=doc.file_name,
                file_extension=doc.file_extension,
                chunk_id=chunk.chunk_id,
                chunk_index=chunk.chunk_index,
                snippet=snippet,
                full_chunk_text=chunk.content,
                page_number=chunk.page_number,
                score=total_score,
                matched_terms=matched_terms
            )
        )

    # Sort matches by score descending
    scored_matches.sort(key=lambda m: m.score, reverse=True)
    top_matches = scored_matches[:limit]

    return DocumentSearchResult(
        query=query,
        total_matches=len(scored_matches),
        matches=top_matches
    )


def list_documents(
    db: Session,
    subpath: Optional[str] = None,
    extension: Optional[str] = None,
    status: Optional[str] = None,
    limit: int = 100
) -> List[DocumentMetadata]:
    """List indexed workspace documents with optional filtering."""
    query = db.query(DocumentModel)

    if subpath:
        clean_sub = subpath.strip().replace("\\", "/").strip("/")
        if clean_sub:
            query = query.filter(DocumentModel.relative_path.startswith(clean_sub))

    if extension:
        ext = extension.strip().lower()
        if not ext.startswith("."):
            ext = f".{ext}"
        query = query.filter(DocumentModel.file_extension == ext)

    if status:
        query = query.filter(DocumentModel.extraction_status == status.upper())

    docs = query.order_by(DocumentModel.relative_path.asc()).limit(limit).all()
    return [DocumentMetadata.model_validate(d) for d in docs]


def get_document_detail(db: Session, doc_id_or_path: str) -> Optional[DocumentDetail]:
    """Retrieve document metadata and all extracted chunks."""
    identifier = doc_id_or_path.strip()

    doc = db.query(DocumentModel).filter(DocumentModel.id == identifier).first()
    if not doc:
        clean_rel = identifier.replace("\\", "/").lstrip("/")
        doc_id = generate_doc_id(clean_rel)
        doc = db.query(DocumentModel).filter(
            or_(
                DocumentModel.id == doc_id,
                DocumentModel.relative_path == clean_rel,
                DocumentModel.file_name == clean_rel,
                DocumentModel.relative_path.endswith("/" + clean_rel)
            )
        ).first()

    if not doc:
        return None

    chunks = (
        db.query(DocumentChunkModel)
        .filter(DocumentChunkModel.doc_id == doc.id)
        .order_by(DocumentChunkModel.chunk_index.asc())
        .all()
    )

    doc_meta = DocumentMetadata.model_validate(doc)
    chunk_schemas = [DocumentChunkSchema.model_validate(c) for c in chunks]

    return DocumentDetail(
        **doc_meta.model_dump(),
        chunks=chunk_schemas
    )


def get_document_content(db: Session, doc_id_or_path: str) -> Optional[DocumentContentResponse]:
    """Retrieve extracted text content and chunks for an indexed document."""
    doc_detail = get_document_detail(db, doc_id_or_path)
    if not doc_detail:
        return None

    full_text = "\n\n".join(c.content for c in doc_detail.chunks)
    return DocumentContentResponse(
        doc_id=doc_detail.id,
        relative_path=doc_detail.relative_path,
        file_name=doc_detail.file_name,
        extraction_status=doc_detail.extraction_status,
        page_count=doc_detail.page_count,
        chunk_count=doc_detail.chunk_count,
        full_text=full_text,
        chunks=doc_detail.chunks
    )



def get_document_stats(db: Session) -> DocumentStats:
    """Calculate index statistics."""
    total_docs = db.query(func.count(DocumentModel.id)).scalar() or 0
    total_chunks = db.query(func.count(DocumentChunkModel.id)).scalar() or 0
    total_size = db.query(func.sum(DocumentModel.size_bytes)).scalar() or 0

    # Group by file_extension
    type_counts = dict(
        db.query(DocumentModel.file_extension, func.count(DocumentModel.id))
        .group_by(DocumentModel.file_extension)
        .all()
    )

    # Group by extraction_status
    status_counts = dict(
        db.query(DocumentModel.extraction_status, func.count(DocumentModel.id))
        .group_by(DocumentModel.extraction_status)
        .all()
    )

    return DocumentStats(
        total_documents=total_docs,
        total_chunks=total_chunks,
        total_size_bytes=total_size,
        documents_by_type=type_counts,
        extraction_statuses=status_counts
    )


def _generate_snippet(content: str, matched_terms: List[str], max_length: int = 250) -> str:
    """Generate a clean contextual snippet highlighting matched terms."""
    if not content:
        return ""

    content_lower = content.lower()
    first_match_idx = len(content)

    for term in matched_terms:
        idx = content_lower.find(term)
        if idx != -1 and idx < first_match_idx:
            first_match_idx = idx

    if first_match_idx == len(content):
        return content[:max_length] + ("..." if len(content) > max_length else "")

    start_idx = max(0, first_match_idx - 60)
    end_idx = min(len(content), first_match_idx + max_length - 60)

    snippet = content[start_idx:end_idx]

    if start_idx > 0:
        snippet = "..." + snippet
    if end_idx < len(content):
        snippet = snippet + "..."

    return snippet
