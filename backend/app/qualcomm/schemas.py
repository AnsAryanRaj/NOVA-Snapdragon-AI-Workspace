"""Pydantic schemas for Qualcomm AI Runtime abstraction."""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, ConfigDict


class ModelConfigSpec(BaseModel):
    """Specification for AI model configuration."""
    name: str = "qcom/llama-3-8b-instruct"
    provider: str = "Qualcomm AI Hub"
    runtime: str = "GenieX / QAIRT"
    modality: str = "text"
    precision: str = "INT4"
    quantization: str = "w4a16"
    target_compute_unit: str = "NPU"
    is_verified: bool = False

    model_config = ConfigDict(from_attributes=True)


class InferenceRequestSpec(BaseModel):
    """Specification for an AI inference request."""
    prompt: str
    max_tokens: int = 512
    temperature: float = 0.7
    model: Optional[str] = None


class InferenceResponseSpec(BaseModel):
    """Specification for an AI inference response."""
    response_text: str
    model: str
    compute_unit_used: str
    latency_ms: float
    is_fallback: bool = True
    error_message: Optional[str] = None


class SystemCapabilitiesSpec(BaseModel):
    """Hardware and OS capability detection results."""
    os_name: str
    processor: str
    architecture: str
    is_snapdragon_hardware: bool
    available_compute_units: List[str]


class QualcommRuntimeInfo(BaseModel):
    """Status details for Qualcomm hardware/runtime."""
    available: bool
    runtime: str = "geniex"
    reason: str
    compute_unit: str = "CPU"
    has_api_token: bool = False
    redacted_token: str = ""


class AIRuntimeStatus(BaseModel):
    """Root AI Runtime Status response for GET /api/v1/ai/runtime."""
    provider: str
    runtime: str
    available: bool
    device: str
    qualcomm: QualcommRuntimeInfo
    active_model: ModelConfigSpec
    capabilities: SystemCapabilitiesSpec

    model_config = ConfigDict(from_attributes=True)
