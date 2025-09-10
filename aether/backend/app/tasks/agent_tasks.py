import asyncio
import time
from datetime import datetime
from typing import Dict, Any
from celery import Task
from sqlalchemy.orm import Session

from ..core.celery_app import celery_app
from ..core.database import SessionLocal
from ..models.database import Agent, AgentExecution, User
from ..services.ai_providers import AIProviderService

class CallbackTask(Task):
    """Base task class with database session and error handling"""
    
    def on_success(self, retval, task_id, args, kwargs):
        """Task success callback"""
        print(f"Task {task_id} succeeded with result: {retval}")
    
    def on_failure(self, exc, task_id, args, kwargs, einfo):
        """Task failure callback"""
        print(f"Task {task_id} failed with exception: {exc}")
        
        # Update execution record with error
        db = SessionLocal()
        try:
            if len(args) >= 2:  # execution_id should be second argument
                execution_id = args[1]
                execution = db.query(AgentExecution).filter(
                    AgentExecution.id == execution_id
                ).first()
                if execution:
                    execution.status = "failed"
                    execution.error_message = str(exc)
                    execution.completed_at = datetime.utcnow()
                    db.commit()
        finally:
            db.close()

@celery_app.task(bind=True, base=CallbackTask, name='execute_agent_task')
def execute_agent_task(self, agent_id: str, execution_id: str, task_input: Dict[str, Any]) -> Dict[str, Any]:
    """Execute an agent task asynchronously"""
    db = SessionLocal()
    start_time = time.time()
    
    try:
        # Get agent and execution records
        agent = db.query(Agent).filter(Agent.id == agent_id).first()
        execution = db.query(AgentExecution).filter(AgentExecution.id == execution_id).first()
        
        if not agent:
            raise ValueError(f"Agent {agent_id} not found")
        
        if not execution:
            raise ValueError(f"Execution {execution_id} not found")
        
        # Update execution status
        execution.status = "running"
        agent.status = "active"
        db.commit()
        
        # Execute based on agent type
        if agent.type == "customer_support":
            result = execute_customer_support_agent(agent, task_input)
        elif agent.type == "coding":
            result = execute_coding_agent(agent, task_input)
        elif agent.type == "workflow":
            result = execute_workflow_agent(agent, task_input)
        elif agent.type == "data_analysis":
            result = execute_data_analysis_agent(agent, task_input)
        else:
            result = execute_generic_agent(agent, task_input)
        
        # Update execution with results
        end_time = time.time()
        execution_time = int((end_time - start_time) * 1000)
        
        execution.task_output = result
        execution.status = "completed"
        execution.execution_time_ms = execution_time
        execution.completed_at = datetime.utcnow()
        
        # Update agent statistics
        agent.execution_count += 1
        agent.last_execution = datetime.utcnow()
        agent.status = "inactive"
        
        db.commit()
        
        return result
        
    except Exception as e:
        # Update execution with error
        execution.status = "failed"
        execution.error_message = str(e)
        execution.completed_at = datetime.utcnow()
        agent.status = "error"
        
        db.commit()
        raise e
    
    finally:
        db.close()

def execute_customer_support_agent(agent: Agent, task_input: Dict[str, Any]) -> Dict[str, Any]:
    """Execute customer support agent logic"""
    config = agent.configuration or {}
    
    # Simulate customer support processing
    customer_query = task_input.get("query", "How can I help you?")
    
    # Use AI provider for response generation
    ai_service = AIProviderService()
    response = ai_service.generate_customer_response(
        query=customer_query,
        context=config.get("knowledge_base", {}),
        tone=config.get("tone", "professional")
    )
    
    return {
        "response": response,
        "confidence": 0.95,
        "actions_taken": [
            "analyzed_sentiment",
            "searched_knowledge_base", 
            "generated_response"
        ],
        "suggested_actions": [
            "escalate_to_human" if "urgent" in customer_query.lower() else "send_response"
        ]
    }

def execute_coding_agent(agent: Agent, task_input: Dict[str, Any]) -> Dict[str, Any]:
    """Execute coding agent logic"""
    config = agent.configuration or {}
    
    task_description = task_input.get("description", "")
    language = task_input.get("language", config.get("default_language", "python"))
    
    # Use AI provider for code generation
    ai_service = AIProviderService()
    generated_code = ai_service.generate_code(
        description=task_description,
        language=language,
        style=config.get("coding_style", "clean")
    )
    
    return {
        "code_generated": generated_code,
        "language": language,
        "confidence": 0.88,
        "suggestions": [
            "Add error handling",
            "Include unit tests",
            "Add documentation"
        ]
    }

def execute_workflow_agent(agent: Agent, task_input: Dict[str, Any]) -> Dict[str, Any]:
    """Execute workflow agent logic"""
    config = agent.configuration or {}
    workflow_steps = config.get("steps", [])
    
    results = []
    for i, step in enumerate(workflow_steps):
        # Simulate step execution
        step_result = {
            "step": i + 1,
            "action": step.get("action", f"step_{i+1}"),
            "status": "completed",
            "duration_ms": 100 + (i * 50),
            "output": f"Step {i+1} completed successfully"
        }
        results.append(step_result)
    
    return {
        "workflow_steps": results,
        "overall_status": "completed",
        "total_duration_ms": sum(step["duration_ms"] for step in results),
        "output": {
            "processed": True,
            "result": "Workflow executed successfully",
            "steps_completed": len(results)
        }
    }

def execute_data_analysis_agent(agent: Agent, task_input: Dict[str, Any]) -> Dict[str, Any]:
    """Execute data analysis agent logic"""
    data = task_input.get("data", [])
    analysis_type = task_input.get("analysis_type", "summary")
    
    # Simulate data analysis
    if analysis_type == "summary":
        result = {
            "summary": {
                "total_records": len(data),
                "data_types": ["numeric", "categorical"],
                "completeness": 0.95
            },
            "insights": [
                "Data quality is high",
                "No significant outliers detected",
                "Ready for further analysis"
            ]
        }
    else:
        result = {
            "analysis_type": analysis_type,
            "result": f"Analysis of {len(data)} records completed",
            "metrics": {
                "accuracy": 0.92,
                "processing_time": "2.3s"
            }
        }
    
    return result

def execute_generic_agent(agent: Agent, task_input: Dict[str, Any]) -> Dict[str, Any]:
    """Execute generic agent logic"""
    return {
        "message": f"Task executed by {agent.name}",
        "task_type": task_input.get("type", "unknown"),
        "status": "completed",
        "timestamp": datetime.utcnow().isoformat(),
        "agent_type": agent.type
    }

@celery_app.task(name='process_agent_workflow')
def process_agent_workflow(workflow_id: str, input_data: Dict[str, Any]) -> Dict[str, Any]:
    """Process a complex multi-agent workflow"""
    # This would handle complex workflows involving multiple agents
    return {
        "workflow_id": workflow_id,
        "status": "completed",
        "steps_processed": 3,
        "result": input_data
    }