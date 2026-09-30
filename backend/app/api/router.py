"""Central API Router for NOVA Backend."""

from fastapi import APIRouter
from app.api.health import router as health_router
from app.api.workspace import router as workspace_router
from app.api.documents import router as documents_router
from app.api.qualcomm import router as qualcomm_router
from app.api.agent import router as agent_router

api_router = APIRouter()
api_router.include_router(health_router, tags=["Health"])
api_router.include_router(workspace_router, prefix="/v1", tags=["Workspace"])
api_router.include_router(documents_router, prefix="/v1", tags=["Documents"])
api_router.include_router(qualcomm_router, prefix="/v1", tags=["AI Runtime"])
api_router.include_router(agent_router, prefix="/v1", tags=["Controlled Agent"])



