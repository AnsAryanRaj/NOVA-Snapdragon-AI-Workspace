"""Workspace Traversal & Scanner Utilities."""

import os
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Dict, Any
from app.workspace.classifier import classify_file_extension
from app.workspace.schemas import FileItemSchema, WorkspaceStatsResponse


def _format_datetime(timestamp: float) -> str:
    """Formats epoch timestamp into ISO 8601 string."""
    return datetime.fromtimestamp(timestamp, tz=timezone.utc).isoformat()


def build_file_item_schema(resolved_path: Path, workspace_root: Path) -> FileItemSchema:
    """Constructs a FileItemSchema from a resolved Path."""
    rel = resolved_path.relative_to(workspace_root)
    clean_rel_path = str(rel).replace("\\", "/")
    if clean_rel_path == ".":
        clean_rel_path = ""

    is_dir = resolved_path.is_dir()
    stat = resolved_path.stat()
    ext = resolved_path.suffix if not is_dir else ""
    category = classify_file_extension(ext) if not is_dir else "Folder"

    return FileItemSchema(
        name=resolved_path.name or workspace_root.name,
        relative_path=clean_rel_path,
        item_type="directory" if is_dir else "file",
        size_bytes=stat.st_size if not is_dir else 0,
        modified_time=_format_datetime(stat.st_mtime),
        extension=ext,
        category=category,
    )


def scan_directory(target_path: Path, workspace_root: Path) -> List[FileItemSchema]:
    """Scans immediate items inside target_path."""
    items: List[FileItemSchema] = []
    if not target_path.exists() or not target_path.is_dir():
        return items

    for entry in sorted(target_path.iterdir(), key=lambda p: (not p.is_dir(), p.name.lower())):
        # Skip pycache and hidden system files if needed
        if entry.name.startswith(".") or entry.name == "__pycache__":
            continue
        items.append(build_file_item_schema(entry, workspace_root))

    return items


def search_workspace(workspace_root: Path, query: str) -> List[FileItemSchema]:
    """Searches workspace recursively for items matching query in name, path, or extension."""
    results: List[FileItemSchema] = []
    q = (query or "").strip().lower()
    if not q:
        return results

    for root, dirs, files in os.walk(workspace_root):
        # Prune hidden dirs & pycache
        dirs[:] = [d for d in dirs if not d.startswith(".") and d != "__pycache__"]

        for file_name in files:
            if file_name.startswith("."):
                continue
            full_path = Path(root) / file_name
            rel_str = str(full_path.relative_to(workspace_root)).replace("\\", "/")

            if q in file_name.lower() or q in rel_str.lower() or q in full_path.suffix.lower():
                results.append(build_file_item_schema(full_path, workspace_root))

        for dir_name in dirs:
            full_path = Path(root) / dir_name
            rel_str = str(full_path.relative_to(workspace_root)).replace("\\", "/")

            if q in dir_name.lower() or q in rel_str.lower():
                results.append(build_file_item_schema(full_path, workspace_root))

    return results


def calculate_workspace_stats(workspace_root: Path) -> WorkspaceStatsResponse:
    """Calculates workspace statistics across all contained files and directories."""
    total_files = 0
    total_dirs = 0
    total_size = 0
    code_cnt = 0
    doc_cnt = 0
    data_cnt = 0
    img_cnt = 0
    other_cnt = 0

    all_files: List[Path] = []

    for root, dirs, files in os.walk(workspace_root):
        dirs[:] = [d for d in dirs if not d.startswith(".") and d != "__pycache__"]
        total_dirs += len(dirs)

        for f in files:
            if f.startswith("."):
                continue
            file_path = Path(root) / f
            all_files.append(file_path)
            total_files += 1

            try:
                stat = file_path.stat()
                total_size += stat.st_size

                cat = classify_file_extension(file_path.suffix)
                if cat == "Code":
                    code_cnt += 1
                elif cat == "Document":
                    doc_cnt += 1
                elif cat == "Data":
                    data_cnt += 1
                elif cat == "Image":
                    img_cnt += 1
                else:
                    other_cnt += 1
            except OSError:
                pass

    # Sort files by modified time descending to get recent files
    all_files.sort(key=lambda p: p.stat().st_mtime if p.exists() else 0, reverse=True)
    recent_schemas = [build_file_item_schema(p, workspace_root) for p in all_files[:10]]

    return WorkspaceStatsResponse(
        total_files=total_files,
        total_directories=total_dirs,
        total_size_bytes=total_size,
        code_count=code_cnt,
        document_count=doc_cnt,
        data_count=data_cnt,
        image_count=img_cnt,
        other_count=other_cnt,
        recent_files=recent_schemas,
    )
