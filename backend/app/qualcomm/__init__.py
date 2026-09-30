"""Qualcomm AI Runtime & Hardware Integration Package for NOVA."""

from app.qualcomm.schemas import (
    AIRuntimeStatus,
    QualcommRuntimeInfo,
    ModelConfigSpec,
    InferenceRequestSpec,
    InferenceResponseSpec,
)
from app.qualcomm.capabilities import detect_system_capabilities
from app.qualcomm.adapter import qualcomm_adapter_manager

__all__ = [
    "AIRuntimeStatus",
    "QualcommRuntimeInfo",
    "ModelConfigSpec",
    "InferenceRequestSpec",
    "InferenceResponseSpec",
    "detect_system_capabilities",
    "qualcomm_adapter_manager",
]
