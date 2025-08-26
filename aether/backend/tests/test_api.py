import pytest
import asyncio
from httpx import AsyncClient
from main import app

@pytest.fixture
async def client():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

@pytest.mark.asyncio
async def test_health_endpoint(client):
    response = await client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy", "service": "aether-agents-api"}

@pytest.mark.asyncio
async def test_root_endpoint(client):
    response = await client.get("/")
    assert response.status_code == 200
    assert "Aether Agents API is running" in response.json()["message"]

@pytest.mark.asyncio
async def test_create_agent(client):
    agent_data = {
        "name": "Test Agent",
        "description": "A test agent for automated testing",
        "type": "workflow",
        "configuration": {
            "temperature": 0.7,
            "max_tokens": 1000
        }
    }
    
    response = await client.post("/api/v1/agents/", json=agent_data)
    assert response.status_code == 200
    
    data = response.json()
    assert data["name"] == agent_data["name"]
    assert data["type"] == agent_data["type"]
    assert "id" in data
    assert "created_at" in data

@pytest.mark.asyncio
async def test_list_agents(client):
    response = await client.get("/api/v1/agents/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

@pytest.mark.asyncio
async def test_generate_interface(client):
    prompt_data = {
        "prompt": "Create a simple contact form with name, email, and message fields",
        "user_id": "test_user"
    }
    
    response = await client.post("/api/v1/interfaces/generate", json=prompt_data)
    assert response.status_code == 200
    
    data = response.json()
    assert data["success"] is True
    assert "interface_id" in data
    assert "html" in data
    assert "css" in data
    assert "javascript" in data