from fastapi import APIRouter
from app.api.v1.endpoints import agents, users, auth, interfaces

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(agents.router, prefix="/agents", tags=["agents"])
api_router.include_router(interfaces.router, prefix="/interfaces", tags=["interfaces"])