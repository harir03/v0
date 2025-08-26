from sqlalchemy import Column, String, DateTime, Integer, JSON, Text, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    subscription_tier = Column(String, default="hobbyist")  # hobbyist, startup, scaleup, enterprise
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    agents = relationship("Agent", back_populates="owner")
    interfaces = relationship("Interface", back_populates="creator")

class Agent(Base):
    __tablename__ = "agents"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    description = Column(Text)
    type = Column(String, nullable=False)  # workflow, coding, customer_support, etc.
    status = Column(String, default="inactive")  # active, inactive, training, error
    configuration = Column(JSON, default=dict)
    execution_count = Column(Integer, default=0)
    last_execution = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Foreign Keys
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    
    # Relationships
    owner = relationship("User", back_populates="agents")
    executions = relationship("AgentExecution", back_populates="agent")

class Interface(Base):
    __tablename__ = "interfaces"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    prompt = Column(Text, nullable=False)
    html = Column(Text)
    css = Column(Text)
    javascript = Column(Text)
    components = Column(JSON, default=dict)
    refinements = Column(JSON, default=list)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Foreign Keys
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    
    # Relationships
    creator = relationship("User", back_populates="interfaces")

class AgentExecution(Base):
    __tablename__ = "agent_executions"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    task_input = Column(JSON)
    task_output = Column(JSON)
    status = Column(String, default="pending")  # pending, running, completed, failed
    execution_time_ms = Column(Integer)
    error_message = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True))
    
    # Foreign Keys
    agent_id = Column(String, ForeignKey("agents.id"), nullable=False)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    
    # Relationships
    agent = relationship("Agent", back_populates="executions")

class Subscription(Base):
    __tablename__ = "subscriptions"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    tier = Column(String, nullable=False)  # hobbyist, startup, scaleup, enterprise
    status = Column(String, default="active")  # active, cancelled, expired
    monthly_tasks_used = Column(Integer, default=0)
    monthly_task_limit = Column(Integer, default=500)
    billing_cycle_start = Column(DateTime(timezone=True))
    billing_cycle_end = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())