from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.api import api_router
from app.core.config import settings
from app.middleware.security import SecurityMiddleware

app = FastAPI(
    title="Aether Agents API",
    description="Backend API for the Aether Agents platform",
    version="1.0.0",
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Add security middleware first (executes last in the middleware stack)
app.add_middleware(SecurityMiddleware, rate_limit_requests=100, rate_limit_window=3600)

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE"],  # More restrictive than "*"
        allow_headers=["Authorization", "Content-Type"],  # More restrictive than "*"
    )

app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/")
async def root():
    return {"message": "Aether Agents API is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "aether-agents-api"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)