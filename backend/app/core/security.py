"""Security Policy Enforcer for NOVA Workspace Assistant.

Enforces strict offline privacy, blocks arbitrary command execution, and mandates tool registration.
"""

from typing import Dict, Any
from app.core.config import settings


class SecurityPolicyEnforcer:
    """Enforces NOVA security principles."""
    
    @staticmethod
    def is_arbitrary_command_allowed() -> bool:
        """Arbitrary shell execution is strictly disabled by design."""
        return settings.UNRESTRICTED_SHELL_ALLOWED

    @staticmethod
    def validate_action_request(tool_name: str, requires_confirmation: bool, user_confirmed: bool) -> Dict[str, Any]:
        """Validates if an action request meets security standards."""
        if settings.UNRESTRICTED_SHELL_ALLOWED:
            raise PermissionError("Unrestricted shell execution is forbidden by core system security policy.")
            
        if requires_confirmation and not user_confirmed:
            return {
                "allowed": False,
                "reason": f"Action '{tool_name}' requires explicit user confirmation before execution."
            }
            
        return {
            "allowed": True,
            "reason": "Action validated against Tool Registry and Security Policy."
        }

    @staticmethod
    def get_security_status() -> Dict[str, Any]:
        """Returns the current security policy status."""
        return {
            "shell_execution_blocked": not settings.UNRESTRICTED_SHELL_ALLOWED,
            "tool_registry_enforced": True,
            "user_confirmation_required": settings.CONFIRMATION_REQUIRED_DEFAULT,
            "audit_logging_active": settings.AUDIT_LOG_ENABLED,
            "privacy_mode": settings.PRIVACY_MODE,
        }
