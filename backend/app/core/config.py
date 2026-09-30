"""Application Configuration for NOVA."""

import os
from pathlib import Path
from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict

# Default workspace root location: D:\Nova Snapdragon\test_workspace
_DEFAULT_ROOT = str((Path(__file__).resolve().parent.parent.parent.parent / "test_workspace").resolve())


class Settings(BaseSettings):
    PROJECT_NAME: str = "NOVA Workspace Assistant"
    VERSION: str = "0.1.0"
    API_V1_STR: str = "/api"
    ENVIRONMENT: str = "development"
    
    # Controlled Workspace Root Directory
    WORKSPACE_ROOT: str = _DEFAULT_ROOT
    MAX_TEXT_READ_BYTES: int = 2_000_000  # 2 MB limit for text reads
    
    # Core Security & Privacy Principles
    PRIVACY_MODE: str = "offline-strict"
    UNRESTRICTED_SHELL_ALLOWED: bool = False
    CONFIRMATION_REQUIRED_DEFAULT: bool = True
    AUDIT_LOG_ENABLED: bool = True
    
    # Database
    DATABASE_URL: str = "sqlite:///./nova_workspace.db"
    
    # CORS
    CORS_ORIGINS: List[str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
    ]

    # Qualcomm AI Runtime & Hardware Integration
    QUALCOMM_ENABLED: bool = False
    QUALCOMM_RUNTIME: str = "auto"
    QUALCOMM_MODEL: str = "qcom/llama-3-8b-instruct"
    QUALCOMM_API_TOKEN: str = ""

    def get_redacted_qualcomm_token(self) -> str:
        """Safely redact Qualcomm API token for display/API responses."""
        if not self.QUALCOMM_API_TOKEN:
            return ""
        if len(self.QUALCOMM_API_TOKEN) <= 8:
            return "********"
        return f"{self.QUALCOMM_API_TOKEN[:4]}...{self.QUALCOMM_API_TOKEN[-4:]}"

    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )


settings = Settings()
