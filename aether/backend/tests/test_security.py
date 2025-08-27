"""
Security tests for Aether Agents API
"""
import pytest
import asyncio
from httpx import AsyncClient
from main import app

@pytest.fixture
async def async_client():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

@pytest.mark.asyncio
async def test_auth_required_for_agents():
    """Test that authentication is required for agent endpoints"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        # Test without authentication
        response = await client.get("/api/v1/agents/")
        assert response.status_code == 401
        
        response = await client.post("/api/v1/agents/", json={
            "name": "Test Agent",
            "type": "automation",
            "description": "Test"
        })
        assert response.status_code == 401

@pytest.mark.asyncio
async def test_login_flow():
    """Test user login functionality"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        # Test login with valid credentials
        response = await client.post("/api/v1/auth/login", json={
            "email": "admin@aether-agents.com",
            "password": "changeme"
        })
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        
        # Test login with invalid credentials
        response = await client.post("/api/v1/auth/login", json={
            "email": "admin@aether-agents.com",
            "password": "wrongpassword"
        })
        assert response.status_code == 401

@pytest.mark.asyncio
async def test_registration_flow():
    """Test user registration functionality"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        # Test registration
        response = await client.post("/api/v1/auth/register", json={
            "email": "newuser@test.com",
            "password": "newpassword123",
            "full_name": "New User"
        })
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        
        # Test duplicate registration
        response = await client.post("/api/v1/auth/register", json={
            "email": "newuser@test.com",
            "password": "anotherpassword",
            "full_name": "Another User"
        })
        assert response.status_code == 400

@pytest.mark.asyncio
async def test_authenticated_agent_access():
    """Test agent access with authentication"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        # First login to get token
        login_response = await client.post("/api/v1/auth/login", json={
            "email": "admin@aether-agents.com",
            "password": "changeme"
        })
        assert login_response.status_code == 200
        token = login_response.json()["access_token"]
        
        # Test authenticated request
        headers = {"Authorization": f"Bearer {token}"}
        response = await client.get("/api/v1/agents/", headers=headers)
        assert response.status_code == 200
        assert isinstance(response.json(), list)