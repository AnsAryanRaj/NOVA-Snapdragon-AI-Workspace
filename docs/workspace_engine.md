# NOVA Workspace Intelligence Engine

## Overview

The NOVA Workspace Engine provides a secure, deterministic filesystem intelligence foundation for the NOVA Privacy-First On-Device AI Assistant.

All workspace operations are strictly scoped to the configured development workspace (`D:\Nova Snapdragon\test_workspace`) and validated using canonical resolved paths before execution.

---

## Security Boundary & Path Protection

### 1. Controlled Workspace Root
The workspace root directory is defined strictly on the server configuration (`app/core/config.py`):
```python
WORKSPACE_ROOT = "D:\\Nova Snapdragon\\test_workspace"
```
The client is **never allowed** to alter the workspace root or supply arbitrary system paths.

### 2. Path Validation Pipeline (`app/core/path_security.py`)
All incoming file paths pass through `validate_workspace_path(relative_path)`:

1. **Null Byte Filter**: Rejects paths containing `\x00` characters.
2. **UNC Path Block**: Rejects network share paths (`\\server\share` or `//server/share`).
3. **Drive Letter Escape Rejection**: Rejects client attempts to specify raw Windows drive letters (`C:`, `D:`, `E:`).
4. **Canonical Path Resolution**: Joins input with `WORKSPACE_ROOT` and resolves to absolute path via `Path.resolve()`.
5. **Containment Verification**: Verifies `candidate_path.relative_to(workspace_root)` succeeds. If the path escapes the workspace root (e.g. via `../` or `..\` traversal or symlink escapes), a `400 Bad Request` security violation error is raised.

---

## Supported Workspace Operations

### 1. Directory Listing
- Endpoint: `GET /api/v1/workspace/files?path=`
- Returns immediate file and directory schemas (`name`, `relative_path`, `item_type`, `size_bytes`, `modified_time`, `extension`, `category`).

### 2. Workspace Search
- Endpoint: `GET /api/v1/workspace/search?q=`
- Scans `test_workspace` recursively for matching filenames, extensions, or relative paths.

### 3. File Metadata
- Endpoint: `GET /api/v1/workspace/metadata?path=`
- Returns metadata including created time, modified time, size, item type, and category.

### 4. Streaming SHA-256 Checksum
- Endpoint: `GET /api/v1/workspace/hash?path=`
- Calculates SHA-256 hashes using a 64 KB streaming chunk buffer to prevent high memory usage.

### 5. Safe Text Content Reader
- Endpoint: `GET /api/v1/workspace/content?path=`
- Allowed Extensions: `.txt`, `.md`, `.csv`, `.json`, `.py`, `.cpp`, `.h`, `.hpp`, `.ts`, `.tsx`, `.js`, `.jsx`, `.css`, `.html`, `.yaml`, `.yml`, `.xml`.
- Rejects binary/unsupported file types with a structured error.
- Enforces `MAX_TEXT_READ_BYTES = 2,000,000` (2 MB).

### 6. Workspace Summary Statistics
- Endpoint: `GET /api/v1/workspace/stats`
- Calculates totals for files, directories, size, categories (Code, Document, Data, Image, Other), and lists recent files.

---

## File Categories

Deterministic extension classification:
- **Code**: `.py`, `.cpp`, `.h`, `.hpp`, `.js`, `.jsx`, `.ts`, `.tsx`, `.java`, `.kt`, `.css`, `.html`
- **Document**: `.txt`, `.md`, `.pdf`, `.doc`, `.docx`, `.rtf`
- **Data**: `.csv`, `.json`, `.xml`, `.yaml`, `.yml`, `.xlsx`
- **Image**: `.png`, `.jpg`, `.jpeg`, `.webp`, `.gif`, `.bmp`, `.tiff`
- **Other**: Everything else

---

## Tool Registry Integration

All Phase 3 capabilities are registered as read-only tools in the central `ToolRegistry`:
- `workspace.list_files`
- `workspace.search_files`
- `workspace.get_metadata`
- `workspace.get_hash`
- `workspace.read_text`
- `workspace.get_stats`

Each tool is declared with:
- `is_destructive`: `False`
- `requires_confirmation`: `False`
- `scope`: `"test_workspace"`
- `risk_level`: `"low"`

---

## Future AI Integration Point

Future NOVA AI components (Local LLM, Qualcomm AI Hub models, GenieX runtime, Agent Planner) will invoke filesystem operations exclusively through the Tool Registry and Path Security validator:

```
User Prompt
   ↓
NOVA Agent Planner / LLM
   ↓
Tool Registry (`workspace.read_text`, `workspace.search_files`)
   ↓
Path Security Validation (`validate_workspace_path`)
   ↓
Workspace Service Layer (`test_workspace/`)
```
No shell execution or arbitrary OS commands are permitted.
