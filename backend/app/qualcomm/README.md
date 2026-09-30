# Qualcomm AI Runtime & Hardware Foundation (Phase 5)

## Overview

The `app.qualcomm` package provides a safe, modular runtime abstraction layer for NOVA.

It decouples core application logic from hardware-specific AI runtimes, allowing NOVA to run seamlessly on standard development machines (via Development Fallback Runtime) while preparing an isolated integration path for Qualcomm AI Hub, GenieX, and Qualcomm AI Runtime (QAIRT) on Snapdragon hardware.

---

## Architecture

```
                       +-------------------------------+
                       |       NOVA AI Interface       |
                       +---------------+---------------+
                                       |
                                       v
                       +---------------+---------------+
                       |    QualcommAdapterManager     |
                       +---------------+---------------+
                                       |
                   +-------------------+-------------------+
                   |                                       |
                   v                                       v
     +---------------------------+           +---------------------------+
     |   DevelopmentRuntime      |           |    QualcommAIRuntime      |
     |   (CPU / Dev Fallback)    |           |    (GenieX / QAIRT NPU)    |
     +---------------------------+           +---------------------------+
```

---

## Principles & Benchmark Standards

1. **Truthful Hardware Detection**: The system safely inspects host architecture (`capabilities.py`) without assuming Snapdragon hardware on x86_64 development PCs.
2. **Zero Fake Metrics**: Non-Snapdragon development machines report `available=False` for Qualcomm hardware with a truthful reason string. No simulated NPU %, fake TOPS, or fake Snapdragon latency metrics are emitted.
3. **Secret Redaction**: API tokens (`QUALCOMM_API_TOKEN`) are automatically redacted in responses and logs.
4. **Optional Dependency Safety**: Missing optional Qualcomm packages (e.g., `qai_hub`) do not break application startup or test suites.

---

## Environment Configuration

Configuration variables managed via `app.core.config.Settings`:

| Variable | Default | Description |
| :--- | :--- | :--- |
| `QUALCOMM_ENABLED` | `False` | Toggle Qualcomm AI runtime integration |
| `QUALCOMM_RUNTIME` | `"auto"` | Target runtime (`"auto"`, `"geniex"`, `"qairt"`, `"disabled"`) |
| `QUALCOMM_MODEL` | `"qcom/llama-3-8b-instruct"` | Target Qualcomm AI Hub model identifier |
| `QUALCOMM_API_TOKEN` | `""` | Optional Qualcomm API token (redacted in output) |

---

## REST API Endpoints

- `GET /api/v1/ai/runtime`: Returns truthful AI runtime engine status and system capabilities.
- `POST /api/v1/ai/infer`: Submits an inference request to the active runtime provider.
