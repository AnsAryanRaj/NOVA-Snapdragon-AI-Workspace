"""Local document text extractor supporting text, code, structured data, and PDFs."""

import os
from pathlib import Path
from typing import Dict, List, Any, Tuple, Optional
import fitz  # PyMuPDF


SUPPORTED_TEXT_EXTENSIONS = {
    ".txt", ".md", ".log", ".rst", ".org", ".env", ".ini",
    ".yaml", ".yml", ".toml", ".json", ".csv", ".tsv", ".jsonl"
}

SUPPORTED_CODE_EXTENSIONS = {
    ".py", ".js", ".ts", ".tsx", ".jsx", ".cpp", ".c", ".h", ".hpp",
    ".cs", ".java", ".kt", ".go", ".rs", ".rb", ".php", ".sh", ".ps1",
    ".html", ".css", ".xml", ".sql"
}

SUPPORTED_DOC_EXTENSIONS = {".pdf"}

ALL_SUPPORTED_EXTENSIONS = (
    SUPPORTED_TEXT_EXTENSIONS | SUPPORTED_CODE_EXTENSIONS | SUPPORTED_DOC_EXTENSIONS
)


class ExtractedData:
    def __init__(
        self,
        full_text: str,
        pages: List[Dict[str, Any]],
        page_count: int,
        status: str = "SUCCESS",
        error_message: Optional[str] = None
    ):
        self.full_text = full_text
        self.pages = pages  # List of {"page_number": int, "text": str}
        self.page_count = page_count
        self.status = status
        self.error_message = error_message


def is_extension_supported(extension: str) -> bool:
    """Check if file extension is supported for document indexing."""
    return extension.lower() in ALL_SUPPORTED_EXTENSIONS


def get_mime_type(extension: str) -> str:
    """Map extension to MIME type."""
    ext = extension.lower()
    if ext == ".pdf":
        return "application/pdf"
    elif ext in (".json", ".jsonl"):
        return "application/json"
    elif ext in (".csv", ".tsv"):
        return "text/csv"
    elif ext == ".html":
        return "text/html"
    elif ext == ".xml":
        return "text/xml"
    elif ext == ".md":
        return "text/markdown"
    elif ext in SUPPORTED_CODE_EXTENSIONS:
        return "text/x-code"
    return "text/plain"


def extract_text_from_file(file_path: Path) -> ExtractedData:
    """
    Extract text content from a file safely.
    Handles text, code, structured formats, and PDFs via PyMuPDF.
    """
    ext = file_path.suffix.lower()

    if ext not in ALL_SUPPORTED_EXTENSIONS:
        return ExtractedData(
            full_text="",
            pages=[],
            page_count=0,
            status="FAILED",
            error_message=f"Unsupported file extension: '{ext}'"
        )

    if ext == ".pdf":
        return _extract_pdf(file_path)
    else:
        return _extract_text_file(file_path)


def _extract_text_file(file_path: Path) -> ExtractedData:
    """Extract text from plain text, code, or structured data files."""
    try:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                text = f.read()
        except UnicodeDecodeError:
            with open(file_path, "r", encoding="utf-8", errors="replace") as f:
                text = f.read()

        pages = [{"page_number": 1, "text": text}]
        return ExtractedData(
            full_text=text,
            pages=pages,
            page_count=1,
            status="SUCCESS"
        )
    except Exception as e:
        return ExtractedData(
            full_text="",
            pages=[],
            page_count=0,
            status="FAILED",
            error_message=f"Text extraction failed: {str(e)}"
        )


def _extract_pdf(file_path: Path) -> ExtractedData:
    """Extract text from PDF using PyMuPDF (fitz)."""
    try:
        doc = fitz.open(str(file_path))
        page_count = len(doc)
        pages = []
        full_text_parts = []

        for page_idx in range(page_count):
            page_num = page_idx + 1
            page = doc[page_idx]
            page_text = page.get_text("text") or ""
            pages.append({
                "page_number": page_num,
                "text": page_text
            })
            if page_count > 1:
                full_text_parts.append(f"--- Page {page_num} ---\n{page_text}")
            else:
                full_text_parts.append(page_text)

        doc.close()
        full_text = "\n\n".join(full_text_parts)

        return ExtractedData(
            full_text=full_text,
            pages=pages,
            page_count=page_count if page_count > 0 else 1,
            status="SUCCESS"
        )
    except Exception as e:
        return ExtractedData(
            full_text="",
            pages=[],
            page_count=0,
            status="FAILED",
            error_message=f"PDF extraction failed: {str(e)}"
        )
