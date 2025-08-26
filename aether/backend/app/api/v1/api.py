from fastapi import APIRouter

from .endpoints import auth, agents, health

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(agents.router, prefix="/agents", tags=["agents"])
api_router.include_router(health.router, prefix="", tags=["health"])