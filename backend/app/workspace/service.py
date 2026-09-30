"""Workspace Intelligence Service.

Combines path validation, file operations, hashing, text reading, and metadata extraction.
"""

import hashlib
from datetime import datetime, timezone
from pathlib import Path
from typing import List
from fastapi import HTTPException

from app.core.config import settings
from app.core.path_security import validate_workspace_path, get_workspace_root
from app.workspace.classifier import classify_file_extension, is_safe_text_file
from app.workspace.scanner import (
    build_file_item_schema,
    scan_directory,
    search_workspace,
    calculate_workspace_stats,
)
from app.workspace.schemas import (
    DirectoryListingResponse,
    FileItemSchema,
    FileMetadataResponse,
    FileHashResponse,
    TextContentResponse,
    WorkspaceStatsResponse,
    FileSearchResponse,
)


class WorkspaceService:
    """Core Workspace Operations Service."""

    @staticmethod
    def list_directory(relative_path: str = "") -> DirectoryListingResponse:
        """Lists files and directories inside a safe workspace relative path."""
        target_path, clean_rel_path = validate_workspace_path(relative_path)
        workspace_root = get_workspace_root()

        if not target_path.exists():
            raise HTTPException(
                status_code=404,
                detail=f"Workspace path '{clean_rel_path}' does not exist."
            )

        if not target_path.is_dir():
            raise HTTPException(
                status_code=400,
                detail=f"Target path '{clean_rel_path}' is a file, not a directory."
            )

        items = scan_directory(target_path, workspace_root)
        return DirectoryListingResponse(
            path=clean_rel_path,
            items=items,
            total_count=len(items)
        )

    @staticmethod
    def search_files(query: str) -> FileSearchResponse:
        """Searches workspace files and directories by query."""
        workspace_root = get_workspace_root()
        results = search_workspace(workspace_root, query)
        return FileSearchResponse(
            query=query,
            results=results,
            total_matches=len(results)
        )

    @staticmethod
    def get_metadata(relative_path: str) -> FileMetadataResponse:
        """Retrieves detailed metadata for a file or directory."""
        target_path, clean_rel_path = validate_workspace_path(relative_path)
        workspace_root = get_workspace_root()

        if not target_path.exists():
            raise HTTPException(
                status_code=404,
                detail=f"Target path '{clean_rel_path}' does not exist."
            )

        is_dir = target_path.is_dir()
        stat = target_path.stat()
        ext = target_path.suffix if not is_dir else ""
        category = classify_file_extension(ext) if not is_dir else "Folder"

        created_time = datetime.fromtimestamp(
            stat.st_ctime if hasattr(stat, "st_ctime") else stat.st_mtime,
            tz=timezone.utc
        ).isoformat()

        modified_time = datetime.fromtimestamp(
            stat.st_mtime,
            tz=timezone.utc
        ).isoformat()

        return FileMetadataResponse(
            name=target_path.name or workspace_root.name,
            relative_path=clean_rel_path,
            extension=ext,
            size_bytes=stat.st_size if not is_dir else 0,
            created_time=created_time,
            modified_time=modified_time,
            item_type="directory" if is_dir else "file",
            category=category,
        )

    @staticmethod
    def calculate_sha256(relative_path: str) -> FileHashResponse:
        """Calculates SHA-256 hash using streaming chunked reading."""
        target_path, clean_rel_path = validate_workspace_path(relative_path)

        if not target_path.exists():
            raise HTTPException(
                status_code=404,
                detail=f"File '{clean_rel_path}' does not exist."
            )

        if target_path.is_dir():
            raise HTTPException(
                status_code=400,
                detail=f"Target path '{clean_rel_path}' is a directory, not a file."
            )

        hasher = hashlib.sha256()
        chunk_size = 65536  # 64 KB chunks
        try:
            with open(target_path, "rb") as f:
                while chunk := f.read(chunk_size):
                    hasher.update(chunk)
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to read file for hashing: {str(e)}"
            )

        return FileHashResponse(
            relative_path=clean_rel_path,
            sha256_hash=hasher.hexdigest(),
            size_bytes=target_path.stat().st_size
        )

    @staticmethod
    def read_text_content(relative_path: str) -> TextContentResponse:
        """Safely reads text content from a supported text file within size limits."""
        target_path, clean_rel_path = validate_workspace_path(relative_path)

        if not target_path.exists():
            raise HTTPException(
                status_code=404,
                detail=f"File '{clean_rel_path}' does not exist."
            )

        if target_path.is_dir():
            raise HTTPException(
                status_code=400,
                detail=f"Target path '{clean_rel_path}' is a directory, not a text file."
            )

        ext = target_path.suffix
        if not is_safe_text_file(ext):
            raise HTTPException(
                status_code=400,
                detail=f"File format '{ext}' is not supported for safe text content reading."
            )

        file_size = target_path.stat().st_size
        max_bytes = settings.MAX_TEXT_READ_BYTES
        is_truncated = file_size > max_bytes

        try:
            with open(target_path, "r", encoding="utf-8", errors="replace") as f:
                content = f.read(max_bytes)
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to read text file: {str(e)}"
            )

        return TextContentResponse(
            relative_path=clean_rel_path,
            content=content,
            size_bytes=file_size,
            max_bytes_read=max_bytes,
            is_truncated=is_truncated
        )

    @staticmethod
    def get_stats() -> WorkspaceStatsResponse:
        """Calculates total workspace summary statistics."""
        workspace_root = get_workspace_root()
        return calculate_workspace_stats(workspace_root)


workspace_service = WorkspaceService()
