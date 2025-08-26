from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ...core.database import get_db
from ...models.database import User
from ...schemas.agent import Agent, AgentCreate, AgentUpdate, TaskExecutionRequest
from ...services.agent_service import AgentService
from ...services.user_service import UserService

router = APIRouter()

@router.get("/", response_model=List[Agent])
async def list_agents(
    db: Session = Depends(get_db),
    current_user: User = Depends(UserService.get_current_active_user)
) -> Any:
    """List all agents for the current user"""
    agents = await AgentService.list_agents(db=db, user_id=current_user.id)
    return agents

@router.post("/", response_model=Agent)
async def create_agent(
    agent_in: AgentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(UserService.get_current_active_user)
) -> Any:
    """Create a new agent"""
    agent = await AgentService.create_agent(
        db=db, 
        agent_data=agent_in, 
        user_id=current_user.id
    )
    return agent

@router.get("/{agent_id}", response_model=Agent)
async def get_agent(
    agent_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(UserService.get_current_active_user)
) -> Any:
    """Get a specific agent by ID"""
    agent = await AgentService.get_agent(db=db, agent_id=agent_id)
    if not agent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Agent not found"
        )
    
    # Check if user owns this agent
    if agent.user_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    return agent

@router.put("/{agent_id}", response_model=Agent)
async def update_agent(
    agent_id: str,
    agent_update: AgentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(UserService.get_current_active_user)
) -> Any:
    """Update an existing agent"""
    # Check if agent exists and user owns it
    agent = await AgentService.get_agent(db=db, agent_id=agent_id)
    if not agent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Agent not found"
        )
    
    if agent.user_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    agent = await AgentService.update_agent(
        db=db, 
        agent_id=agent_id, 
        agent_update=agent_update
    )
    return agent

@router.delete("/{agent_id}")
async def delete_agent(
    agent_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(UserService.get_current_active_user)
) -> Any:
    """Delete an agent"""
    # Check if agent exists and user owns it
    agent = await AgentService.get_agent(db=db, agent_id=agent_id)
    if not agent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Agent not found"
        )
    
    if agent.user_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    success = await AgentService.delete_agent(db=db, agent_id=agent_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete agent"
        )
    
    return {"message": "Agent deleted successfully"}

@router.post("/{agent_id}/execute")
async def execute_agent(
    agent_id: str,
    task: TaskExecutionRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(UserService.get_current_active_user)
) -> Any:
    """Execute a task using the specified agent"""
    # Check if agent exists and user owns it
    agent = await AgentService.get_agent(db=db, agent_id=agent_id)
    if not agent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Agent not found"
        )
    
    if agent.user_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    try:
        result = await AgentService.execute_agent(
            db=db,
            agent_id=agent_id,
            task=task.dict(),
            user_id=current_user.id
        )
        return result
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Execution failed: {str(e)}"
        )