import asyncio
from datetime import datetime
from fastapi import APIRouter, Depends
from typing import Dict, Any

from ...services.monitoring import health_service, monitoring_service

router = APIRouter()

@router.get("/health")
async def health_check() -> Dict[str, Any]:
    """Basic health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "aether-agents-api"
    }

@router.get("/health/detailed")
async def detailed_health_check() -> Dict[str, Any]:
    """Detailed health check with all service dependencies"""
    return await health_service.get_overall_health()

@router.get("/health/ready")
async def readiness_check() -> Dict[str, Any]:
    """Readiness check for Kubernetes/container orchestration"""
    health_status = await health_service.get_overall_health()
    
    if health_status["status"] == "healthy":
        return health_status
    else:
        from fastapi import HTTPException
        raise HTTPException(status_code=503, detail=health_status)

@router.get("/health/live")
async def liveness_check() -> Dict[str, Any]:
    """Liveness check for Kubernetes/container orchestration"""
    return {
        "status": "alive",
        "timestamp": datetime.utcnow().isoformat()
    }

@router.get("/metrics")
async def metrics() -> str:
    """Prometheus metrics endpoint"""
    from fastapi import Response
    metrics_data = monitoring_service.get_metrics()
    return Response(content=metrics_data, media_type="text/plain")