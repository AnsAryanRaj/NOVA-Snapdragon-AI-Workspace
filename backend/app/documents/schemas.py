"""Pydantic schemas for Document Intelligence and Semantic Retrieval."""

from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict


class DocumentBase(BaseModel):
    relative_path: str
    file_name: str
    file_extension: str
    mime_type: str
    size_bytes: int
    content_hash: str
    page_count: int = 1
    chunk_count: int = 0
    extraction_status: str = "SUCCESS"
    error_message: Optional[str] = None


class DocumentMetadata(DocumentBase):
    id: str
    indexed_at: datetime
    last_modified: datetime

    model_config = ConfigDict(from_attributes=True)


class DocumentChunkSchema(BaseModel):
    chunk_id: str
    doc_id: str
    chunk_index: int
    content: str
    start_char: int
    end_char: int
    page_number: Optional[int] = 1
    token_count: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)



class DocumentDetail(DocumentMetadata):
    chunks: List[DocumentChunkSchema] = []


class DocumentContentResponse(BaseModel):
    doc_id: str
    relative_path: str
    file_name: str
    extraction_status: str
    page_count: int
    chunk_count: int
    full_text: str
    chunks: List[DocumentChunkSchema] = []



class SearchMatch(BaseModel):
    doc_id: str
    relative_path: str
    file_name: str
    file_extension: str
    chunk_id: str
    chunk_index: int
    snippet: str
    full_chunk_text: str
    page_number: Optional[int] = 1
    score: float
    matched_terms: List[str] = []


class DocumentSearchResult(BaseModel):
    query: str
    total_matches: int
    matches: List[SearchMatch] = []


class IndexingRequest(BaseModel):
    subpath: Optional[str] = ""
    force_reindex: bool = False


class IndexingSummary(BaseModel):
    total_found: int = 0
    indexed_new: int = 0
    updated: int = 0
    skipped_unchanged: int = 0
    failed: int = 0
    pruned_deleted: int = 0
    total_chunks: int = 0
    duration_ms: int = 0


class DocumentStats(BaseModel):
    total_documents: int
    total_chunks: int
    total_size_bytes: int
    documents_by_type: dict
    extraction_statuses: dict
