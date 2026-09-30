# NOVA — Privacy-First On-Device AI Workspace Assistant

**NOVA** is a production-quality, privacy-first, on-device AI workspace assistant built for the **Snapdragon AI Lab Build & Present Challenge**.

## Core Value

NOVA helps users understand and work with their local Windows workspace using controlled, privacy-first AI workflows directly on their device. Zero external cloud telemetry or arbitrary command execution.

---

## Current Verified Capabilities

- **Controlled Workspace Engine**: Scoped to `test_workspace` with canonical path boundary verification and directory tree traversal defense.
- **Document Intelligence**: Local document extraction for `.txt`, `.md`, `.pdf`, `.py`, `.ts`, `.kt`, `.java`, `.csv`, `.json` with token-aware chunking and page attribution.
- **Lexical Search Engine**: Ranked multi-term keyword search over indexed document chunks with scoring and contextual snippet generation.
- **Controlled Tool Registry**: Typed system action boundary supporting 12 read-only workspace & document tools. Zero arbitrary shell access.
- **Controlled Agent Foundation**: Deterministic intent planner mapping user requests (`SEARCH_DOCUMENTS`, `GET_DOCUMENT_CONTENT`, `SEARCH_AND_READ`, `WORKSPACE_SUMMARY`) to structured `AgentPlan` steps.
- **Safe Read-Only Execution**: Re-validates every plan step (`is_enabled`, `is_destructive=False`, `scope="test_workspace"`, path validation) before running.
- **Prompt Injection Defense**: Document text and metadata are handled strictly as untrusted data strings, preventing malicious content from altering security policies.
- **Local SQLite Audit Trail**: Every tool request, plan, step execution, and status outcome is recorded in SQLite (`audit_logs`).
- **Qualcomm AI Runtime Abstraction**: Hardware abstraction layer separating application logic from Snapdragon runtime acceleration (`qualcomm/`).

---

## Security Model

- **No Arbitrary Shell Execution**: `subprocess`, `os.system`, `os.popen`, `shell=True`, `Popen`, `cmd.exe`, and `powershell.exe` are hard-blocked and forbidden.
- **No Unrestricted Filesystem Access**: All file operations pass through canonical path validation (`path_security.py`) scoped exclusively to `test_workspace`.
- **No Admin Privileges**: Operates entirely within standard user permissions. Zero registry, service, Defender, or firewall modification.
- **Read-Only Tools Only**: Agent tool execution is strictly read-only. Creating, modifying, renaming, or deleting files is forbidden in this phase.
- **Untrusted Document Content**: Document text is isolated as plain data. Prompt injection strings cannot bypass security checks or trigger unauthorized actions.
- **Local-First Processing**: All indexing, planning, search, and retrieval execute 100% locally.

---

## Qualcomm / Snapdragon Statement

> Qualcomm/Snapdragon runtime integration is architected through a dedicated runtime abstraction. Snapdragon NPU execution and performance benchmarks are not claimed on the current x86_64 development machine and require validation on compatible Snapdragon hardware or Qualcomm-hosted profiling.

The system truthfully detects the host architecture (`capabilities.py`) and reports local CPU development fallback without fabricating TOPS or NPU metrics.

---

## Project Structure

```
Nova Snapdragon/
├── frontend/             # React + TypeScript + Vite + Tailwind CSS desktop app
│   ├── src/
│   │   ├── components/  # TitleBar, Sidebar, Card, Button, Badge, etc.
│   │   ├── views/       # Overview, Workspace, Documents, Vision, Voice, Activity, Performance, Settings
│   │   ├── types.ts     # TypeScript schemas
│   │   └── App.tsx      # Main application frame
│   └── vite.config.ts   # Vite configuration & backend proxy (/api)
├── backend/              # FastAPI + Python + SQLite core workspace engine
│   ├── app/
│   │   ├── agent/       # Phase 6 Controlled Agent Foundation (planner, executor, schemas)
│   │   ├── api/         # Routers for workspace, documents, qualcomm, agent, health
│   │   ├── core/        # Security policy enforcer & path security guard
│   │   ├── db/          # SQLite database connection & audit log models
│   │   ├── documents/   # Phase 4 Document Intelligence (extractor, chunker, index, service)
│   │   ├── tools/       # Tool Action Registry system (12 read-only tools)
│   │   ├── workspace/   # Phase 3 Real Workspace Engine (service, classifier, schemas)
│   │   └── main.py      # FastAPI application entrypoint
│   └── requirements.txt
├── qualcomm/             # Qualcomm AI Hub & Snapdragon NPU hardware abstraction layer
│   ├── adapter.py       # Hardware Abstraction Adapter with dev fallback
│   └── README.md        # NPU isolation boundary specification
├── docs/                 # Documentation & Architecture guides
│   ├── architecture.md
│   ├── agent_architecture.md
│   ├── document_intelligence.md
│   ├── workspace_engine.md
│   └── demo_script.md   # 2-3 minute presentation script
└── tests/                # 49 automated unit & integration tests
    └── backend/
        ├── test_agent.py
        ├── test_documents.py
        ├── test_health.py
        ├── test_qualcomm.py
        └── test_workspace.py
```

---

## Quick Start & Verification

### Running Backend Tests (49/49 Passing)
```powershell
$env:PYTHONPATH="backend"
.\backend\venv\Scripts\python -m pytest
```

### Running Frontend Build (0 Errors)
```powershell
cd frontend
npm run build
```

### Starting Local Backend Server
```powershell
$env:PYTHONPATH="backend"
.\backend\venv\Scripts\python -m uvicorn app.main:app --reload --port 8000
```
- Interactive API Docs: `http://127.0.0.1:8000/api/docs`
- Health Check: `http://127.0.0.1:8000/api/health`

### Starting Frontend Dev Application
```powershell
cd frontend
npm run dev
```
- Dev App URL: `http://localhost:5173`
