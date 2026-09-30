# Qualcomm Snapdragon NPU Isolation Module

This directory contains the **Hardware Abstraction Layer (HAL)** for Qualcomm AI Hub and GenieX engine integration on Snapdragon devices.

## Architectural Isolation Principles

1. **Strict Decoupling**: Core workspace processing, document indexing, safety verification, and tool dispatch logic must NEVER directly depend on Qualcomm-specific C++ / Python SDK binaries.
2. **Interface Abstraction**: Hardware acceleration is accessed exclusively via the abstract `QualcommNPUAdapter` interface.
3. **Local Development Fallback**: If GenieX or Snapdragon NPU drivers are missing (e.g., developing on x86_64 host machines or non-Snapdragon platforms), `QualcommNPUAdapter` automatically operates in `ISOLATED_FALLBACK` mode. The rest of NOVA continues functioning without error.
4. **Zero Metrics Fabrication**: Real-world NPU latency, memory bandwidth, and TOPS (Tera Operations Per Second) are reported ONLY when physical execution occurs on Snapdragon NPU hardware.

## Directory Structure

```
qualcomm/
├── README.md            # Architectural specification
├── adapter.py           # Hardware abstraction layer & fallback interface
└── genie_bindings/     # (Future) GenieX and Snapdragon NPU execution bindings
```
