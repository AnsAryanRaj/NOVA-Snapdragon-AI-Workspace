"""Qualcomm AI Runtime REST API Endpoints."""

from fastapi import APIRouter
from app.qualcomm.schemas import (
    AIRuntimeStatus,
    InferenceRequestSpec,
    InferenceResponseSpec,
)
from app.qualcomm.adapter import qualcomm_adapter_manager

router = APIRouter(prefix="/ai", tags=["AI Runtime"])


@router.get("/runtime", response_model=AIRuntimeStatus)
def get_ai_runtime_status():
    """
    Returns truthful status of AI runtime engine and Qualcomm hardware detection.
    Secrets and tokens are strictly redacted or omitted.
    """
    return qualcomm_adapter_manager.get_runtime_status()


@router.post("/infer", response_model=InferenceResponseSpec)
def execute_ai_inference(request: InferenceRequestSpec):
    """
    Execute AI inference on active runtime provider or safe development fallback.
    """
    return qualcomm_adapter_manager.run_inference(request)
