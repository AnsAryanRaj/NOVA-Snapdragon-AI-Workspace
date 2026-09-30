"""Safe Agent Executor providing tool safety validation, multi-step execution, and audit logging."""

import time
from datetime import datetime
from typing import List, Dict, Any, Optional, Tuple
from sqlalchemy.orm import Session

from app.agent.schemas import (
    AgentPlan,
    PlanStep,
    StepExecutionResult,
    AgentExecutionResult
)
from app.tools.registry import tool_registry, BaseTool
from app.core.path_security import validate_workspace_path, WorkspaceSecurityError
from app.db.models import AuditLogEntry


class AgentExecutor:
    """
    Validates and executes AgentPlans safely through the ToolRegistry boundary.
    Strictly re-validates tool safety, enforces read-only constraints, and records audit logs.
    """

    async def execute_plan(self, plan: AgentPlan, db: Session) -> AgentExecutionResult:
        start_time = time.time()

        # Reject unsupported or unsafe plans immediately
        if not plan.is_supported or plan.intent == "UNSUPPORTED":
            return AgentExecutionResult(
                plan_id=plan.plan_id,
                request=plan.request,
                intent=plan.intent,
                status="UNSUPPORTED",
                step_results=[],
                summary_text=f"Request unsupported: {plan.reasoning}",
                total_duration_ms=round((time.time() - start_time) * 1000, 2)
            )

        step_results: List[StepExecutionResult] = []
        overall_status = "SUCCESS"
        context_data: Dict[str, Any] = {}

        for step in plan.steps:
            step_start = time.time()

            # 1. Resolve dynamic arguments from previous step context if applicable
            resolved_args = self._resolve_arguments(step, context_data)

            # 2. Strict Tool Re-Validation
            tool_obj, validation_error = self._validate_step_tool(step.tool_name, resolved_args)
            if validation_error or not tool_obj:
                step_results.append(
                    StepExecutionResult(
                        step_index=step.step_index,
                        tool_name=step.tool_name,
                        arguments=resolved_args,
                        status="BLOCKED",
                        output={"error": validation_error},
                        execution_time_ms=round((time.time() - step_start) * 1000, 2),
                        error_message=validation_error
                    )
                )
                overall_status = "FAILED"
                break

            # 3. Execute Tool safely via ToolRegistry
            try:
                resolved_args["_db"] = db
                result_output = await tool_obj.execute(resolved_args, user_confirmed=True)
                step_duration = round((time.time() - step_start) * 1000, 2)

                # Store output in context for multi-step resolution
                context_data[f"step_{step.step_index}"] = result_output

                step_results.append(
                    StepExecutionResult(
                        step_index=step.step_index,
                        tool_name=step.tool_name,
                        arguments={k: v for k, v in resolved_args.items() if k != "_db"},
                        status="SUCCESS",
                        output=result_output,
                        execution_time_ms=step_duration
                    )
                )
            except Exception as e:
                step_duration = round((time.time() - step_start) * 1000, 2)
                step_results.append(
                    StepExecutionResult(
                        step_index=step.step_index,
                        tool_name=step.tool_name,
                        arguments={k: v for k, v in resolved_args.items() if k != "_db"},
                        status="FAILED",
                        output={"error": str(e)},
                        execution_time_ms=step_duration,
                        error_message=str(e)
                    )
                )
                overall_status = "FAILED"
                break

        total_duration = round((time.time() - start_time) * 1000, 2)

        # 4. Generate summary text
        summary_text = self._build_summary(plan, step_results, overall_status)

        # 5. Record Audit Event in database
        audit_entry_id = self._record_audit_log(db, plan, step_results, overall_status, total_duration)

        return AgentExecutionResult(
            plan_id=plan.plan_id,
            request=plan.request,
            intent=plan.intent,
            status=overall_status,
            step_results=step_results,
            summary_text=summary_text,
            audit_log_id=audit_entry_id,
            total_duration_ms=total_duration
        )

    def _validate_step_tool(self, tool_name: str, args: Dict[str, Any]) -> Tuple[Optional[BaseTool], Optional[str]]:
        """Re-validate that the tool is registered, enabled, read-only, and scoped to test_workspace."""
        tool = tool_registry.get_tool(tool_name)
        if not tool:
            return None, f"Security Violation: Tool '{tool_name}' is not registered in ToolRegistry."

        if not tool.is_enabled:
            return None, f"Security Violation: Tool '{tool_name}' is disabled."

        if tool.is_destructive:
            return None, f"Security Violation: Destructive tool '{tool_name}' cannot be called by Agent."

        if tool.scope != "test_workspace":
            return None, f"Security Violation: Tool '{tool_name}' scope '{tool.scope}' is outside test_workspace."

        # Validate path argument if present
        target_path = args.get("path") or args.get("subpath")
        if target_path:
            try:
                validate_workspace_path(target_path)
            except Exception as e:
                return None, f"Security Boundary Violation: Path '{target_path}' is invalid or escapes workspace."

        return tool, None

    def _resolve_arguments(self, step: PlanStep, context: Dict[str, Any]) -> Dict[str, Any]:
        """Resolve dynamic argument dependencies between steps in multi-step plans."""
        args = dict(step.arguments)

        # Multi-step resolution for SEARCH_AND_READ (step 2 gets top search match from step 1)
        if step.step_index == 2 and "step_1" in context:
            step_1_out = context["step_1"]
            matches = step_1_out.get("matches", [])
            if matches:
                top_match = matches[0]
                args["doc_id"] = top_match.get("doc_id") or top_match.get("relative_path")
                args["path"] = top_match.get("relative_path")
            else:
                # No search matches found
                args["doc_id"] = "NO_MATCH_FOUND"

        return args

    def _build_summary(self, plan: AgentPlan, step_results: List[StepExecutionResult], status: str) -> str:
        """Construct human-readable execution summary text."""
        if status != "SUCCESS":
            errors = [sr.error_message for sr in step_results if sr.error_message]
            return f"Agent workflow failed or was blocked: {', '.join(errors) if errors else 'Execution error'}"

        if plan.intent == "SEARCH_AND_READ":
            step_1 = step_results[0].output if len(step_results) > 0 else {}
            step_2 = step_results[1].output if len(step_results) > 1 else {}
            total_matches = step_1.get("total_matches", 0)
            doc_name = step_2.get("file_name", "document")
            chunk_count = step_2.get("chunk_count", 0)
            return f"Found {total_matches} search matches. Displaying extracted content for '{doc_name}' ({chunk_count} chunks)."

        if plan.intent == "SEARCH_DOCUMENTS":
            step_1 = step_results[0].output if len(step_results) > 0 else {}
            total_matches = step_1.get("total_matches", 0)
            return f"Search complete. Located {total_matches} matching document chunks."

        if plan.intent in ("GET_DOCUMENT_CONTENT", "GET_DOCUMENT_METADATA"):
            step_1 = step_results[0].output if len(step_results) > 0 else {}
            doc_name = step_1.get("file_name") or step_1.get("relative_path") or "document"
            return f"Successfully retrieved information for '{doc_name}'."

        if plan.intent == "WORKSPACE_SUMMARY":
            step_1 = step_results[0].output if len(step_results) > 0 else {}
            total_files = step_1.get("total_files", 0)
            return f"Workspace contains {total_files} files across controlled workspace."

        return f"Successfully executed {len(step_results)} step(s) for request."

    def _record_audit_log(
        self,
        db: Session,
        plan: AgentPlan,
        step_results: List[StepExecutionResult],
        status: str,
        duration_ms: float
    ) -> Optional[int]:
        """Record audit event into SQLite audit_logs table."""
        try:
            import json
            executed_tools = [sr.tool_name for sr in step_results]
            entry = AuditLogEntry(
                action_name=f"agent.execute.{plan.intent}",
                tool_name=", ".join(executed_tools) if executed_tools else "agent.planner",
                parameters_json=json.dumps({"request": plan.request, "intent": plan.intent}),
                requires_confirmation=plan.requires_confirmation,
                user_confirmed=True,
                status=status,
                execution_time_ms=int(duration_ms),
                error_message=step_results[-1].error_message if step_results and step_results[-1].error_message else None
            )
            db.add(entry)
            db.commit()
            db.refresh(entry)
            return entry.id
        except Exception as e:
            db.rollback()
            print(f"[AgentExecutor] Audit Log Failed: {e}")
            return None


# Singleton executor instance
agent_executor = AgentExecutor()
