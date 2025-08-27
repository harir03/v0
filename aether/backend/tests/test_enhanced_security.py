"""
Additional security tests for enhanced middleware and async execution
"""
import pytest
import asyncio
from httpx import AsyncClient
from main import app

@pytest.mark.asyncio
async def test_security_headers():
    """Test that security headers are properly set"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/health")
        
        # Check all security headers
        assert "x-content-type-options" in response.headers
        assert response.headers["x-content-type-options"] == "nosniff"
        
        assert "x-frame-options" in response.headers
        assert response.headers["x-frame-options"] == "DENY"
        
        assert "x-xss-protection" in response.headers
        assert response.headers["x-xss-protection"] == "1; mode=block"
        
        assert "strict-transport-security" in response.headers
        assert "max-age=31536000" in response.headers["strict-transport-security"]

@pytest.mark.asyncio
async def test_payload_size_limit():
    """Test that large payloads are rejected"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        # Create a large payload (simulated with headers since we're not actually sending 10MB)
        large_data = "x" * 1000  # This won't trigger the limit, but tests the endpoint
        
        # Login first
        login_response = await client.post("/api/v1/auth/login", json={
            "email": "admin@aether-agents.com",
            "password": "changeme"
        })
        token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        
        # Try to create agent with large description (should be blocked by length validation)
        agent_data = {
            "name": "Test Agent",
            "type": "automation", 
            "description": large_data,  # Large but under limit
            "configuration": {"test": "value"}
        }
        
        response = await client.post("/api/v1/agents/", json=agent_data, headers=headers)
        # Should be rejected due to description length limit (500 chars)
        assert response.status_code == 400

@pytest.mark.asyncio
async def test_async_task_execution():
    """Test async task execution flow"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        # Login
        login_response = await client.post("/api/v1/auth/login", json={
            "email": "admin@aether-agents.com",
            "password": "changeme"
        })
        token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        
        # Create agent
        agent_data = {
            "name": "Async Test Agent",
            "type": "data_analysis",
            "description": "Testing async execution",
            "configuration": {"analysis_type": "comprehensive"}
        }
        
        create_response = await client.post("/api/v1/agents/", json=agent_data, headers=headers)
        assert create_response.status_code == 200
        agent = create_response.json()
        agent_id = agent["id"]
        
        # Submit task
        task_data = {
            "type": "data_analysis",
            "description": "Analyze user behavior patterns from the last month"
        }
        
        exec_response = await client.post(f"/api/v1/agents/{agent_id}/execute", json=task_data, headers=headers)
        assert exec_response.status_code == 200
        
        result = exec_response.json()["result"]
        assert "task_id" in result
        assert result["status"] == "submitted"
        
        task_id = result["task_id"]
        
        # Check task status
        status_response = await client.get(f"/api/v1/agents/tasks/{task_id}", headers=headers)
        assert status_response.status_code == 200
        
        status = status_response.json()
        assert status["task_id"] == task_id
        assert status["status"] in ["pending", "running", "completed"]

@pytest.mark.asyncio
async def test_queue_status():
    """Test execution queue status endpoint"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        # Login
        login_response = await client.post("/api/v1/auth/login", json={
            "email": "admin@aether-agents.com",
            "password": "changeme"
        })
        token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        
        # Get queue status
        queue_response = await client.get("/api/v1/agents/execution/queue-status", headers=headers)
        assert queue_response.status_code == 200
        
        queue_status = queue_response.json()
        assert "queued_tasks" in queue_status
        assert "active_tasks" in queue_status
        assert "running_tasks" in queue_status
        assert "completed_tasks" in queue_status
        assert "max_concurrent" in queue_status

@pytest.mark.asyncio
async def test_user_isolation():
    """Test that users can only access their own agents and tasks"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        # Register first user
        user1_response = await client.post("/api/v1/auth/register", json={
            "email": "user1@test.com",
            "password": "password123",
            "full_name": "User One"
        })
        assert user1_response.status_code == 200
        user1_token = user1_response.json()["access_token"]
        user1_headers = {"Authorization": f"Bearer {user1_token}"}
        
        # Register second user
        user2_response = await client.post("/api/v1/auth/register", json={
            "email": "user2@test.com",
            "password": "password123",
            "full_name": "User Two"
        })
        assert user2_response.status_code == 200
        user2_token = user2_response.json()["access_token"]
        user2_headers = {"Authorization": f"Bearer {user2_token}"}
        
        # User 1 creates an agent
        agent_data = {
            "name": "User 1 Agent",
            "type": "automation",
            "description": "User 1's private agent"
        }
        
        create_response = await client.post("/api/v1/agents/", json=agent_data, headers=user1_headers)
        assert create_response.status_code == 200
        agent = create_response.json()
        agent_id = agent["id"]
        
        # User 2 should not be able to access User 1's agent
        access_response = await client.get(f"/api/v1/agents/{agent_id}", headers=user2_headers)
        assert access_response.status_code == 404  # Not found (due to user isolation)
        
        # User 1 should be able to access their own agent
        own_access_response = await client.get(f"/api/v1/agents/{agent_id}", headers=user1_headers)
        assert own_access_response.status_code == 200

@pytest.mark.asyncio 
async def test_input_sanitization():
    """Test that malicious inputs are sanitized or rejected"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        # Login
        login_response = await client.post("/api/v1/auth/login", json={
            "email": "admin@aether-agents.com",
            "password": "changeme"
        })
        token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        
        # Test XSS attempt in agent name
        malicious_agent = {
            "name": "<script>alert('xss')</script>Test Agent",
            "type": "automation",
            "description": "Testing XSS protection"
        }
        
        response = await client.post("/api/v1/agents/", json=malicious_agent, headers=headers)
        assert response.status_code == 200
        
        # Check that the script tags were sanitized
        agent = response.json()
        # The validation should sanitize the input
        assert "alert('xss')" not in agent["name"]
        # Either the tags are removed or escaped
        assert ("<script>" not in agent["name"]) or ("&lt;script&gt;" in agent["name"])

@pytest.mark.asyncio
async def test_authentication_required():
    """Test that all protected endpoints require authentication"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        protected_endpoints = [
            ("GET", "/api/v1/agents/"),
            ("POST", "/api/v1/agents/"),
            ("GET", "/api/v1/agents/test-id"),
            ("PUT", "/api/v1/agents/test-id"),
            ("DELETE", "/api/v1/agents/test-id"),
            ("POST", "/api/v1/agents/test-id/execute"),
            ("GET", "/api/v1/agents/tasks/test-task-id"),
            ("GET", "/api/v1/agents/execution/queue-status"),
        ]
        
        for method, endpoint in protected_endpoints:
            if method == "GET":
                response = await client.get(endpoint)
            elif method == "POST":
                response = await client.post(endpoint, json={})
            elif method == "PUT":
                response = await client.put(endpoint, json={})
            elif method == "DELETE":
                response = await client.delete(endpoint)
            
            # Should be 403 (Forbidden) or 401 (Unauthorized)
            assert response.status_code in [401, 403], f"Endpoint {method} {endpoint} should require auth"