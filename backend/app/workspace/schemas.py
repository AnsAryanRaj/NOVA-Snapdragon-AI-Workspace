"""Pydantic Schemas for NOVA Workspace Operations."""

from typing import List, Optional
from pydantic import BaseModel, Field


class FileItemSchema(BaseModel):
    name: str = Field(..., json_schema_extra={"example": "sample_report.txt"})
    relative_path: str = Field(..., json_schema_extra={"example": "Documents/sample_report.txt"})
    item_type: str = Field(..., json_schema_extra={"example": "file"})  # "file" or "directory"
    size_bytes: int = Field(..., json_schema_extra={"example": 1024})
    modified_time: str = Field(..., json_schema_extra={"example": "2026-09-24T13:51:51Z"})
    extension: str = Field(..., json_schema_extra={"example": ".txt"})
    category: str = Field(..., json_schema_extra={"example": "Document"})  # Code, Document, Data, Image, Other


class DirectoryListingResponse(BaseModel):
    path: str = Field(..., json_schema_extra={"example": "Documents"})
    items: List[FileItemSchema]
    total_count: int = Field(..., json_schema_extra={"example": 1})


class FileMetadataResponse(BaseModel):
    name: str = Field(..., json_schema_extra={"example": "sample_report.txt"})
    relative_path: str = Field(..., json_schema_extra={"example": "Documents/sample_report.txt"})
    extension: str = Field(..., json_schema_extra={"example": ".txt"})
    size_bytes: int = Field(..., json_schema_extra={"example": 1024})
    created_time: str = Field(..., json_schema_extra={"example": "2026-09-24T13:50:00Z"})
    modified_time: str = Field(..., json_schema_extra={"example": "2026-09-24T13:51:51Z"})
    item_type: str = Field(..., json_schema_extra={"example": "file"})
    category: str = Field(..., json_schema_extra={"example": "Document"})


class FileHashResponse(BaseModel):
    relative_path: str = Field(..., json_schema_extra={"example": "Documents/sample_report.txt"})
    sha256_hash: str = Field(..., json_schema_extra={"example": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"})
    size_bytes: int = Field(..., json_schema_extra={"example": 1024})


class TextContentResponse(BaseModel):
    relative_path: str = Field(..., json_schema_extra={"example": "Documents/sample_report.txt"})
    content: str = Field(..., json_schema_extra={"example": "NOVA Test Workspace Report"})
    size_bytes: int = Field(..., json_schema_extra={"example": 1024})
    max_bytes_read: int = Field(..., json_schema_extra={"example": 2000000})
    is_truncated: bool = Field(False, json_schema_extra={"example": False})


class WorkspaceStatsResponse(BaseModel):
    total_files: int = Field(..., json_schema_extra={"example": 14})
    total_directories: int = Field(..., json_schema_extra={"example": 6})
    total_size_bytes: int = Field(..., json_schema_extra={"example": 45000})
    code_count: int = Field(..., json_schema_extra={"example": 4})
    document_count: int = Field(..., json_schema_extra={"example": 3})
    data_count: int = Field(..., json_schema_extra={"example": 2})
    image_count: int = Field(..., json_schema_extra={"example": 0})
    other_count: int = Field(..., json_schema_extra={"example": 5})
    recent_files: List[FileItemSchema]


class FileSearchResponse(BaseModel):
    query: str = Field(..., json_schema_extra={"example": "report"})
    results: List[FileItemSchema]
    total_matches: int = Field(..., json_schema_extra={"example": 1})
