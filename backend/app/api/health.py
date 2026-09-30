"""Health Check API Endpoint."""

from datetime import datetime, timezone
from fastapi import APIRouter
from pydantic import BaseModel, Field
from app.core.config import settings
from app.core.security import SecurityPolicyEnforcer

router = APIRouter()


class SecurityPolicySchema(BaseModel):
    shell_execution_blocked: bool = Field(..., description="Whether arbitrary shell execution is blocked")
    tool_registry_enforced: bool = Field(..., description="Whether actions must go through tool registry")
    user_confirmation_required: bool = Field(..., description="Whether sensitive actions require confirmation")
    audit_logging_active: bool = Field(..., description="Whether audit trail is recorded")


class HealthResponse(BaseModel):
    status: str = Field("ok", json_schema_extra={"example": "ok"})
    service: str = Field(..., json_schema_extra={"example": "NOVA Workspace Assistant"})
    version: str = Field(..., json_schema_extra={"example": "0.1.0"})
    privacy_mode: str = Field(..., json_schema_extra={"example": "offline-strict"})
    qualcomm_isolation: str = Field("isolated-fallback", json_schema_extra={"example": "isolated-fallback"})
    environment: str = Field(..., json_schema_extra={"example": "development"})
    timestamp: str = Field(..., json_schema_extra={"example": "2026-09-24T13:51:51Z"})
    security_policy: SecurityPolicySchema


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Basic health check endpoint returning system status and security policy state."""
    sec_status = SecurityPolicyEnforcer.get_security_status()
    return HealthResponse(
        status="ok",
        service=settings.PROJECT_NAME,
        version=settings.VERSION,
        privacy_mode=settings.PRIVACY_MODE,
        qualcomm_isolation="isolated-fallback",
        environment=settings.ENVIRONMENT,
        timestamp=datetime.now(timezone.utc).isoformat(),
        security_policy=SecurityPolicySchema(
            shell_execution_blocked=sec_status["shell_execution_blocked"],
            tool_registry_enforced=sec_status["tool_registry_enforced"],
            user_confirmation_required=sec_status["user_confirmation_required"],
            audit_logging_active=sec_status["audit_logging_active"],
        )
    )
