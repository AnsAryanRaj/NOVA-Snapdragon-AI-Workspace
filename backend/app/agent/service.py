"""Agent service interface providing planning, plan execution, and unified workflow dispatch."""

from sqlalchemy.orm import Session
from app.agent.schemas import (
    AgentRequest,
    AgentPlan,
    AgentExecutionResult
)
from app.agent.planner import agent_planner
from app.agent.executor import agent_executor


def plan_agent_request(request_input: AgentRequest) -> AgentPlan:
    """
    Parse natural language request and create inspectable AgentPlan.
    Does NOT execute tools.
    """
    return agent_planner.create_plan(request_input)


async def execute_agent_plan(plan: AgentPlan, db: Session) -> AgentExecutionResult:
    """
    Re-validate and execute an AgentPlan safely through the ToolRegistry boundary.
    """
    return await agent_executor.execute_plan(plan, db)


async def plan_and_execute(request_input: AgentRequest, db: Session) -> AgentExecutionResult:
    """
    Convenience method to plan and execute a natural language request.
    """
    plan = plan_agent_request(request_input)
    return await execute_agent_plan(plan, db)
