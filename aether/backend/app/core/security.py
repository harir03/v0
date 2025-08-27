"""
Security utilities and authentication middleware for Aether Agents API
"""
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import secrets
import time
from collections import defaultdict
from app.core.config import settings

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT token handling
security = HTTPBearer()

# Rate limiting storage (in production, use Redis)
rate_limit_store: Dict[str, Dict[str, Any]] = defaultdict(lambda: {"count": 0, "reset_time": 0})

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against a hashed password"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Hash a password"""
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create JWT access token"""
    from datetime import datetime, timezone
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def verify_token(token: str) -> Optional[Dict[str, Any]]:
    """Verify JWT token and return payload"""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            return None
        return payload
    except JWTError:
        return None

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> Dict[str, Any]:
    """Dependency to get current authenticated user"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    payload = verify_token(credentials.credentials)
    if payload is None:
        raise credentials_exception
    
    return payload

def rate_limit(requests: int = 10, window: int = 60):
    """Rate limiting decorator"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            # Rate limiting logic would go here
            # For now, just pass through
            return func(*args, **kwargs)
        return wrapper
    return decorator

def require_auth(user: Dict[str, Any] = Depends(get_current_user)) -> Dict[str, Any]:
    """Dependency to require authentication"""
    return user

def validate_input(data: Dict[str, Any], required_fields: list = None, max_lengths: Dict[str, int] = None) -> Dict[str, Any]:
    """Input validation and sanitization"""
    if required_fields:
        for field in required_fields:
            if field not in data:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Missing required field: {field}"
                )
    
    if max_lengths:
        for field, max_length in max_lengths.items():
            if field in data and isinstance(data[field], str) and len(data[field]) > max_length:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Field {field} exceeds maximum length of {max_length}"
                )
    
    # Basic sanitization - remove/escape potentially dangerous characters
    sanitized_data = {}
    for key, value in data.items():
        if isinstance(value, str):
            # More aggressive HTML/script tag removal and escaping
            sanitized_value = value
            
            # Remove script tags completely
            import re
            sanitized_value = re.sub(r'<script[^>]*>.*?</script>', '', sanitized_value, flags=re.IGNORECASE | re.DOTALL)
            sanitized_value = re.sub(r'<script[^>]*>', '', sanitized_value, flags=re.IGNORECASE)
            sanitized_value = re.sub(r'</script>', '', sanitized_value, flags=re.IGNORECASE)
            
            # Remove other potentially dangerous tags
            dangerous_tags = ['iframe', 'object', 'embed', 'form', 'input', 'textarea', 'button', 'select']
            for tag in dangerous_tags:
                sanitized_value = re.sub(f'<{tag}[^>]*>.*?</{tag}>', '', sanitized_value, flags=re.IGNORECASE | re.DOTALL)
                sanitized_value = re.sub(f'<{tag}[^>]*>', '', sanitized_value, flags=re.IGNORECASE)
                sanitized_value = re.sub(f'</{tag}>', '', sanitized_value, flags=re.IGNORECASE)
            
            # Remove javascript: and vbscript: protocols
            sanitized_value = re.sub(r'javascript\s*:', '', sanitized_value, flags=re.IGNORECASE)
            sanitized_value = re.sub(r'vbscript\s*:', '', sanitized_value, flags=re.IGNORECASE)
            
            # Remove event handlers
            event_handlers = ['onload', 'onclick', 'onmouseover', 'onerror', 'onsubmit', 'onchange', 'onkeydown', 'onkeyup']
            for handler in event_handlers:
                sanitized_value = re.sub(f'{handler}\\s*=\\s*["\'][^"\']*["\']', '', sanitized_value, flags=re.IGNORECASE)
                sanitized_value = re.sub(f'{handler}\\s*=\\s*[^\\s>]+', '', sanitized_value, flags=re.IGNORECASE)
            
            # Basic HTML escaping for remaining brackets
            sanitized_value = sanitized_value.replace("<", "&lt;").replace(">", "&gt;")
            
            sanitized_data[key] = sanitized_value.strip()
        else:
            sanitized_data[key] = value
    
    return sanitized_data

def log_security_event(event_type: str, user_id: str = None, details: Dict[str, Any] = None):
    """Log security events for audit trail"""
    from datetime import datetime, timezone
    log_entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "event_type": event_type,
        "user_id": user_id,
        "details": details or {}
    }
    
    # In production, this would write to a proper audit log system
    # For now, we'll print to console (could be enhanced to write to file/db)
    print(f"SECURITY_EVENT: {log_entry}")