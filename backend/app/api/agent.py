"""Controlled Agent REST API Endpoints."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.agent.schemas import (
    AgentRequest,
    AgentPlan,
    AgentExecuteRequest,
    AgentExecutionResult
)
from app.agent.service import (
    plan_agent_request,
    execute_agent_plan,
    plan_and_execute
)

router = APIRouter(prefix="/agent", tags=["Controlled Agent"])


@router.post("/plan", response_model=AgentPlan)
def plan_agent_workflow(request_input: AgentRequest):
    """
    Parse natural language request and create an inspectable AgentPlan.
    Does NOT execute tools or modify any state.
    """
    try:
        return plan_agent_request(request_input)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate agent plan: {str(e)}"
        )


@router.post("/execute", response_model=AgentExecutionResult)
async def execute_agent_workflow(
    request: AgentExecuteRequest,
    db: Session = Depends(get_db)
):
    """
    Re-validate every step of an AgentPlan and execute safe read-only tools via ToolRegistry.
    Records an audit log entry upon completion.
    """
    try:
        return await execute_agent_plan(request.plan, db)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to execute agent plan: {str(e)}"
        )


@router.post("/run", response_model=AgentExecutionResult)
async def run_agent_workflow(
    request_input: AgentRequest,
    db: Session = Depends(get_db)
):
    """
    Convenience endpoint to plan, validate, and execute an agent request.
    """
    try:
        return await plan_and_execute(request_input, db)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to run agent workflow: {str(e)}"
        )


@router.get("/audit-logs")
def get_agent_audit_logs(
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """
    Retrieve recent agent execution audit logs recorded in SQLite database.
    """
    from app.db.models import AuditLogEntry
    entries = db.query(AuditLogEntry).order_by(AuditLogEntry.timestamp.desc()).limit(limit).all()
    return [
        {
            "id": str(e.id),
            "timestamp": e.timestamp.isoformat() if e.timestamp else "",
            "action_name": e.action_name,
            "tool_name": e.tool_name,
            "parameters_json": e.parameters_json,
            "requires_confirmation": e.requires_confirmation,
            "user_confirmed": e.user_confirmed,
            "status": e.status,
            "execution_time_ms": e.execution_time_ms,
            "error_message": e.error_message
        }
        for e in entries
    ]
