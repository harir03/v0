"""
Enhanced security middleware for Aether Agents API
"""
from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
import time
from typing import Dict, Any
from collections import defaultdict
import re
from app.core.security import log_security_event

class SecurityMiddleware(BaseHTTPMiddleware):
    """Enhanced security middleware with rate limiting, IP filtering, and request validation"""
    
    def __init__(self, app, rate_limit_requests: int = 100, rate_limit_window: int = 3600):
        super().__init__(app)
        self.rate_limit_requests = rate_limit_requests
        self.rate_limit_window = rate_limit_window
        # In production, use Redis for distributed rate limiting
        self.request_counts: Dict[str, Dict[str, Any]] = defaultdict(
            lambda: {"count": 0, "reset_time": 0}
        )
        
        # Basic security patterns
        self.suspicious_patterns = [
            r'<script.*?>.*?</script>',
            r'javascript:',
            r'vbscript:',
            r'onload\s*=',
            r'onerror\s*=',
            r'onclick\s*=',
            r'eval\s*\(',
            r'expression\s*\(',
            r'exec\s*\(',
            r'system\s*\(',
            r'shell_exec\s*\(',
            r'passthru\s*\(',
            r'union\s+select',
            r'drop\s+table',
            r'insert\s+into',
            r'delete\s+from',
            r'update\s+.*set',
            r'\.\./\.\.',
            r'etc/passwd',
            r'proc/self',
        ]
        self.compiled_patterns = [re.compile(pattern, re.IGNORECASE) for pattern in self.suspicious_patterns]
    
    def get_client_ip(self, request: Request) -> str:
        """Extract client IP address"""
        # Check for forwarded headers (proxy/load balancer)
        forwarded_for = request.headers.get("X-Forwarded-For")
        if forwarded_for:
            return forwarded_for.split(",")[0].strip()
        
        real_ip = request.headers.get("X-Real-IP")
        if real_ip:
            return real_ip
        
        # Fallback to client host
        if hasattr(request.client, 'host'):
            return request.client.host
        return "unknown"
    
    def is_request_suspicious(self, request_data: str) -> bool:
        """Check for suspicious patterns in request data"""
        for pattern in self.compiled_patterns:
            if pattern.search(request_data):
                return True
        return False
    
    def check_rate_limit(self, client_ip: str) -> bool:
        """Check if client has exceeded rate limit"""
        current_time = time.time()
        client_data = self.request_counts[client_ip]
        
        # Reset counter if window has passed
        if current_time > client_data["reset_time"]:
            client_data["count"] = 0
            client_data["reset_time"] = current_time + self.rate_limit_window
        
        # Check if limit exceeded
        if client_data["count"] >= self.rate_limit_requests:
            return False
        
        # Increment counter
        client_data["count"] += 1
        return True
    
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        client_ip = self.get_client_ip(request)
        
        try:
            # Rate limiting
            if not self.check_rate_limit(client_ip):
                log_security_event("rate_limit_exceeded", None, {
                    "client_ip": client_ip,
                    "path": str(request.url.path),
                    "method": request.method
                })
                return JSONResponse(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    content={"detail": "Rate limit exceeded. Please try again later."}
                )
            
            # Request size limiting (prevent large payloads)
            content_length = request.headers.get("content-length")
            if content_length and int(content_length) > 10 * 1024 * 1024:  # 10MB limit
                log_security_event("payload_too_large", None, {
                    "client_ip": client_ip,
                    "content_length": content_length
                })
                return JSONResponse(
                    status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                    content={"detail": "Request payload too large"}
                )
            
            # Process request
            response = await call_next(request)
            
            # Add security headers
            response.headers["X-Content-Type-Options"] = "nosniff"
            response.headers["X-Frame-Options"] = "DENY"
            response.headers["X-XSS-Protection"] = "1; mode=block"
            response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains; preload"
            response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
            response.headers["Content-Security-Policy"] = "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' data: https:; font-src 'self' https:; connect-src 'self' https:; frame-ancestors 'none';"
            response.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=(), payment=()"
            
            # HTTPS enforcement for production
            if request.headers.get("x-forwarded-proto") == "http":
                https_url = str(request.url).replace("http://", "https://", 1)
                return JSONResponse(
                    status_code=status.HTTP_301_MOVED_PERMANENTLY,
                    headers={"Location": https_url}
                )
            
            return response
            
        except Exception as e:
            # Log security incidents
            log_security_event("security_middleware_error", None, {
                "client_ip": client_ip,
                "error": str(e),
                "path": str(request.url.path)
            })
            # Return generic error to avoid information disclosure
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"detail": "Internal server error"}
            )