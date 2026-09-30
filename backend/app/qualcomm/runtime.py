"""Runtime provider abstractions for Development Fallback and Qualcomm AI Runtime."""

from abc import ABC, abstractmethod
import time
from typing import Dict, Any, Optional

from app.core.config import settings
from app.qualcomm.capabilities import detect_system_capabilities
from app.qualcomm.schemas import (
    InferenceRequestSpec,
    InferenceResponseSpec,
    QualcommRuntimeInfo
)


class BaseAIRuntime(ABC):
    """Abstract base class for all AI runtime providers."""

    @abstractmethod
    def is_available(self) -> bool:
        """Check if runtime environment is available."""
        pass

    @abstractmethod
    def get_provider_name(self) -> str:
        """Return provider identifier (e.g. 'local', 'qualcomm')."""
        pass

    @abstractmethod
    def get_runtime_name(self) -> str:
        """Return runtime identifier (e.g. 'development', 'geniex', 'qairt')."""
        pass

    @abstractmethod
    def run_inference(self, request: InferenceRequestSpec) -> InferenceResponseSpec:
        """Execute inference or safe fallback response."""
        pass


class DevelopmentRuntime(BaseAIRuntime):
    """Local development runtime fallback when Snapdragon hardware is not present."""

    def is_available(self) -> bool:
        return True

    def get_provider_name(self) -> str:
        return "local"

    def get_runtime_name(self) -> str:
        return "development"

    def run_inference(self, request: InferenceRequestSpec) -> InferenceResponseSpec:
        start_time = time.time()
        # Truthful local fallback response
        response_text = (
            f"[Development Runtime Fallback] Prompt received ({len(request.prompt)} chars). "
            f"Local CPU inference placeholder."
        )
        latency = (time.time() - start_time) * 1000.0

        return InferenceResponseSpec(
            response_text=response_text,
            model=request.model or settings.QUALCOMM_MODEL,
            compute_unit_used="CPU",
            latency_ms=round(latency, 2),
            is_fallback=True
        )


class QualcommAIRuntime(BaseAIRuntime):
    """Qualcomm AI Hub & GenieX Runtime Adapter."""

    def __init__(self):
        self._sdk_available = False
        self._check_sdk_availability()

    def _check_sdk_availability(self):
        """Safely attempt loading optional Qualcomm SDK packages without breaking startup."""
        if not settings.QUALCOMM_ENABLED:
            self._sdk_available = False
            return

        try:
            # Check for hypothetical optional Qualcomm SDK imports
            import qai_hub  # type: ignore # noqa: F401
            self._sdk_available = True
        except ImportError:
            self._sdk_available = False

    def is_available(self) -> bool:
        caps = detect_system_capabilities()
        return settings.QUALCOMM_ENABLED and caps.is_snapdragon_hardware and self._sdk_available

    def get_provider_name(self) -> str:
        return "qualcomm"

    def get_runtime_name(self) -> str:
        return settings.QUALCOMM_RUNTIME

    def get_qualcomm_info(self) -> QualcommRuntimeInfo:
        caps = detect_system_capabilities()

        if not settings.QUALCOMM_ENABLED:
            reason = "Qualcomm runtime disabled in application configuration (QUALCOMM_ENABLED=false)"
        elif not caps.is_snapdragon_hardware:
            reason = "Snapdragon runtime is not available on this development machine"
        elif not self._sdk_available:
            reason = "Qualcomm AI Hub / GenieX SDK packages are not installed in the local Python environment"
        else:
            reason = "Qualcomm AI Runtime active and ready"

        return QualcommRuntimeInfo(
            available=self.is_available(),
            runtime=settings.QUALCOMM_RUNTIME,
            reason=reason,
            compute_unit="NPU" if self.is_available() else "CPU",
            has_api_token=bool(settings.QUALCOMM_API_TOKEN),
            redacted_token=settings.get_redacted_qualcomm_token()
        )

    def run_inference(self, request: InferenceRequestSpec) -> InferenceResponseSpec:
        if not self.is_available():
            info = self.get_qualcomm_info()
            return InferenceResponseSpec(
                response_text="",
                model=request.model or settings.QUALCOMM_MODEL,
                compute_unit_used="N/A",
                latency_ms=0.0,
                is_fallback=True,
                error_message=f"Qualcomm runtime unavailable: {info.reason}"
            )

        start_time = time.time()
        # Placeholder for actual hardware execution when running on Snapdragon device with SDK
        response_text = f"[Snapdragon NPU Execution] Executed prompt for {request.model}"
        latency = (time.time() - start_time) * 1000.0

        return InferenceResponseSpec(
            response_text=response_text,
            model=request.model or settings.QUALCOMM_MODEL,
            compute_unit_used="NPU",
            latency_ms=round(latency, 2),
            is_fallback=False
        )
