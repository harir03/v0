from fastapi import APIRouter, HTTPException, Depends
from typing import List, Dict, Any
from app.schemas.agent import Agent, AgentCreate, AgentUpdate
from app.services.agent_service import AgentService
from app.core.security import require_auth, rate_limit, validate_input, log_security_event

router = APIRouter()

@router.get("/", response_model=List[Agent])
async def list_agents(current_user: Dict[str, Any] = Depends(require_auth)):
    """Get all agents for the current user"""
    log_security_event("list_agents", current_user.get("sub"))
    return await AgentService.list_agents(user_id=current_user.get("sub"))

@router.post("/", response_model=Agent)
async def create_agent(agent: AgentCreate, current_user: Dict[str, Any] = Depends(require_auth)):
    """Create a new agent"""
    # Input validation and sanitization
    agent_data = validate_input(
        agent.dict(),
        required_fields=["name", "type"],
        max_lengths={"name": 100, "description": 500}
    )
    
    log_security_event("create_agent", current_user.get("sub"), {"agent_name": agent_data.get("name")})
    
    # Create agent with user context
    return await AgentService.create_agent(agent, user_id=current_user.get("sub"))

@router.get("/{agent_id}", response_model=Agent)
async def get_agent(agent_id: str, current_user: Dict[str, Any] = Depends(require_auth)):
    """Get a specific agent by ID"""
    agent = await AgentService.get_agent(agent_id, user_id=current_user.get("sub"))
    if not agent:
        log_security_event("agent_access_denied", current_user.get("sub"), {"agent_id": agent_id})
        raise HTTPException(status_code=404, detail="Agent not found")
    return agent

@router.put("/{agent_id}", response_model=Agent)
async def update_agent(agent_id: str, agent_update: AgentUpdate, current_user: Dict[str, Any] = Depends(require_auth)):
    """Update an existing agent"""
    # Input validation
    update_data = validate_input(
        agent_update.dict(exclude_unset=True),
        max_lengths={"name": 100, "description": 500}
    )
    
    agent = await AgentService.update_agent(agent_id, agent_update, user_id=current_user.get("sub"))
    if not agent:
        log_security_event("agent_update_denied", current_user.get("sub"), {"agent_id": agent_id})
        raise HTTPException(status_code=404, detail="Agent not found")
    
    log_security_event("agent_updated", current_user.get("sub"), {"agent_id": agent_id})
    return agent

@router.delete("/{agent_id}")
async def delete_agent(agent_id: str, current_user: Dict[str, Any] = Depends(require_auth)):
    """Delete an agent"""
    success = await AgentService.delete_agent(agent_id, user_id=current_user.get("sub"))
    if not success:
        log_security_event("agent_delete_denied", current_user.get("sub"), {"agent_id": agent_id})
        raise HTTPException(status_code=404, detail="Agent not found")
    
    log_security_event("agent_deleted", current_user.get("sub"), {"agent_id": agent_id})
    return {"message": "Agent deleted successfully"}

@router.post("/{agent_id}/execute")
async def execute_agent(agent_id: str, task: dict, current_user: Dict[str, Any] = Depends(require_auth)):
    """Execute a task using the specified agent (async execution)"""
    # Validate task input
    task_data = validate_input(
        task,
        required_fields=["type"],
        max_lengths={"description": 1000, "input": 5000}
    )
    
    log_security_event("agent_execution_started", current_user.get("sub"), {
        "agent_id": agent_id,
        "task_type": task_data.get("type")
    })
    
    result = await AgentService.execute_agent(agent_id, task_data, user_id=current_user.get("sub"))
    
    log_security_event("agent_execution_submitted", current_user.get("sub"), {
        "agent_id": agent_id,
        "task_id": result.get("task_id"),
        "task_type": task_data.get("type")
    })
    
    return {"result": result}

@router.get("/tasks/{task_id}")
async def get_task_status(task_id: str, current_user: Dict[str, Any] = Depends(require_auth)):
    """Get the status of an async task"""
    task_status = await AgentService.get_task_status(task_id, user_id=current_user.get("sub"))
    if not task_status:
        raise HTTPException(status_code=404, detail="Task not found")
    return task_status

@router.get("/execution/queue-status")
async def get_queue_status(current_user: Dict[str, Any] = Depends(require_auth)):
    """Get execution queue status"""
    return await AgentService.get_execution_queue_status()