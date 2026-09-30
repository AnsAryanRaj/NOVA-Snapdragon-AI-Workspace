"""Deterministic File Type Classifier for NOVA Workspace Engine."""

import os
from pathlib import Path

# Category Extension Mappings
CODE_EXTENSIONS = {
    ".py", ".cpp", ".c", ".cc", ".cxx", ".h", ".hpp",
    ".js", ".jsx", ".ts", ".tsx", ".java", ".kt", ".kts",
    ".css", ".scss", ".html", ".htm", ".rs", ".go", ".sh", ".ps1"
}

DOCUMENT_EXTENSIONS = {
    ".txt", ".md", ".markdown", ".pdf", ".doc", ".docx", ".rtf", ".odt"
}

DATA_EXTENSIONS = {
    ".csv", ".json", ".xml", ".yaml", ".yml", ".xlsx", ".xls", ".tsv", ".sqlite", ".db"
}

IMAGE_EXTENSIONS = {
    ".png", ".jpg", ".jpeg", ".webp", ".gif", ".bmp", ".tiff", ".svg"
}

# Safe Text-Reading Extension Set (Phase 3 allowed text files)
SAFE_TEXT_EXTENSIONS = {
    ".txt", ".md", ".csv", ".json", ".py", ".cpp", ".h", ".hpp",
    ".ts", ".tsx", ".js", ".jsx", ".css", ".html", ".yaml", ".yml", ".xml"
}


def classify_file_extension(extension: str) -> str:
    """Classifies a file extension into Code, Document, Data, Image, or Other.

    Args:
        extension: Extension string (e.g. '.py', '.txt'). Case-insensitive.

    Returns:
        str: Category name ('Code', 'Document', 'Data', 'Image', or 'Other').
    """
    ext = (extension or "").lower()
    if ext in CODE_EXTENSIONS:
        return "Code"
    if ext in DOCUMENT_EXTENSIONS:
        return "Document"
    if ext in DATA_EXTENSIONS:
        return "Data"
    if ext in IMAGE_EXTENSIONS:
        return "Image"
    return "Other"


def is_safe_text_file(extension: str) -> bool:
    """Determines whether a file extension is allowed for safe text reading.

    Args:
        extension: Extension string.

    Returns:
        bool: True if file is a safe supported text format.
    """
    return (extension or "").lower() in SAFE_TEXT_EXTENSIONS
