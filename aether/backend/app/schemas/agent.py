from pydantic import BaseModel, Field
from typing import Optional, Dict, List, Any
from datetime import datetime
from enum import Enum

class AgentType(str, Enum):
    WORKFLOW = "workflow"
    CODING = "coding"
    CUSTOMER_SUPPORT = "customer_support"
    DATA_ANALYSIS = "data_analysis"
    AUTOMATION = "automation"
    COMMUNICATION = "communication"
    ANALYSIS = "analysis"
    CUSTOM = "custom"

class AgentStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    TRAINING = "training"
    ERROR = "error"

class AgentBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    type: AgentType
    configuration: Dict[str, Any] = Field(default_factory=dict)
    
class AgentCreate(AgentBase):
    pass

class AgentUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    configuration: Optional[Dict[str, Any]] = None
    status: Optional[AgentStatus] = None

class Agent(AgentBase):
    id: str
    user_id: str
    status: AgentStatus = AgentStatus.INACTIVE
    created_at: datetime
    updated_at: datetime
    last_execution: Optional[datetime] = None
    execution_count: int = 0
    
    class Config:
        from_attributes = True