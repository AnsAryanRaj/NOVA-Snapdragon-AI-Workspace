# Document & Semantic Intelligence Foundation (Phase 4)

## Architecture Overview

Phase 4 introduces a real, local Document Intelligence and Semantic Retrieval baseline for NOVA, operating on top of the Phase 3 Workspace Engine.

All text extraction, document parsing, chunking, indexing, and search processes run 100% on-device with zero cloud AI API dependencies.

---

## 1. Supported Document & Text Formats

| Category | File Extensions | Extractor Engine |
| :--- | :--- | :--- |
| **PDF Documents** | `.pdf` | Local PyMuPDF (`fitz`) text page extraction |
| **Markdown & Notes** | `.md`, `.txt`, `.rst`, `.org` | Local UTF-8 text reader with encoding fallback |
| **Source Code** | `.py`, `.js`, `.ts`, `.tsx`, `.jsx`, `.cpp`, `.c`, `.h`, `.hpp`, `.cs`, `.java`, `.kt`, `.go`, `.rs`, `.html`, `.css`, `.sql` | UTF-8 code parser |
| **Structured Formats** | `.json`, `.jsonl`, `.csv`, `.tsv`, `.yaml`, `.yml`, `.toml`, `.ini`, `.env`, `.log` | Structured text parser |

---

## 2. Text Extraction & Chunking Strategy

- **Document Identifiers**: Stable deterministic `doc_id` generated via `sha256(f"{relative_path.lower()}:{content_hash}")`.
- **Target Chunk Size**: 800 - 1200 characters per chunk (default `1000` chars).
- **Chunk Overlap**: 100 - 200 characters (default `150` chars) to preserve context across boundaries.
- **Natural Boundary Detection**: Respects double newlines (`\n\n`), single newlines (`\n`), sentence periods (`. `), and spaces (` `).
- **Multi-page Attribution**: Tracks page numbers (`page_number`) for PDFs and multi-page formats.
- **Token Estimation**: Computes approximate token count per chunk.

---

## 3. SQLite Database Schema

```
+-------------------------------------------------------+
|                       documents                       |
+-------------------------------------------------------+
| id (VARCHAR 64, PK)                                   |
| relative_path (VARCHAR 500, UNIQUE, INDEX)            |
| file_name (VARCHAR 255, INDEX)                        |
| file_extension (VARCHAR 20)                           |
| mime_type (VARCHAR 100)                               |
| size_bytes (INTEGER)                                  |
| content_hash (VARCHAR 64)                             |
| page_count (INTEGER)                                  |
| chunk_count (INTEGER)                                 |
| indexed_at (DATETIME)                                 |
| last_modified (DATETIME)                              |
| extraction_status (VARCHAR 50)                        |
| error_message (TEXT)                                  |
+-------------------------------------------------------+
                           | 1
                           |
                           | N
+-------------------------------------------------------+
|                    document_chunks                    |
+-------------------------------------------------------+
| id (INTEGER, PK, AUTOINCREMENT)                       |
| chunk_id (VARCHAR 100, UNIQUE, INDEX)                 |
| doc_id (VARCHAR 64, FK -> documents.id, INDEX)        |
| chunk_index (INTEGER)                                 |
| content (TEXT)                                        |
| start_char (INTEGER)                                  |
| end_char (INTEGER)                                    |
| page_number (INTEGER)                                 |
| token_count (INTEGER)                                 |
| created_at (DATETIME)                                 |
+-------------------------------------------------------+
```

---

## 4. Incremental Indexing Engine

1. Scans target directory inside `test_workspace` using `validate_workspace_path`.
2. Computes `sha256` content hash for each candidate file.
3. Compares with DB records:
   - **Unchanged**: Skips re-extraction and re-chunking.
   - **Modified**: Deletes stale chunks and updates database record with version-safe content `doc_id`.
   - **New**: Extracts text, chunks content, and inserts into SQLite.
4. **Pruning**: Deletes stale DB records for files removed from disk.

---

## 5. Lexical Retrieval & Search Baseline

- Endpoint: `GET /api/v1/documents/search?q={query}`
- Performs term-frequency keyword matching across indexed document chunks.
- Computes relevance score:
  \[
  \text{Score} = \text{TermFreq} + \text{TitleBonus}(3.0) + \text{PathBonus}(1.5) + \text{CoverageScore}(5.0)
  \]
- Returns ranked matches with contextual snippets and page/chunk attribution.

---

## 6. REST API Endpoints

1. `GET /api/v1/documents`: List indexed workspace documents.
2. `GET /api/v1/documents/{document_id}`: Retrieve document metadata and chunks.
3. `GET /api/v1/documents/{document_id}/content`: Retrieve extracted text content and chunks safely.
4. `GET /api/v1/documents/search?q=`: Search indexed document chunks.
5. `POST /api/v1/documents/index`: Trigger incremental workspace indexing.
6. `GET /api/v1/documents/stats`: Get document index statistics.

---

## 7. Registered Document Tools (`ToolRegistry`)

1. `document.list`: List indexed workspace documents.
2. `document.get_metadata`: Get metadata for a document by path or ID.
3. `document.get_content`: Get extracted text content and chunks for a document.
4. `document.search`: Search workspace documents by keyword query.
5. `document.index`: Index/reindex workspace documents.
6. `document.get_stats`: Get document index statistics.

All 6 tools are registered as `is_destructive=False`, `requires_confirmation=False`, and strictly bound to `test_workspace`.
