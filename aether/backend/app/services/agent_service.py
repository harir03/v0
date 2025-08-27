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
    async def create_agent(cls, agent_data, user_id: str) -> Dict[str, Any]:
        """Create a new agent"""
        agent_id = str(uuid.uuid4())
        agent = {
            "id": agent_id,
            "name": agent_data.name,
            "description": agent_data.description,
            "type": agent_data.type,
            "configuration": agent_data.configuration,
            "status": "inactive",
            "user_id": user_id,
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
        if user_id:
            return [agent for agent in cls._agents.values() if agent.get("user_id") == user_id]
        return list(cls._agents.values())
    
    @classmethod
    async def get_agent(cls, agent_id: str, user_id: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """Get a specific agent by ID"""
        agent = cls._agents.get(agent_id)
        if agent and user_id and agent.get("user_id") != user_id:
            return None  # Don't allow access to other users' agents
        return agent
    
    @classmethod
    async def update_agent(cls, agent_id: str, agent_update, user_id: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """Update an existing agent"""
        if agent_id not in cls._agents:
            return None
        
        agent = cls._agents[agent_id]
        
        # Check user ownership
        if user_id and agent.get("user_id") != user_id:
            return None
        
        update_data = agent_update.dict(exclude_unset=True)
        
        for field, value in update_data.items():
            if value is not None:
                agent[field] = value
        
        agent["updated_at"] = datetime.utcnow().isoformat()
        return agent
    
    @classmethod
    async def delete_agent(cls, agent_id: str, user_id: Optional[str] = None) -> bool:
        """Delete an agent"""
        if agent_id not in cls._agents:
            return False
        
        agent = cls._agents[agent_id]
        
        # Check user ownership
        if user_id and agent.get("user_id") != user_id:
            return False
        
        del cls._agents[agent_id]
        return True
    
    @classmethod
    async def execute_agent(cls, agent_id: str, task: Dict[str, Any], user_id: Optional[str] = None) -> Dict[str, Any]:
        """Execute a task using the specified agent"""
        agent = cls._agents.get(agent_id)
        if not agent:
            raise ValueError(f"Agent {agent_id} not found")
        
        # Check user ownership
        if user_id and agent.get("user_id") != user_id:
            raise ValueError(f"Agent {agent_id} not accessible")
        
        # Update execution statistics
        agent["execution_count"] += 1
        agent["last_execution"] = datetime.utcnow().isoformat()
        agent["status"] = "active"
        
        # Simulate agent execution (improved async handling)
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