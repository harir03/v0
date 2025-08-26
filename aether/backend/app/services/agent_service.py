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
        user_id: str
    ) -> Dict[str, Any]:
        """Execute a task using the specified agent"""
        agent = db.query(Agent).filter(Agent.id == agent_id).first()
        if not agent:
            raise ValueError(f"Agent {agent_id} not found")
        
        # Create execution record
        execution = AgentExecution(
            id=str(uuid.uuid4()),
            agent_id=agent_id,
            user_id=user_id,
            task_input=task,
            status="running"
        )
        db.add(execution)
        
        # Update agent statistics
        agent.execution_count += 1
        agent.last_execution = datetime.utcnow()
        agent.status = "active"
        
        db.commit()
        
        try:
            # Simulate agent execution
            start_time = datetime.utcnow()
            await asyncio.sleep(1)  # Simulate processing time
            
            # Mock response based on agent type
            if agent.type == "customer_support":
                result = {
                    "response": "I've analyzed the customer inquiry and generated a response.",
                    "confidence": 0.95,
                    "actions_taken": [
                        "analyzed_sentiment", 
                        "searched_knowledge_base", 
                        "generated_response"
                    ]
                }
            elif agent.type == "coding":
                result = {
                    "code_generated": "// Example generated code\\nfunction handleTask() {\\n  return 'Task completed';\\n}",
                    "language": "javascript",
                    "confidence": 0.88
                }
            elif agent.type == "workflow":
                result = {
                    "workflow_steps": [
                        {"step": 1, "action": "process_input", "status": "completed"},
                        {"step": 2, "action": "analyze_data", "status": "completed"},
                        {"step": 3, "action": "generate_output", "status": "completed"}
                    ],
                    "output": {"processed": True, "result": "Workflow executed successfully"}
                }
            else:
                result = {
                    "message": f"Task executed by {agent.name}",
                    "task_type": task.get("type", "unknown"),
                    "status": "completed"
                }
            
            # Update execution with results
            end_time = datetime.utcnow()
            execution_time = (end_time - start_time).total_seconds() * 1000
            
            execution.task_output = result
            execution.status = "completed"
            execution.execution_time_ms = int(execution_time)
            execution.completed_at = end_time
            
            agent.status = "inactive"
            
            db.commit()
            db.refresh(execution)
            
            return result
            
        except Exception as e:
            # Handle execution error
            execution.status = "failed"
            execution.error_message = str(e)
            execution.completed_at = datetime.utcnow()
            agent.status = "error"
            
            db.commit()
            raise e