# NOVA System Architecture

## Overview

NOVA is a production-quality, privacy-first, on-device AI workspace assistant built for the Snapdragon AI Lab Build & Present Challenge.

NOVA is designed as a native Windows application that understands a user's local workspace and performs file, document, voice, vision, and system utility actions safely.

---

## High-Level Architecture Flow

```
User Request
     ↓
NOVA UI (React + TypeScript)
     ↓
Agent Planner (Deterministic Intents)
     ↓
Safety Validator (Read-Only & Path Guard)
     ↓
Tool Registry (Explicit Typed Actions)
     ↓
Workspace / Document Services
     ↓
SQLite / Local Workspace (test_workspace)
```

---

## AI Runtime Abstraction Hierarchy

```
NOVA AI Interface (BaseAIRuntime)
 ├── Development Runtime (Local CPU Fallback)
 └── Snapdragon Runtime (Hardware Acceleration)
       ├── GenieX Engine
       └── Qualcomm AI Runtime (QNN)
```

---

## Security & Execution Boundary

```
AI Intent / User Query
     ↓
Tool Registry Check (Is Tool Allowed & Enabled?)
     ↓
Safety Validator (Is Tool Read-Only & Scoped to test_workspace?)
     ↓
User Confirmation Check (If Required)
     ↓
Tool Runner (Executes Typed Handler)
     ↓
Local Workspace Access
     ↓
SQLite Audit Trail Logging
```

---

## Core Security & Privacy Principles

### 1. Privacy-First & Offline-First
All workspace indexing, prompt evaluation, document scanning, and user interactions remain strictly on-device. Zero telemetry or user workspace context is transmitted over external networks.

### 2. No Unrestricted System Access
Arbitrary shell command execution (PowerShell / CMD) is hard-blocked at the system security layer. The assistant cannot construct or invoke arbitrary terminal scripts.

### 3. Explicit Tool Registry & Path Security
Every interaction with the local filesystem must pass canonical path validation (`app/core/path_security.py`) restricted to `test_workspace` and execute via typed read-only tool handlers in `app/tools/registry.py`.

### 4. Mandatory User Confirmation & Read-Only Constraint
All agent tool actions are strictly read-only (`is_destructive=False`). Writing, deleting, moving, or modifying files is disabled.

### 5. Immutable Audit Trail & SQLite Index
Every tool invocation request, authorization check, user decision, latency metric, and status outcome is recorded in an SQLite database table (`audit_logs`). Document metadata and extracted chunks are stored in `documents` and `document_chunks` tables.

### 6. Phase 4 Document & Semantic Intelligence Foundation
- **Local Extraction**: Supports `.txt`, `.md`, source code (`.py`, `.ts`, `.cpp`, `.java`, `.kt`), structured data (`.csv`, `.json`), and `.pdf` via PyMuPDF (`fitz`).
- **Deterministic Chunker**: Splits document text into overlapping chunks (800–1200 characters, 100–200 overlap) with page and line attribution.
- **Incremental Indexer**: Tracks `content_hash` (`sha256`), skipping unchanged files and pruning deleted records.
- **Lexical Search Engine**: Scores and ranks document chunks based on term frequency, title relevance, and snippet proximity.

### 7. Phase 5 Qualcomm AI Runtime Foundation & Isolation
- **Runtime Abstraction**: Decouples application code from hardware bindings via `BaseAIRuntime`, `DevelopmentRuntime`, and `QualcommAIRuntime`.
- **Truthful Capability Detection**: Safely detects host OS, architecture, and processor (`capabilities.py`) without assuming Snapdragon hardware on x86_64 development PCs.
- **Safe Development Fallback**: On non-Snapdragon machines, NOVA reports `available=False` for Qualcomm hardware with a truthful reason string and falls back to local CPU execution.
- **Secret Redaction**: Sensitive API tokens (`QUALCOMM_API_TOKEN`) are automatically redacted in responses and logs.

### 8. Phase 6 Controlled Agent Foundation
- **Deterministic Agent Planner**: Parses user requests into structured `AgentPlan` objects with explicit intents (`SEARCH_DOCUMENTS`, `GET_DOCUMENT_CONTENT`, `SEARCH_AND_READ`, `WORKSPACE_SUMMARY`, etc.) without requiring a cloud LLM.
- **Safe Read-Only Executor**: Re-validates every plan step against `ToolRegistry` (`is_enabled`, `is_destructive=False`, `scope="test_workspace"`) and canonical path boundary rules before execution.
- **Multi-Step Workflows**: Supports multi-step search-and-read workflows (`document.search` -> top match resolution -> `document.get_content`).
- **Prompt Injection Defense**: Document text and metadata are handled as untrusted string data, ensuring document content cannot alter tool policies or execute system commands.
- **REST Endpoints**: Exposes `POST /api/v1/agent/plan`, `POST /api/v1/agent/execute`, and `POST /api/v1/agent/run`.
