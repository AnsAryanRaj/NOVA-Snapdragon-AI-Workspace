"""Deterministic text chunker supporting page attribution and overlap."""

from typing import List, Dict, Any
from app.documents.extractor import ExtractedData


class ChunkData:
    def __init__(
        self,
        chunk_index: int,
        content: str,
        start_char: int,
        end_char: int,
        page_number: int = 1,
        token_count: int = 0
    ):
        self.chunk_index = chunk_index
        self.content = content
        self.start_char = start_char
        self.end_char = end_char
        self.page_number = page_number
        self.token_count = token_count or max(1, len(content.split()))


def chunk_extracted_data(
    extracted: ExtractedData,
    target_chunk_size: int = 1000,
    chunk_overlap: int = 150
) -> List[ChunkData]:
    """
    Split ExtractedData into overlapping text chunks.
    Preserves page attribution for multi-page documents (PDFs).
    """
    if not extracted.full_text or extracted.status == "FAILED":
        return []

    chunks: List[ChunkData] = []
    chunk_idx = 0

    if len(extracted.pages) > 1:
        # Multi-page extraction (e.g. PDF)
        global_char_offset = 0
        for page in extracted.pages:
            page_num = page.get("page_number", 1)
            page_text = page.get("text", "")
            if not page_text.strip():
                continue

            page_chunks = _split_text_into_chunks(
                text=page_text,
                target_size=target_chunk_size,
                overlap=chunk_overlap,
                page_number=page_num,
                start_index=chunk_idx,
                base_char_offset=global_char_offset
            )
            chunks.extend(page_chunks)
            chunk_idx += len(page_chunks)
            global_char_offset += len(page_text) + 2  # account for page separators
    else:
        # Single-page text/code document
        text = extracted.full_text
        chunks = _split_text_into_chunks(
            text=text,
            target_size=target_chunk_size,
            overlap=chunk_overlap,
            page_number=1,
            start_index=0,
            base_char_offset=0
        )

    return chunks


def _split_text_into_chunks(
    text: str,
    target_size: int,
    overlap: int,
    page_number: int,
    start_index: int,
    base_char_offset: int
) -> List[ChunkData]:
    """Split a block of text into chunks with smart boundary detection."""
    if not text.strip():
        return []

    if len(text) <= target_size:
        return [
            ChunkData(
                chunk_index=start_index,
                content=text,
                start_char=base_char_offset,
                end_char=base_char_offset + len(text),
                page_number=page_number,
                token_count=len(text.split())
            )
        ]

    chunks: List[ChunkData] = []
    start = 0
    text_len = len(text)
    current_index = start_index

    step = max(200, target_size - overlap)

    while start < text_len:
        end = min(start + target_size, text_len)

        # If not at the end of text, try to find a natural boundary
        if end < text_len:
            # Look for double newline, single newline, or space near end
            break_point = _find_natural_break(text, end, search_window=100)
            if break_point > start + 200:
                end = break_point

        chunk_text = text[start:end]
        if chunk_text.strip():
            chunks.append(
                ChunkData(
                    chunk_index=current_index,
                    content=chunk_text,
                    start_char=base_char_offset + start,
                    end_char=base_char_offset + end,
                    page_number=page_number,
                    token_count=len(chunk_text.split())
                )
            )
            current_index += 1

        if end >= text_len:
            break

        start += step

    return chunks


def _find_natural_break(text: str, target_pos: int, search_window: int = 100) -> int:
    """Find natural breakpoint (paragraph, newline, period, space) near target_pos."""
    window_start = max(0, target_pos - search_window)
    window_end = min(len(text), target_pos + search_window)
    search_sub = text[window_start:window_end]

    # Try paragraph break
    para_break = search_sub.rfind("\n\n")
    if para_break != -1:
        return window_start + para_break + 2

    # Try line break
    line_break = search_sub.rfind("\n")
    if line_break != -1:
        return window_start + line_break + 1

    # Try sentence boundary
    period_break = search_sub.rfind(". ")
    if period_break != -1:
        return window_start + period_break + 2

    # Try space boundary
    space_break = search_sub.rfind(" ")
    if space_break != -1:
        return window_start + space_break + 1

    return target_pos
