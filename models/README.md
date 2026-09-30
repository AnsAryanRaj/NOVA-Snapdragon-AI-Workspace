# NOVA Model Storage & Local Weights Directory

This directory serves as the local storage location for privacy-first, on-device AI models utilized by NOVA.

## Planned Local Model Layout

```
models/
├── llm/                # Local Large Language Model weights (GGUF / ONNX / safetensors)
├── whisper/            # Whisper speech recognition model weights
├── vision/             # Local Vision-Language Model weights
└── qualcomm_quantized/ # QNN/GenieX compiled model context binaries for Snapdragon NPU
```

## Architectural Guarantee

1. **Offline & Privacy-First**: Models run strictly locally on device. No context data leaves the local machine.
2. **Qualcomm NPU Hardware Isolation**: Compiled Qualcomm QNN models and GenieX runtime engine bindings reside in `qualcomm/` and connect to backend services via standard hardware abstraction interfaces.
3. **Local Development Fallback**: If a Snapdragon NPU or GenieX engine is unavailable during local development, the backend cleanly defaults to CPU/GPU fallback without breaking application execution.
