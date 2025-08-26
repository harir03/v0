import logging
import structlog
import time
from datetime import datetime
from typing import Dict, Any, Optional
from prometheus_client import Counter, Histogram, Gauge, generate_latest
from fastapi import Request, Response

# Configure structured logging
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

# Prometheus metrics
REQUEST_COUNT = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status_code']
)

REQUEST_DURATION = Histogram(
    'http_request_duration_seconds',
    'HTTP request duration in seconds',
    ['method', 'endpoint']
)

AGENT_EXECUTIONS = Counter(
    'agent_executions_total',
    'Total agent executions',
    ['agent_type', 'status']
)

AGENT_EXECUTION_DURATION = Histogram(
    'agent_execution_duration_seconds',
    'Agent execution duration in seconds',
    ['agent_type']
)

ACTIVE_USERS = Gauge(
    'active_users_total',
    'Number of active users'
)

SYSTEM_HEALTH = Gauge(
    'system_health_status',
    'System health status (1 = healthy, 0 = unhealthy)'
)

class MonitoringService:
    """Service for application monitoring and observability"""
    
    def __init__(self):
        self.logger = structlog.get_logger(__name__)
    
    def log_request(
        self, 
        request: Request, 
        response: Response, 
        process_time: float
    ):
        """Log HTTP request with structured data"""
        REQUEST_COUNT.labels(
            method=request.method,
            endpoint=str(request.url.path),
            status_code=response.status_code
        ).inc()
        
        REQUEST_DURATION.labels(
            method=request.method,
            endpoint=str(request.url.path)
        ).observe(process_time)
        
        self.logger.info(
            "HTTP request processed",
            method=request.method,
            path=str(request.url.path),
            status_code=response.status_code,
            process_time=process_time,
            user_agent=request.headers.get("user-agent"),
            ip_address=request.client.host if request.client else None
        )
    
    def log_agent_execution(
        self,
        agent_id: str,
        agent_type: str,
        status: str,
        duration: float,
        user_id: str,
        error: Optional[str] = None
    ):
        """Log agent execution with metrics"""
        AGENT_EXECUTIONS.labels(
            agent_type=agent_type,
            status=status
        ).inc()
        
        if status == "completed":
            AGENT_EXECUTION_DURATION.labels(
                agent_type=agent_type
            ).observe(duration)
        
        log_data = {
            "event": "agent_execution",
            "agent_id": agent_id,
            "agent_type": agent_type,
            "status": status,
            "duration": duration,
            "user_id": user_id
        }
        
        if error:
            log_data["error"] = error
            self.logger.error("Agent execution failed", **log_data)
        else:
            self.logger.info("Agent execution completed", **log_data)
    
    def log_user_activity(
        self,
        user_id: str,
        action: str,
        resource_type: str,
        resource_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ):
        """Log user activity for audit purposes"""
        self.logger.info(
            "User activity",
            user_id=user_id,
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            metadata=metadata or {},
            timestamp=datetime.utcnow().isoformat()
        )
    
    def log_security_event(
        self,
        event_type: str,
        severity: str,
        description: str,
        user_id: Optional[str] = None,
        ip_address: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ):
        """Log security-related events"""
        self.logger.warning(
            "Security event",
            event_type=event_type,
            severity=severity,
            description=description,
            user_id=user_id,
            ip_address=ip_address,
            metadata=metadata or {},
            timestamp=datetime.utcnow().isoformat()
        )
    
    def update_system_health(self, is_healthy: bool):
        """Update system health metric"""
        SYSTEM_HEALTH.set(1 if is_healthy else 0)
    
    def get_metrics(self) -> str:
        """Get Prometheus metrics"""
        return generate_latest()

class HealthCheckService:
    """Service for application health checks"""
    
    def __init__(self):
        self.logger = structlog.get_logger(__name__)
    
    async def check_database_health(self) -> Dict[str, Any]:
        """Check database connectivity"""
        try:
            from ..core.database import SessionLocal
            db = SessionLocal()
            
            # Simple query to test connection
            db.execute("SELECT 1")
            db.close()
            
            return {
                "status": "healthy",
                "service": "database",
                "timestamp": datetime.utcnow().isoformat()
            }
        except Exception as e:
            self.logger.error("Database health check failed", error=str(e))
            return {
                "status": "unhealthy",
                "service": "database",
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }
    
    async def check_redis_health(self) -> Dict[str, Any]:
        """Check Redis connectivity"""
        try:
            import redis
            from ..core.config import settings
            
            redis_client = redis.from_url(settings.REDIS_URL)
            redis_client.ping()
            
            return {
                "status": "healthy",
                "service": "redis",
                "timestamp": datetime.utcnow().isoformat()
            }
        except Exception as e:
            self.logger.error("Redis health check failed", error=str(e))
            return {
                "status": "unhealthy",
                "service": "redis",
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }
    
    async def check_celery_health(self) -> Dict[str, Any]:
        """Check Celery worker status"""
        try:
            from ..core.celery_app import celery_app
            
            # Check if workers are available
            inspect = celery_app.control.inspect()
            stats = inspect.stats()
            
            if stats:
                return {
                    "status": "healthy",
                    "service": "celery",
                    "workers": len(stats),
                    "timestamp": datetime.utcnow().isoformat()
                }
            else:
                return {
                    "status": "unhealthy",
                    "service": "celery",
                    "error": "No workers available",
                    "timestamp": datetime.utcnow().isoformat()
                }
        except Exception as e:
            self.logger.error("Celery health check failed", error=str(e))
            return {
                "status": "unhealthy",
                "service": "celery",
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }
    
    async def get_overall_health(self) -> Dict[str, Any]:
        """Get overall system health"""
        import asyncio
        
        checks = await asyncio.gather(
            self.check_database_health(),
            self.check_redis_health(),
            self.check_celery_health(),
            return_exceptions=True
        )
        
        all_healthy = all(
            isinstance(check, dict) and check.get("status") == "healthy" 
            for check in checks
        )
        
        return {
            "status": "healthy" if all_healthy else "unhealthy",
            "timestamp": datetime.utcnow().isoformat(),
            "checks": [check for check in checks if isinstance(check, dict)]
        }

# Global instances
monitoring_service = MonitoringService()
health_service = HealthCheckService()