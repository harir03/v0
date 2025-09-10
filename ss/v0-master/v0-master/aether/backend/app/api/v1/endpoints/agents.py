from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app.schemas.agent import Agent, AgentCreate, AgentUpdate
from app.services.agent_service import AgentService

router = APIRouter()

@router.get("/", response_model=List[Agent])
async def list_agents():
    """Get all agents for the current user"""
    # TODO: Add authentication and user filtering
    return await AgentService.list_agents()

@router.post("/", response_model=Agent)
async def create_agent(agent: AgentCreate):
    """Create a new agent"""
    return await AgentService.create_agent(agent)

@router.get("/{agent_id}", response_model=Agent)
async def get_agent(agent_id: str):
    """Get a specific agent by ID"""
    agent = await AgentService.get_agent(agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    return agent

@router.put("/{agent_id}", response_model=Agent)
async def update_agent(agent_id: str, agent_update: AgentUpdate):
    """Update an existing agent"""
    agent = await AgentService.update_agent(agent_id, agent_update)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    return agent

@router.delete("/{agent_id}")
async def delete_agent(agent_id: str):
    """Delete an agent"""
    success = await AgentService.delete_agent(agent_id)
    if not success:
        raise HTTPException(status_code=404, detail="Agent not found")
    return {"message": "Agent deleted successfully"}

@router.post("/{agent_id}/execute")
async def execute_agent(agent_id: str, task: dict):
    """Execute a task using the specified agent"""
    result = await AgentService.execute_agent(agent_id, task)
    return {"result": result}