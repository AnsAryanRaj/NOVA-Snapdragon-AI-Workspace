"""Deterministic Agent Planner for natural language intent routing and multi-step plans."""

import re
import hashlib
import time
from typing import List, Dict, Any, Tuple
from app.agent.schemas import AgentPlan, PlanStep, AgentRequest


UNSAFE_KEYWORDS = {
    "delete", "remove", "unlink", "rm", "rmdir", "erase",
    "write", "edit", "update", "modify", "save", "create",
    "rename", "move", "mv",
    "powershell", "cmd", "exec", "eval", "shell", "bash",
    "sh", "sudo", "admin", "registry", "defender", "firewall",
    "download", "upload", "curl", "wget", "http", "https"
}


class DeterministicAgentPlanner:
    """
    Parses natural language user requests into safe, inspectable, multi-step AgentPlans.
    Uses deterministic keyword and pattern matching. ZERO LLM dependencies.
    """

    def create_plan(self, request_input: AgentRequest) -> AgentPlan:
        raw_text = request_input.request.strip()
        lower_text = raw_text.lower()
        plan_id = hashlib.sha256(f"{raw_text}:{time.time()}".encode("utf-8")).hexdigest()[:16]

        # 1. Check for unsafe/destructive or shell keywords
        tokens = set(re.findall(r"\b\w+\b", lower_text))
        if tokens & UNSAFE_KEYWORDS:
            return AgentPlan(
                plan_id=plan_id,
                request=raw_text,
                intent="UNSUPPORTED",
                steps=[],
                requires_confirmation=False,
                risk_level="high",
                is_supported=False,
                reasoning="Request involves write, modification, deletion, or shell execution which is not allowed."
            )

        # 2. Check for Multi-Step Intent: SEARCH_AND_READ
        if ("find" in lower_text or "search" in lower_text) and ("show" in lower_text or "read" in lower_text or "content" in lower_text or "display" in lower_text):
            query_term = self._extract_search_query(raw_text)
            steps = [
                PlanStep(
                    step_index=1,
                    tool_name="document.search",
                    arguments={"q": query_term},
                    description=f"Search indexed document chunks for query '{query_term}'"
                ),
                PlanStep(
                    step_index=2,
                    tool_name="document.get_content",
                    arguments={"path": query_term},  # Target will be resolved dynamically from search results
                    description=f"Retrieve extracted text content for top matching document"
                )
            ]
            return AgentPlan(
                plan_id=plan_id,
                request=raw_text,
                intent="SEARCH_AND_READ",
                steps=steps,
                requires_confirmation=False,
                risk_level="low",
                is_supported=True,
                reasoning=f"Multi-step plan to search documents for '{query_term}' and read top result."
            )

        # 3. Check for GET_DOCUMENT_CONTENT
        if any(kw in lower_text for kw in ["show content", "read content", "get content", "read file", "read document", "show text", "cat "]):
            path_or_name = self._extract_target_name(raw_text)
            steps = [
                PlanStep(
                    step_index=1,
                    tool_name="document.get_content",
                    arguments={"path": path_or_name},
                    description=f"Retrieve extracted text content for '{path_or_name}'"
                )
            ]
            return AgentPlan(
                plan_id=plan_id,
                request=raw_text,
                intent="GET_DOCUMENT_CONTENT",
                steps=steps,
                requires_confirmation=False,
                risk_level="low",
                is_supported=True,
                reasoning=f"Single-step plan to retrieve document content for '{path_or_name}'."
            )

        # 4. Check for SEARCH_DOCUMENTS
        if any(kw in lower_text for kw in ["search", "find", "query", "look for", "where is"]):
            query_term = self._extract_search_query(raw_text)
            steps = [
                PlanStep(
                    step_index=1,
                    tool_name="document.search",
                    arguments={"q": query_term},
                    description=f"Search workspace document chunks for '{query_term}'"
                )
            ]
            return AgentPlan(
                plan_id=plan_id,
                request=raw_text,
                intent="SEARCH_DOCUMENTS",
                steps=steps,
                requires_confirmation=False,
                risk_level="low",
                is_supported=True,
                reasoning=f"Single-step plan to search documents for '{query_term}'."
            )

        # 5. Check for GET_DOCUMENT_METADATA
        if "metadata" in lower_text or "info" in lower_text or "details" in lower_text:
            path_or_name = self._extract_target_name(raw_text)
            steps = [
                PlanStep(
                    step_index=1,
                    tool_name="document.get_metadata",
                    arguments={"path": path_or_name},
                    description=f"Retrieve metadata for document '{path_or_name}'"
                )
            ]
            return AgentPlan(
                plan_id=plan_id,
                request=raw_text,
                intent="GET_DOCUMENT_METADATA",
                steps=steps,
                requires_confirmation=False,
                risk_level="low",
                is_supported=True,
                reasoning=f"Single-step plan to retrieve document metadata for '{path_or_name}'."
            )

        # 6. Check for LIST_DOCUMENTS
        if "documents" in lower_text and ("list" in lower_text or "show" in lower_text or "what" in lower_text):
            subpath = request_input.subpath or ""
            steps = [
                PlanStep(
                    step_index=1,
                    tool_name="document.list",
                    arguments={"subpath": subpath},
                    description="List indexed workspace documents"
                )
            ]
            return AgentPlan(
                plan_id=plan_id,
                request=raw_text,
                intent="LIST_DOCUMENTS",
                steps=steps,
                requires_confirmation=False,
                risk_level="low",
                is_supported=True,
                reasoning="Single-step plan to list indexed documents."
            )

        # 7. Check for WORKSPACE_SUMMARY
        if any(kw in lower_text for kw in ["how many files", "workspace stats", "workspace summary", "workspace status", "stats"]):
            steps = [
                PlanStep(
                    step_index=1,
                    tool_name="workspace.get_stats",
                    arguments={},
                    description="Retrieve workspace summary statistics"
                )
            ]
            return AgentPlan(
                plan_id=plan_id,
                request=raw_text,
                intent="WORKSPACE_SUMMARY",
                steps=steps,
                requires_confirmation=False,
                risk_level="low",
                is_supported=True,
                reasoning="Single-step plan to retrieve summary statistics for test_workspace."
            )

        # 8. Check for LIST_FILES
        if "list" in lower_text or "files" in lower_text or "dir" in lower_text or "ls" in lower_text:
            subpath = request_input.subpath or ""
            steps = [
                PlanStep(
                    step_index=1,
                    tool_name="workspace.list_files",
                    arguments={"path": subpath},
                    description=f"List files in workspace subpath '{subpath}'"
                )
            ]
            return AgentPlan(
                plan_id=plan_id,
                request=raw_text,
                intent="LIST_FILES",
                steps=steps,
                requires_confirmation=False,
                risk_level="low",
                is_supported=True,
                reasoning="Single-step plan to list workspace files."
            )

        # Fallback for unrecognized intent
        return AgentPlan(
            plan_id=plan_id,
            request=raw_text,
            intent="UNSUPPORTED",
            steps=[],
            requires_confirmation=False,
            risk_level="low",
            is_supported=False,
            reasoning=f"Request '{raw_text}' did not match any supported safe read-only intent patterns."
        )

    def _extract_search_query(self, text: str) -> str:
        """Clean natural language wrapper words to extract search query terms."""
        cleaned = re.sub(r"(?i)\b(find|search|for|my|show|the|contents|of|document|file|report|project|and|read|display|where|is|it)\b", " ", text)
        cleaned = re.sub(r"\s+", " ", cleaned).strip()
        return cleaned if cleaned else text.strip()

    def _extract_target_name(self, text: str) -> str:
        """Extract target file name or path from text."""
        cleaned = re.sub(r"(?i)\b(show|read|get|content|metadata|info|of|file|document|text|cat|details|for|the)\b", " ", text)
        cleaned = re.sub(r"\s+", " ", cleaned).strip()
        return cleaned if cleaned else text.strip()


# Singleton planner instance
agent_planner = DeterministicAgentPlanner()
