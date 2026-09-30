"""Qualcomm Adapter Manager providing unified runtime selection and capability reporting."""

from typing import Dict, Any, Optional
from app.core.config import settings
from app.qualcomm.capabilities import detect_system_capabilities
from app.qualcomm.schemas import (
    AIRuntimeStatus,
    ModelConfigSpec,
    InferenceRequestSpec,
    InferenceResponseSpec,
)
from app.qualcomm.runtime import DevelopmentRuntime, QualcommAIRuntime


class QualcommAdapterManager:
    """Central manager coordinating AI Runtimes and hardware abstraction."""

    def __init__(self):
        self.dev_runtime = DevelopmentRuntime()
        self.qualcomm_runtime = QualcommAIRuntime()

    def get_active_model_config(self) -> ModelConfigSpec:
        """Returns the active model specification."""
        is_qualcomm_active = self.qualcomm_runtime.is_available()
        return ModelConfigSpec(
            name=settings.QUALCOMM_MODEL,
            provider="Qualcomm AI Hub" if is_qualcomm_active else "Local Development Hub",
            runtime=settings.QUALCOMM_RUNTIME if is_qualcomm_active else "Development Fallback",
            modality="text",
            precision="INT4",
            quantization="w4a16",
            target_compute_unit="NPU" if is_qualcomm_active else "CPU",
            is_verified=is_qualcomm_active
        )

    def get_runtime_status(self) -> AIRuntimeStatus:
        """
        Returns complete, truthful runtime status for API clients and UI.
        Redacts sensitive tokens and reports accurate capability state.
        """
        caps = detect_system_capabilities()
        q_info = self.qualcomm_runtime.get_qualcomm_info()
        active_model = self.get_active_model_config()

        if q_info.available:
            provider_name = "qualcomm"
            runtime_name = settings.QUALCOMM_RUNTIME
            device_name = "Snapdragon NPU / Qualcomm AI Engine"
        else:
            provider_name = "local"
            runtime_name = "development"
            device_name = f"Development Host ({caps.processor})"

        return AIRuntimeStatus(
            provider=provider_name,
            runtime=runtime_name,
            available=True,  # Overall system available via dev fallback or Qualcomm
            device=device_name,
            qualcomm=q_info,
            active_model=active_model,
            capabilities=caps
        )

    def run_inference(self, request: InferenceRequestSpec) -> InferenceResponseSpec:
        """Dispatch inference request to active runtime or safe fallback."""
        if self.qualcomm_runtime.is_available():
            return self.qualcomm_runtime.run_inference(request)
        return self.dev_runtime.run_inference(request)


# Singleton instance
qualcomm_adapter_manager = QualcommAdapterManager()
