from fastapi import APIRouter, HTTPException, status
from app.core.security import create_access_token, verify_password, get_password_hash, log_security_event
from pydantic import BaseModel
from typing import Dict, Any
from datetime import timedelta

router = APIRouter()

# Temporary in-memory user store (would be database in production)
fake_users_db = {
    "admin@aether-agents.com": {
        "id": "admin_user_id",
        "email": "admin@aether-agents.com",
        "hashed_password": get_password_hash("CHANGE_ME_IN_PRODUCTION_SECURE_ADMIN_PASSWORD"),
        "full_name": "Admin User",
        "is_active": True
    }
}

class LoginRequest(BaseModel):
    email: str
    password: str

class RegisterRequest(BaseModel):
    email: str
    password: str
    full_name: str

class Token(BaseModel):
    access_token: str
    token_type: str

def authenticate_user(email: str, password: str) -> Dict[str, Any]:
    """Authenticate user with email and password"""
    user = fake_users_db.get(email)
    if not user:
        return None
    if not verify_password(password, user["hashed_password"]):
        return None
    return user

@router.post("/login", response_model=Token)
async def login(login_data: LoginRequest):
    """User login endpoint"""
    user = authenticate_user(login_data.email, login_data.password)
    if not user:
        log_security_event("login_failed", None, {"email": login_data.email})
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=60 * 24)  # 24 hours (more secure than 8 days)
    access_token = create_access_token(
        data={"sub": user["id"], "email": user["email"]}, expires_delta=access_token_expires
    )
    
    log_security_event("login_success", user["id"], {"email": login_data.email})
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/register", response_model=Token)
async def register(register_data: RegisterRequest):
    """User registration endpoint"""
    # Check if user already exists
    if register_data.email in fake_users_db:
        log_security_event("registration_failed", None, {"email": register_data.email, "reason": "user_exists"})
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user
    import uuid
    user_id = str(uuid.uuid4())
    new_user = {
        "id": user_id,
        "email": register_data.email,
        "hashed_password": get_password_hash(register_data.password),
        "full_name": register_data.full_name,
        "is_active": True
    }
    
    fake_users_db[register_data.email] = new_user
    
    # Generate access token
    access_token_expires = timedelta(minutes=60 * 24)  # 24 hours (more secure than 8 days)
    access_token = create_access_token(
        data={"sub": user_id, "email": register_data.email}, expires_delta=access_token_expires
    )
    
    log_security_event("registration_success", user_id, {"email": register_data.email})
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/logout")
async def logout():
    """User logout endpoint"""
    # In a real implementation, you'd invalidate the token
    # For JWT tokens, you could maintain a blacklist or use short expiry times
    log_security_event("logout", None, {})
    return {"message": "Successfully logged out"}

@router.get("/me")
async def get_current_user():
    """Get current user information"""
    from app.core.security import require_auth
    from fastapi import Depends
    
    # This would typically be implemented with dependency injection
    return {"message": "Current user endpoint - Use /me with proper dependency injection"}