import uuid
import asyncio
from datetime import datetime
from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session

from ..models.database import Agent, AgentExecution, User
from ..schemas.agent import AgentCreate, AgentUpdate
from ..core.database import get_db

class AgentService:
    """Service for managing AI agents with database persistence"""
    
    @classmethod
    async def create_agent(
        cls, 
        db: Session, 
        agent_data: AgentCreate, 
        user_id: str
    ) -> Agent:
        """Create a new agent"""
        agent = Agent(
            id=str(uuid.uuid4()),
            name=agent_data.name,
            description=agent_data.description,
            type=agent_data.type,
            configuration=agent_data.configuration,
            status="inactive",
            user_id=user_id,
            execution_count=0,
            last_execution=None
        )
        db.add(agent)
        db.commit()
        db.refresh(agent)
        return agent
    
    @classmethod
    async def list_agents(
        cls, 
        db: Session, 
        user_id: Optional[str] = None
    ) -> List[Agent]:
        """List all agents for a user"""
        query = db.query(Agent)
        if user_id:
            query = query.filter(Agent.user_id == user_id)
        return query.all()
    
    @classmethod
    async def get_agent(cls, db: Session, agent_id: str) -> Optional[Agent]:
        """Get a specific agent by ID"""
        return db.query(Agent).filter(Agent.id == agent_id).first()
    
    @classmethod
    async def update_agent(
        cls, 
        db: Session, 
        agent_id: str, 
        agent_update: AgentUpdate
    ) -> Optional[Agent]:
        """Update an existing agent"""
        agent = db.query(Agent).filter(Agent.id == agent_id).first()
        if not agent:
            return None
        
        update_data = agent_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(agent, field, value)
        
        agent.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(agent)
        return agent
    
    @classmethod
    async def delete_agent(cls, db: Session, agent_id: str) -> bool:
        """Delete an agent"""
        agent = db.query(Agent).filter(Agent.id == agent_id).first()
        if not agent:
            return False
        
        db.delete(agent)
        db.commit()
        return True
    
    @classmethod
    async def execute_agent(
        cls, 
        db: Session, 
        agent_id: str, 
        task: Dict[str, Any],
        user_id: str,
        async_execution: bool = True
    ) -> Dict[str, Any]:
        """Execute a task using the specified agent"""
        from ..tasks.agent_tasks import execute_agent_task
        from ..services.monitoring import monitoring_service
        
        agent = db.query(Agent).filter(Agent.id == agent_id).first()
        if not agent:
            raise ValueError(f"Agent {agent_id} not found")
        
        # Create execution record
        execution = AgentExecution(
            id=str(uuid.uuid4()),
            agent_id=agent_id,
            user_id=user_id,
            task_input=task,
            status="pending"
        )
        db.add(execution)
        db.commit()
        db.refresh(execution)
        
        # Log the execution start
        monitoring_service.log_user_activity(
            user_id=user_id,
            action="execute_agent",
            resource_type="agent",
            resource_id=agent_id,
            metadata={"execution_id": execution.id}
        )
        
        if async_execution:
            # Execute asynchronously using Celery
            task_result = execute_agent_task.delay(
                agent_id=agent_id,
                execution_id=execution.id,
                task_input=task
            )
            
            return {
                "execution_id": execution.id,
                "task_id": task_result.id,
                "status": "queued",
                "message": "Agent execution queued for processing"
            }
        else:
            # Execute synchronously (for testing/debugging)
            try:
                start_time = datetime.utcnow()
                
                # Update execution status
                execution.status = "running"
                agent.status = "active"
                db.commit()
                
                # Simple mock execution for synchronous mode
                await asyncio.sleep(1)  # Simulate processing time
                
                result = {
                    "message": f"Task executed by {agent.name}",
                    "task_type": task.get("type", "unknown"),
                    "status": "completed",
                    "execution_mode": "synchronous"
                }
                
                # Update execution with results
                end_time = datetime.utcnow()
                execution_time = (end_time - start_time).total_seconds() * 1000
                
                execution.task_output = result
                execution.status = "completed"
                execution.execution_time_ms = int(execution_time)
                execution.completed_at = end_time
                
                # Update agent statistics
                agent.execution_count += 1
                agent.last_execution = datetime.utcnow()
                agent.status = "inactive"
                
                db.commit()
                
                # Log successful execution
                monitoring_service.log_agent_execution(
                    agent_id=agent_id,
                    agent_type=agent.type,
                    status="completed",
                    duration=execution_time / 1000,
                    user_id=user_id
                )
                
                return result
                
            except Exception as e:
                # Handle execution error
                execution.status = "failed"
                execution.error_message = str(e)
                execution.completed_at = datetime.utcnow()
                agent.status = "error"
                
                db.commit()
                
                # Log failed execution
                monitoring_service.log_agent_execution(
                    agent_id=agent_id,
                    agent_type=agent.type,
                    status="failed",
                    duration=0,
                    user_id=user_id,
                    error=str(e)
                )
                
                raise e
    
    @classmethod
    async def get_execution_status(
        cls,
        db: Session,
        execution_id: str
    ) -> Optional[AgentExecution]:
        """Get the status of an agent execution"""
        return db.query(AgentExecution).filter(
            AgentExecution.id == execution_id
        ).first()