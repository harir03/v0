from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from datetime import datetime

# Agent Schemas
class AgentBase(BaseModel):
    name: str
    description: Optional[str] = None
    type: str
    configuration: Optional[Dict[str, Any]] = {}

class AgentCreate(AgentBase):
    pass

class AgentUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    type: Optional[str] = None
    configuration: Optional[Dict[str, Any]] = None

class Agent(AgentBase):
    id: str
    status: str
    execution_count: int
    last_execution: Optional[datetime]
    created_at: datetime
    updated_at: Optional[datetime]
    user_id: str

    class Config:
        from_attributes = True

# Agent Execution Schemas
class AgentExecutionBase(BaseModel):
    task_input: Optional[Dict[str, Any]] = None

class AgentExecutionCreate(AgentExecutionBase):
    agent_id: str

class AgentExecution(AgentExecutionBase):
    id: str
    task_output: Optional[Dict[str, Any]]
    status: str
    execution_time_ms: Optional[int]
    error_message: Optional[str]
    created_at: datetime
    completed_at: Optional[datetime]
    agent_id: str
    user_id: str

    class Config:
        from_attributes = True

# Task Execution Request
class TaskExecutionRequest(BaseModel):
    type: str
    data: Dict[str, Any]