"""Path Security Module for NOVA Workspace Assistant.

Strictly enforces filesystem containment within the configured workspace root.
Rejects path traversal, drive letter escapes, UNC paths, and access outside the workspace boundary.
"""

import os
from pathlib import Path
from typing import Union, Tuple
from fastapi import HTTPException
from app.core.config import settings


class WorkspaceSecurityError(Exception):
    """Custom exception raised when a path security violation is detected."""
    pass


def get_workspace_root() -> Path:
    """Returns the canonical resolved workspace root directory."""
    root_path = Path(settings.WORKSPACE_ROOT).resolve()
    if not root_path.exists():
        root_path.mkdir(parents=True, exist_ok=True)
    return root_path


def validate_workspace_path(relative_path: Union[str, Path] = "") -> Tuple[Path, str]:
    """Validates and resolves a client-supplied path against the workspace root boundary.

    Args:
        relative_path: Target path string or Path object supplied by API client or tool.

    Returns:
        Tuple containing:
          - safe_resolved_path (Path): Resolved canonical path on the local filesystem.
          - clean_relative_path (str): Safe normalized relative path relative to workspace root.

    Raises:
        WorkspaceSecurityError or HTTPException(400) if path escapes or violates security boundary.
    """
    workspace_root = get_workspace_root()
    path_str = str(relative_path or "").strip()

    # Reject null bytes
    if "\x00" in path_str:
        raise HTTPException(
            status_code=400,
            detail="Security Violation: Path contains invalid null byte characters."
        )

    # Reject UNC paths (e.g., \\server\share or //server/share)
    if path_str.startswith("\\\\") or path_str.startswith("//"):
        raise HTTPException(
            status_code=400,
            detail="Security Violation: UNC network paths are strictly forbidden."
        )

    # Check for drive letter escapes (e.g., C:\, C:, D:/) if client passes raw drive path
    if len(path_str) >= 2 and path_str[1] == ":" and path_str[0].isalpha():
        # Check if it attempts to target a different drive or absolute path outside
        candidate = Path(path_str).resolve()
        try:
            candidate.relative_to(workspace_root)
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail=f"Security Violation: Path '{path_str}' attempts to escape workspace root."
            )

    # Construct target candidate path relative to workspace root
    clean_path_input = path_str.lstrip("/\\")
    candidate_path = (workspace_root / clean_path_input).resolve()

    # Enforce strict canonical containment check
    try:
        rel = candidate_path.relative_to(workspace_root)
        clean_rel_str = str(rel).replace("\\", "/")
        if clean_rel_str == ".":
            clean_rel_str = ""
        return candidate_path, clean_rel_str
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail=f"Security Violation: Target path '{path_str}' resolves outside workspace boundary."
        )
