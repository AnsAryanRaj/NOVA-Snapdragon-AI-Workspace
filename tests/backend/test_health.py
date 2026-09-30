"""Unit tests for Backend Health API Endpoint."""

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health_check_endpoint():
    """Test GET /api/health returns 200 OK and expected structure."""
    response = client.get("/api/health")
    assert response.status_code == 200
    
    data = response.json()
    assert data["status"] == "ok"
    assert data["service"] == "NOVA Workspace Assistant"
    assert data["version"] == "0.1.0"
    assert data["privacy_mode"] == "offline-strict"
    assert data["qualcomm_isolation"] == "isolated-fallback"
    assert "security_policy" in data
    
    sec_policy = data["security_policy"]
    assert sec_policy["shell_execution_blocked"] is True
    assert sec_policy["tool_registry_enforced"] is True
    assert sec_policy["user_confirmation_required"] is True
    assert sec_policy["audit_logging_active"] is True


def test_root_endpoint():
    """Test GET / returns welcome message."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert data["health_endpoint"] == "/api/health"
