"""Tool Registry System for NOVA.

All system actions MUST be registered here.
Direct/arbitrary command execution is strictly forbidden.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from app.core.security import SecurityPolicyEnforcer


class BaseTool(ABC):
    """Abstract base class for all NOVA explicit workspace tools."""

    name: str
    category: str
    description: str
    is_destructive: bool = False
    requires_confirmation: bool = True
    is_enabled: bool = True
    scope: str = "test_workspace"
    risk_level: str = "low"

    @abstractmethod
    async def execute(self, params: Dict[str, Any], user_confirmed: bool = False) -> Dict[str, Any]:
        """Executes the tool after passing security checks."""
        pass


class ToolRegistry:
    """Central Tool Registry managing allowed system actions."""

    def __init__(self):
        self._registry: Dict[str, BaseTool] = {}

    def register(self, tool: BaseTool) -> None:
        """Registers a new explicit tool into the registry."""
        if SecurityPolicyEnforcer.is_arbitrary_command_allowed():
            raise PermissionError("System security violation: arbitrary shell execution attempted.")
        self._registry[tool.name] = tool

    def get_tool(self, tool_name: str) -> Optional[BaseTool]:
        """Retrieves a registered tool by name."""
        return self._registry.get(tool_name)

    def list_tools(self) -> List[Dict[str, Any]]:
        """Returns metadata for all registered tools."""
        return [
            {
                "name": tool.name,
                "category": tool.category,
                "description": tool.description,
                "is_destructive": tool.is_destructive,
                "requires_confirmation": tool.requires_confirmation,
                "is_enabled": tool.is_enabled,
                "scope": tool.scope,
                "risk_level": tool.risk_level,
            }
            for tool in self._registry.values()
        ]


# --- Read-Only Workspace Tools Definitions ---

class WorkspaceListFilesTool(BaseTool):
    name = "workspace.list_files"
    category = "workspace"
    description = "List files and subdirectories inside controlled workspace"
    is_destructive = False
    requires_confirmation = False
    scope = "test_workspace"
    risk_level = "low"

    async def execute(self, params: Dict[str, Any], user_confirmed: bool = False) -> Dict[str, Any]:
        from app.workspace.service import workspace_service
        path = params.get("path", "")
        res = workspace_service.list_directory(path)
        return res.model_dump()


class WorkspaceSearchFilesTool(BaseTool):
    name = "workspace.search_files"
    category = "workspace"
    description = "Search files and directories by query string inside test workspace"
    is_destructive = False
    requires_confirmation = False
    scope = "test_workspace"
    risk_level = "low"

    async def execute(self, params: Dict[str, Any], user_confirmed: bool = False) -> Dict[str, Any]:
        from app.workspace.service import workspace_service
        q = params.get("q", "")
        res = workspace_service.search_files(q)
        return res.model_dump()


class WorkspaceGetMetadataTool(BaseTool):
    name = "workspace.get_metadata"
    category = "workspace"
    description = "Retrieve detailed file or directory metadata"
    is_destructive = False
    requires_confirmation = False
    scope = "test_workspace"
    risk_level = "low"

    async def execute(self, params: Dict[str, Any], user_confirmed: bool = False) -> Dict[str, Any]:
        from app.workspace.service import workspace_service
        path = params.get("path", "")
        res = workspace_service.get_metadata(path)
        return res.model_dump()


class WorkspaceGetHashTool(BaseTool):
    name = "workspace.get_hash"
    category = "workspace"
    description = "Calculate streaming SHA-256 hash for a workspace file"
    is_destructive = False
    requires_confirmation = False
    scope = "test_workspace"
    risk_level = "low"

    async def execute(self, params: Dict[str, Any], user_confirmed: bool = False) -> Dict[str, Any]:
        from app.workspace.service import workspace_service
        path = params.get("path", "")
        res = workspace_service.calculate_sha256(path)
        return res.model_dump()


class WorkspaceReadTextTool(BaseTool):
    name = "workspace.read_text"
    category = "workspace"
    description = "Safely read text content of supported text files within size limit"
    is_destructive = False
    requires_confirmation = False
    scope = "test_workspace"
    risk_level = "low"

    async def execute(self, params: Dict[str, Any], user_confirmed: bool = False) -> Dict[str, Any]:
        from app.workspace.service import workspace_service
        path = params.get("path", "")
        res = workspace_service.read_text_content(path)
        return res.model_dump()


class WorkspaceGetStatsTool(BaseTool):
    name = "workspace.get_stats"
    category = "workspace"
    description = "Retrieve summary statistics for the controlled workspace"
    is_destructive = False
    requires_confirmation = False
    scope = "test_workspace"
    risk_level = "low"

    async def execute(self, params: Dict[str, Any], user_confirmed: bool = False) -> Dict[str, Any]:
        from app.workspace.service import workspace_service
        res = workspace_service.get_stats()
        return res.model_dump()


# --- Read-Only Document Tools Definitions ---

class DocumentListTool(BaseTool):
    name = "document.list"
    category = "document"
    description = "List indexed workspace documents"
    is_destructive = False
    requires_confirmation = False
    scope = "test_workspace"
    risk_level = "low"

    async def execute(self, params: Dict[str, Any], user_confirmed: bool = False) -> Dict[str, Any]:
        from app.db.database import SessionLocal
        from app.documents.service import list_documents
        db_provided = params.get("_db")
        db = db_provided if db_provided is not None else SessionLocal()
        try:
            subpath = params.get("subpath")
            extension = params.get("extension")
            status = params.get("status")
            res = list_documents(db, subpath=subpath, extension=extension, status=status)
            return {"documents": [d.model_dump() for d in res]}
        finally:
            if db_provided is None:
                db.close()


class DocumentGetMetadataTool(BaseTool):
    name = "document.get_metadata"
    category = "document"
    description = "Retrieve metadata for an indexed document by ID or path"
    is_destructive = False
    requires_confirmation = False
    scope = "test_workspace"
    risk_level = "low"

    async def execute(self, params: Dict[str, Any], user_confirmed: bool = False) -> Dict[str, Any]:
        from app.db.database import SessionLocal
        from app.documents.service import get_document_detail
        db_provided = params.get("_db")
        db = db_provided if db_provided is not None else SessionLocal()
        try:
            doc_id = params.get("doc_id") or params.get("path", "")
            res = get_document_detail(db, doc_id)
            return res.model_dump() if res else {"error": "Document not found"}
        finally:
            if db_provided is None:
                db.close()


class DocumentGetContentTool(BaseTool):
    name = "document.get_content"
    category = "document"
    description = "Retrieve extracted text content and chunks for an indexed document"
    is_destructive = False
    requires_confirmation = False
    scope = "test_workspace"
    risk_level = "low"

    async def execute(self, params: Dict[str, Any], user_confirmed: bool = False) -> Dict[str, Any]:
        from app.db.database import SessionLocal
        from app.documents.service import get_document_content
        db_provided = params.get("_db")
        db = db_provided if db_provided is not None else SessionLocal()
        try:
            doc_id = params.get("doc_id") or params.get("path", "")
            res = get_document_content(db, doc_id)
            if not res:
                return {"error": "Document not found"}
            return res.model_dump()
        finally:
            if db_provided is None:
                db.close()


class DocumentSearchTool(BaseTool):
    name = "document.search"
    category = "document"
    description = "Search workspace document contents by query terms with snippet matching"
    is_destructive = False
    requires_confirmation = False
    scope = "test_workspace"
    risk_level = "low"

    async def execute(self, params: Dict[str, Any], user_confirmed: bool = False) -> Dict[str, Any]:
        from app.db.database import SessionLocal
        from app.documents.service import search_documents
        db_provided = params.get("_db")
        db = db_provided if db_provided is not None else SessionLocal()
        try:
            q = params.get("q", "")
            limit = params.get("limit", 20)
            res = search_documents(db, q, limit=limit)
            return res.model_dump()
        finally:
            if db_provided is None:
                db.close()


class DocumentIndexTool(BaseTool):
    name = "document.index"
    category = "document"
    description = "Trigger workspace document indexing or reindexing within test_workspace"
    is_destructive = False
    requires_confirmation = False
    scope = "test_workspace"
    risk_level = "low"

    async def execute(self, params: Dict[str, Any], user_confirmed: bool = False) -> Dict[str, Any]:
        from app.db.database import SessionLocal
        from app.documents.index import index_workspace_documents
        db_provided = params.get("_db")
        db = db_provided if db_provided is not None else SessionLocal()
        try:
            subpath = params.get("subpath", "")
            force = params.get("force_reindex", False)
            res = index_workspace_documents(db, subpath=subpath, force_reindex=force)
            return res.model_dump()
        finally:
            if db_provided is None:
                db.close()


class DocumentGetStatsTool(BaseTool):
    name = "document.get_stats"
    category = "document"
    description = "Get statistics for the document index"
    is_destructive = False
    requires_confirmation = False
    scope = "test_workspace"
    risk_level = "low"

    async def execute(self, params: Dict[str, Any], user_confirmed: bool = False) -> Dict[str, Any]:
        from app.db.database import SessionLocal
        from app.documents.service import get_document_stats
        db_provided = params.get("_db")
        db = db_provided if db_provided is not None else SessionLocal()
        try:
            res = get_document_stats(db)
            return res.model_dump()
        finally:
            if db_provided is None:
                db.close()


# Singleton instance of ToolRegistry
tool_registry = ToolRegistry()

# Automatically register Phase 3 Read-Only Workspace Tools
tool_registry.register(WorkspaceListFilesTool())
tool_registry.register(WorkspaceSearchFilesTool())
tool_registry.register(WorkspaceGetMetadataTool())
tool_registry.register(WorkspaceGetHashTool())
tool_registry.register(WorkspaceReadTextTool())
tool_registry.register(WorkspaceGetStatsTool())

# Automatically register Phase 4 Read-Only Document Tools
tool_registry.register(DocumentListTool())
tool_registry.register(DocumentGetMetadataTool())
tool_registry.register(DocumentGetContentTool())
tool_registry.register(DocumentSearchTool())
tool_registry.register(DocumentIndexTool())
tool_registry.register(DocumentGetStatsTool())

