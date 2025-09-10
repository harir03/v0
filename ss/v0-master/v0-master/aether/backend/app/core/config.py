import secrets
from typing import Any, Dict, List, Optional, Union
from pydantic import AnyHttpUrl, HttpUrl, field_validator
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    SERVER_NAME: str = "Aether Agents API"
    SERVER_HOST: AnyHttpUrl = "http://localhost"
    
    # CORS Origins
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = [
        "http://localhost:3000",
        "http://localhost:3001",
        "https://aether-agents.com",
        "https://www.aether-agents.com"
    ]

    @field_validator("BACKEND_CORS_ORIGINS", mode='before')
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    PROJECT_NAME: str = "Aether Agents"
    
    # Database
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_USER: str = "aether_user"
    POSTGRES_PASSWORD: str = "aether_password"
    POSTGRES_DB: str = "aether_agents"
    SQLALCHEMY_DATABASE_URI: Optional[str] = None

    # Redis
    REDIS_URL: str = "redis://localhost:6379"
    
    # AI Provider Settings
    OPENAI_API_KEY: Optional[str] = None
    ANTHROPIC_API_KEY: Optional[str] = None
    GOOGLE_AI_API_KEY: Optional[str] = None
    
    # Email
    SMTP_TLS: bool = True
    SMTP_PORT: Optional[int] = None
    SMTP_HOST: Optional[str] = None
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    EMAILS_FROM_EMAIL: Optional[str] = None
    EMAILS_FROM_NAME: Optional[str] = None

    # First superuser
    FIRST_SUPERUSER: str = "admin@aether-agents.com"
    FIRST_SUPERUSER_PASSWORD: str = "changeme"
    
    # Security
    ALGORITHM: str = "HS256"
    
    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings()