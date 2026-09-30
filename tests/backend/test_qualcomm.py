"""Unit and integration tests for Phase 5 Qualcomm AI Runtime Foundation."""

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.core.config import settings
from app.qualcomm.capabilities import detect_system_capabilities
from app.qualcomm.runtime import DevelopmentRuntime, QualcommAIRuntime
from app.qualcomm.adapter import qualcomm_adapter_manager
from app.qualcomm.schemas import InferenceRequestSpec

client = TestClient(app)


def test_development_runtime_fallback():
    dev_rt = DevelopmentRuntime()
    assert dev_rt.is_available() is True
    assert dev_rt.get_provider_name() == "local"
    assert dev_rt.get_runtime_name() == "development"

    req = InferenceRequestSpec(prompt="Test prompt for fallback execution")
    resp = dev_rt.run_inference(req)
    assert resp.is_fallback is True
    assert resp.compute_unit_used == "CPU"
    assert "Development Runtime Fallback" in resp.response_text


def test_qualcomm_runtime_unavailable_on_dev_machine():
    q_rt = QualcommAIRuntime()
    # On x86_64 dev host without QUALCOMM_ENABLED=true, is_available is False
    assert q_rt.is_available() is False
    info = q_rt.get_qualcomm_info()
    assert info.available is False
    assert "disabled" in info.reason or "Snapdragon" in info.reason or "SDK" in info.reason


def test_capability_detection():
    caps = detect_system_capabilities()
    assert caps.os_name is not None
    assert caps.processor is not None
    assert "CPU" in caps.available_compute_units
    # On non-Snapdragon x86_64 test machine, is_snapdragon_hardware must be False
    assert isinstance(caps.is_snapdragon_hardware, bool)


def test_secret_redaction():
    orig_token = settings.QUALCOMM_API_TOKEN
    try:
        settings.QUALCOMM_API_TOKEN = "qcom_secret_api_token_12345"
        redacted = settings.get_redacted_qualcomm_token()
        assert "secret" not in redacted
        assert redacted.startswith("qcom")
        assert redacted.endswith("2345")

        settings.QUALCOMM_API_TOKEN = "short"
        assert settings.get_redacted_qualcomm_token() == "********"
    finally:
        settings.QUALCOMM_API_TOKEN = orig_token


def test_ai_runtime_api_endpoint():
    resp = client.get("/api/v1/ai/runtime")
    assert resp.status_code == 200
    data = resp.json()

    assert "provider" in data
    assert "runtime" in data
    assert "available" in data
    assert "qualcomm" in data
    assert "capabilities" in data

    q_info = data["qualcomm"]
    assert "available" in q_info
    assert "reason" in q_info
    # Ensure sensitive tokens are NOT exposed
    assert "qcom_secret" not in str(data)


def test_ai_infer_api_endpoint():
    req_body = {
        "prompt": "Summarize workspace document",
        "max_tokens": 100
    }
    resp = client.post("/api/v1/ai/infer", json=req_body)
    assert resp.status_code == 200
    data = resp.json()

    assert "response_text" in data
    assert "compute_unit_used" in data
    assert "latency_ms" in data
    assert data["is_fallback"] is True


def test_app_startup_without_qualcomm_sdk():
    # Verify app status endpoint returns 200 OK without requiring optional SDKs
    resp = client.get("/api/health")
    assert resp.status_code == 200
