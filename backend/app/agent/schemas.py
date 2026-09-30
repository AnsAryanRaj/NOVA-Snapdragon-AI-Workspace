"""Pydantic schemas for Controlled Agent Foundation."""

from datetime import datetime
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, ConfigDict


class PlanStep(BaseModel):
    """Specification for an individual plan step in an AgentPlan."""
    step_index: int
    tool_name: str
    arguments: Dict[str, Any] = {}
    description: str

    model_config = ConfigDict(from_attributes=True)


class AgentPlan(BaseModel):
    """Structured inspection plan produced by the Agent Planner."""
    plan_id: str
    request: str
    intent: str
    steps: List[PlanStep] = []
    requires_confirmation: bool = False
    risk_level: str = "low"
    is_supported: bool = True
    reasoning: str = ""

    model_config = ConfigDict(from_attributes=True)


class AgentRequest(BaseModel):
    """Client request sent to POST /api/v1/agent/plan."""
    request: str
    subpath: Optional[str] = ""


class AgentExecuteRequest(BaseModel):
    """Client request sent to POST /api/v1/agent/execute."""
    plan: AgentPlan


class StepExecutionResult(BaseModel):
    """Execution output of an individual tool step."""
    step_index: int
    tool_name: str
    arguments: Dict[str, Any]
    status: str  # "SUCCESS", "FAILED", "BLOCKED"
    output: Dict[str, Any] = {}
    execution_time_ms: float = 0.0
    error_message: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class AgentExecutionResult(BaseModel):
    """Overall execution summary returned by POST /api/v1/agent/execute."""
    plan_id: str
    request: str
    intent: str
    status: str  # "SUCCESS", "PARTIAL", "FAILED", "REJECTED", "UNSUPPORTED"
    step_results: List[StepExecutionResult] = []
    summary_text: str = ""
    audit_log_id: Optional[int] = None
    total_duration_ms: float = 0.0

    model_config = ConfigDict(from_attributes=True)
