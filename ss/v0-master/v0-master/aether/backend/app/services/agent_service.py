from typing import List, Optional, Dict, Any
import uuid
import json
import asyncio
from datetime import datetime

class AgentService:
    """Service for managing AI agents"""
    
    # In-memory storage for demo purposes
    # In production, this would use a database
    _agents: Dict[str, Dict] = {}
    
    @classmethod
    async def create_agent(cls, agent_data) -> Dict[str, Any]:
        """Create a new agent"""
        agent_id = str(uuid.uuid4())
        agent = {
            "id": agent_id,
            "name": agent_data.name,
            "description": agent_data.description,
            "type": agent_data.type,
            "configuration": agent_data.configuration,
            "status": "inactive",
            "user_id": "demo_user",  # TODO: Get from authentication
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
            "execution_count": 0,
            "last_execution": None
        }
        cls._agents[agent_id] = agent
        return agent
    
    @classmethod
    async def list_agents(cls, user_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """List all agents for a user"""
        # Filter by user_id in production
        return list(cls._agents.values())
    
    @classmethod
    async def get_agent(cls, agent_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific agent by ID"""
        return cls._agents.get(agent_id)
    
    @classmethod
    async def update_agent(cls, agent_id: str, agent_update) -> Optional[Dict[str, Any]]:
        """Update an existing agent"""
        if agent_id not in cls._agents:
            return None
        
        agent = cls._agents[agent_id]
        update_data = agent_update.dict(exclude_unset=True)
        
        for field, value in update_data.items():
            if value is not None:
                agent[field] = value
        
        agent["updated_at"] = datetime.utcnow().isoformat()
        return agent
    
    @classmethod
    async def delete_agent(cls, agent_id: str) -> bool:
        """Delete an agent"""
        if agent_id in cls._agents:
            del cls._agents[agent_id]
            return True
        return False
    
    @classmethod
    async def execute_agent(cls, agent_id: str, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a task using the specified agent"""
        agent = cls._agents.get(agent_id)
        if not agent:
            raise ValueError(f"Agent {agent_id} not found")
        
        # Update execution statistics
        agent["execution_count"] += 1
        agent["last_execution"] = datetime.utcnow().isoformat()
        agent["status"] = "active"
        
        # Simulate agent execution
        await asyncio.sleep(1)  # Simulate processing time
        
        # Mock response based on agent type
        if agent["type"] == "customer_support":
            result = {
                "response": "I've analyzed the customer inquiry and generated a response.",
                "confidence": 0.95,
                "actions_taken": ["analyzed_sentiment", "searched_knowledge_base", "generated_response"]
            }
        elif agent["type"] == "coding":
            result = {
                "code_generated": "// Example generated code\nfunction handleTask() {\n  return 'Task completed';\n}",
                "language": "javascript",
                "confidence": 0.88
            }
        else:
            result = {
                "message": f"Task executed by {agent['name']}",
                "task_type": task.get("type", "unknown"),
                "status": "completed"
            }
        
        agent["status"] = "inactive"
        return result