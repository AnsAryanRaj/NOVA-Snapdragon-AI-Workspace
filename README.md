# NOVA — Privacy-First On-Device AI Workspace Assistant

> **A privacy-first AI workspace assistant designed for Windows and optimized for a future Snapdragon-powered deployment.**

NOVA is a local-first AI workspace assistant that helps users understand, search, and work with their files and documents through a controlled agent architecture.

Instead of giving an AI unrestricted access to the computer, NOVA places every operation behind a **Tool Registry → Safety Validation → Controlled Execution → Audit Log** pipeline.

The result is an AI workspace experience designed around **privacy, security, transparency, and user control**.

---

## Why NOVA?

Traditional AI assistants can require users to upload files or grant broad access to their computers.

NOVA takes a different approach:

- Files remain in the local workspace.
- Document processing is performed locally.
- AI actions are restricted to registered tools.
- Arbitrary shell or PowerShell execution is blocked.
- Workspace access is restricted to a controlled directory.
- Tool activity is recorded in a local audit trail.
- Snapdragon acceleration is isolated behind a dedicated runtime abstraction.

NOVA is therefore not designed as "just another chatbot".

The chat/command interface is an interaction layer over a controlled local workspace intelligence and agent system.

---

## Core Capabilities

### Workspace Intelligence

NOVA can safely inspect a configured local workspace and provide:

- File listing
- Workspace statistics
- File search
- File metadata
- SHA-256 file hashing
- Controlled text-file reading
- Canonical path validation
- Directory traversal protection

### Document Intelligence

The document subsystem supports deterministic local processing for formats including:

- `.txt`
- `.md`
- `.pdf`
- `.py`
- `.cpp`
- `.java`
- `.kt`
- `.ts`
- `.tsx`
- `.js`
- `.jsx`
- `.css`
- `.html`
- `.csv`
- `.json`
- `.xml`
- `.yaml`
- `.yml`

Documents are extracted locally, chunked deterministically, indexed in SQLite, and retrieved through lexical search.

PDF extraction includes page attribution.

### Controlled Agent

NOVA converts supported user requests into structured plans.

Example:

```text
User
 ↓
Agent Planner
 ↓
Tool Registry
 ↓
Safety Validation
 ↓
Controlled Tool Execution
 ↓
Result
 ↓
Audit Log