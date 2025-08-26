from typing import Any, Dict, Optional, Union

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from pydantic import ValidationError
from sqlalchemy.orm import Session

from ..core.config import settings
from ..core.database import get_db
from ..core.security import verify_password, get_password_hash
from ..models.database import User, Subscription
from ..schemas.user import UserCreate, TokenPayload

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/auth/login"
)

class UserService:
    """Service for managing users and authentication"""
    
    @classmethod
    async def get_user_by_email(cls, db: Session, email: str) -> Optional[User]:
        """Get user by email"""
        return db.query(User).filter(User.email == email).first()
    
    @classmethod
    async def authenticate(cls, db: Session, email: str, password: str) -> Optional[User]:
        """Authenticate a user"""
        user = await cls.get_user_by_email(db, email=email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user
    
    @classmethod
    async def create_user(cls, db: Session, user_create: UserCreate) -> User:
        """Create new user"""
        user = User(
            email=user_create.email,
            hashed_password=get_password_hash(user_create.password),
            full_name=user_create.full_name,
            is_active=True,
            is_superuser=False,
            subscription_tier="free"
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        
        # Create default subscription
        subscription = Subscription(
            user_id=user.id,
            tier="free",
            status="active",
            monthly_task_limit=500,
            monthly_tasks_used=0
        )
        db.add(subscription)
        db.commit()
        
        return user
    
    @classmethod
    async def get_current_user(
        cls,
        db: Session = Depends(get_db),
        token: str = Depends(oauth2_scheme)
    ) -> User:
        """Get current user from JWT token"""
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
        try:
            payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
            )
            token_data = TokenPayload(**payload)
        except (JWTError, ValidationError):
            raise credentials_exception
        
        user = db.query(User).filter(User.id == token_data.sub).first()
        if user is None:
            raise credentials_exception
        return user
    
    @classmethod
    async def get_current_active_user(
        cls,
        current_user: User = Depends(get_current_user),
    ) -> User:
        """Get current active user"""
        if not current_user.is_active:
            raise HTTPException(status_code=400, detail="Inactive user")
        return current_user