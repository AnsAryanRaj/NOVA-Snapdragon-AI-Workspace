# NOVA 2-Minute Presentation & Demo Script

## Overview

This script guides a 2 to 3-minute live presentation of **NOVA — Privacy-First On-Device AI Workspace Assistant**.

---

## Step-by-Step Presentation Flow

### STEP 1: Introduction & Overview (30 Seconds)
- **Action**: Open NOVA application on Overview screen (`http://localhost:5173`).
- **Presenter Statement**:
  > "NOVA is a privacy-first Windows workspace assistant designed around local processing and controlled actions. All document scanning, search, planning, and execution happen on-device without cloud telemetry or arbitrary command execution."

---

### STEP 2: Document Intelligence & Indexing (30 Seconds)
- **Action**: Click **Documents** tab in left navigation sidebar. Click **Index Workspace** button.
- **Presenter Statement**:
  > "NOVA's Document Engine automatically extracts and chunks local `.txt`, `.md`, `.pdf`, code files (`.py`, `.ts`, `.kt`, `.java`), and structured data (`.csv`, `.json`). Here we see indexed documents, page counts, and total chunks stored safely in local SQLite."

---

### STEP 3: Single-Step Agent Query (30 Seconds)
- **Action**: Return to **Overview** tab. Click suggested prompt pill: `"Find my project report"` (or type it into command bar and click **Run Agent**).
- **Presenter Statement**:
  > "When I request 'Find my project report', NOVA's deterministic planner parses the request, creates a safe read-only plan using `document.search`, re-validates tool safety, and retrieves matching document snippets instantly."

---

### STEP 4: Multi-Step Agent Search-and-Read (30 Seconds)
- **Action**: Click suggested prompt pill: `"Find my project report and show the contents"` (or type it into command bar and click **Run Agent**).
- **Presenter Statement**:
  > "For multi-step requests like 'Find my project report and show the contents', NOVA executes a 2-step workflow: first searching for matching documents, then deterministically selecting the top match to extract its full text content safely."

---

### STEP 5: AI Runtime & Qualcomm Truthfulness (20 Seconds)
- **Action**: Click **Performance** tab in left navigation sidebar.
- **Presenter Statement**:
  > "NOVA features a dedicated Qualcomm AI Runtime abstraction. Because we are demonstrating on an x86_64 development machine, the system truthfully reports local CPU development fallback without fabricating fake NPU TOPS or Snapdragon latency metrics."

---

### STEP 6: Security Boundary & Prompt-Injection Defense (20 Seconds)
- **Action**: Click **Activity** tab in left navigation sidebar.
- **Presenter Statement**:
  > "Security is strictly enforced. Arbitrary PowerShell or shell execution is hard-blocked. All workspace access passes through canonical path validation restricted to `test_workspace`. Furthermore, document content is treated strictly as untrusted data—so malicious text inside documents cannot execute shell commands or alter agent permissions."

---

### STEP 7: Audit Logging & Conclusion (10 Seconds)
- **Action**: Point out the live Activity Log.
- **Presenter Statement**:
  > "Every plan creation, tool authorization, and step result is recorded in an immutable local SQLite audit log. NOVA provides a robust, submission-ready foundation designed to transition seamlessly from local development to hardware-accelerated Snapdragon NPU execution."
