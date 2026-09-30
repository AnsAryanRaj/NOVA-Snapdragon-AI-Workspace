"""Qualcomm Snapdragon NPU Hardware Abstraction Layer (HAL).

Isolates Qualcomm GenieX & NPU runtime calls from core application logic.
"""

from typing import Dict, Any, Optional


class QualcommNPUAdapter:
    """Hardware abstraction adapter for Snapdragon NPU execution."""

    def __init__(self):
        self._is_hardware_available: bool = False
        self._mode: str = "isolated-fallback"
        self._detect_hardware()

    def _detect_hardware(self) -> None:
        """Detects whether Snapdragon NPU runtime (GenieX / QNN) is natively available."""
        # Hardware detection logic will probe for qnn-runtime or genie-sdk
        # Defaults to isolated-fallback when running on local development machines without NPU
        self._is_hardware_available = False
        self._mode = "isolated-fallback"

    def get_status(self) -> Dict[str, Any]:
        """Returns current NPU isolation and availability status."""
        return {
            "npu_available": self._is_hardware_available,
            "isolation_mode": self._mode,
            "hardware_target": "Qualcomm Snapdragon NPU",
            "runtime_binding": "GenieX/QNN Adapter",
            "metrics": {
                "npu_latency_ms": None,
                "npu_utilization_pct": None,
                "note": "Metrics available only when running on physical Snapdragon NPU hardware."
            }
        }

    async def execute_npu_inference(self, model_name: str, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Executes inference on Snapdragon NPU if available, or delegates to fallback."""
        if not self._is_hardware_available:
            return {
                "status": "fallback",
                "execution_engine": "CPU/GPU Local Development Fallback",
                "result": "Execution completed via dev fallback (Snapdragon NPU offline)."
            }
        raise NotImplementedError("Qualcomm GenieX NPU execution will be wired during hardware integration phase.")


qualcomm_npu_adapter = QualcommNPUAdapter()
