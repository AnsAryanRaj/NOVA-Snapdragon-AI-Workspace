"""Document Intelligence REST API Endpoints."""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.documents.schemas import (
    IndexingRequest,
    IndexingSummary,
    DocumentSearchResult,
    DocumentMetadata,
    DocumentDetail,
    DocumentContentResponse,
    DocumentStats
)
from app.documents.index import index_workspace_documents
from app.documents.service import (
    search_documents,
    list_documents,
    get_document_detail,
    get_document_content,
    get_document_stats
)

router = APIRouter(prefix="/documents", tags=["documents"])


@router.post("/index", response_model=IndexingSummary)
def trigger_workspace_indexing(
    request: Optional[IndexingRequest] = None,
    db: Session = Depends(get_db)
):
    """
    Scan and index workspace documents incrementally.
    Strictly scoped to configured test_workspace root.
    """
    req = request or IndexingRequest()
    try:
        summary = index_workspace_documents(
            db=db,
            subpath=req.subpath or "",
            force_reindex=req.force_reindex
        )
        return summary
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to complete document indexing: {str(e)}"
        )


@router.get("/search", response_model=DocumentSearchResult)
def search_workspace_documents(
    q: str = Query(..., min_length=1, description="Search query string"),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Perform lexical keyword search over indexed workspace document chunks."""
    return search_documents(db=db, query=q, limit=limit)


@router.get("", response_model=List[DocumentMetadata])
@router.get("/list", response_model=List[DocumentMetadata])
def get_indexed_documents(
    subpath: Optional[str] = Query(None, description="Subpath filter"),
    extension: Optional[str] = Query(None, description="Extension filter, e.g. .pdf or .md"),
    status: Optional[str] = Query(None, description="Status filter: SUCCESS, FAILED"),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db)
):
    """List indexed workspace documents."""
    return list_documents(
        db=db,
        subpath=subpath,
        extension=extension,
        status=status,
        limit=limit
    )


@router.get("/stats", response_model=DocumentStats)
def get_indexing_stats(db: Session = Depends(get_db)):
    """Get statistics for the workspace document index."""
    return get_document_stats(db=db)


@router.get("/{doc_id}", response_model=DocumentDetail)
def get_document_by_id(
    doc_id: str,
    db: Session = Depends(get_db)
):
    """Get metadata and chunks for a specific indexed document."""
    doc_detail = get_document_detail(db=db, doc_id_or_path=doc_id)
    if not doc_detail:
        raise HTTPException(
            status_code=404,
            detail=f"Document with ID or path '{doc_id}' was not found in the index."
        )
    return doc_detail


@router.get("/{doc_id}/content", response_model=DocumentContentResponse)
def get_document_content_by_id(
    doc_id: str,
    db: Session = Depends(get_db)
):
    """Get extracted text content and chunks for a specific indexed document."""
    doc_content = get_document_content(db=db, doc_id_or_path=doc_id)
    if not doc_content:
        raise HTTPException(
            status_code=404,
            detail=f"Document content for ID or path '{doc_id}' was not found in the index."
        )
    return doc_content

