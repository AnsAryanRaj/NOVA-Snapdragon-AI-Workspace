"""REST API Router for NOVA Workspace Operations (/api/v1/workspace)."""

from typing import Optional
from fastapi import APIRouter, Query
from app.workspace.service import workspace_service
from app.workspace.schemas import (
    DirectoryListingResponse,
    FileMetadataResponse,
    FileHashResponse,
    TextContentResponse,
    WorkspaceStatsResponse,
    FileSearchResponse,
)

router = APIRouter(prefix="/workspace", tags=["Workspace"])


@router.get("/files", response_model=DirectoryListingResponse)
async def list_files(path: str = Query("", description="Relative path within workspace")):
    """List files and subdirectories inside the specified relative workspace path."""
    return workspace_service.list_directory(path)


@router.get("/search", response_model=FileSearchResponse)
async def search_files(q: str = Query(..., min_length=1, description="Search query string")):
    """Search workspace files and directories by name, path, or extension."""
    return workspace_service.search_files(q)


@router.get("/metadata", response_model=FileMetadataResponse)
async def get_metadata(path: str = Query(..., min_length=1, description="Relative path to file or directory")):
    """Retrieve detailed file or directory metadata."""
    return workspace_service.get_metadata(path)


@router.get("/hash", response_model=FileHashResponse)
async def get_file_hash(path: str = Query(..., min_length=1, description="Relative path to file")):
    """Calculate streaming SHA-256 checksum for a workspace file."""
    return workspace_service.calculate_sha256(path)


@router.get("/content", response_model=TextContentResponse)
async def get_file_content(path: str = Query(..., min_length=1, description="Relative path to text file")):
    """Read safe text file content up to configured size limit."""
    return workspace_service.read_text_content(path)


@router.get("/stats", response_model=WorkspaceStatsResponse)
async def get_workspace_stats():
    """Retrieve summary statistics and recent files for the controlled workspace."""
    return workspace_service.get_stats()
