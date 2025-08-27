"""
Improved async agent execution system with background processing
"""
import asyncio
import uuid
from datetime import datetime
from typing import Dict, Any, Optional
from enum import Enum
import json

class TaskStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class TaskResult:
    def __init__(self, task_id: str, agent_id: str, task_data: Dict[str, Any], user_id: str):
        self.task_id = task_id
        self.agent_id = agent_id
        self.task_data = task_data
        self.user_id = user_id
        self.status = TaskStatus.PENDING
        self.result: Optional[Dict[str, Any]] = None
        self.error: Optional[str] = None
        self.created_at = datetime.utcnow()
        self.started_at: Optional[datetime] = None
        self.completed_at: Optional[datetime] = None

class AgentExecutionEngine:
    """Improved agent execution engine with async processing and queuing"""
    
    def __init__(self, max_concurrent_tasks: int = 10):
        self.max_concurrent_tasks = max_concurrent_tasks
        self.task_queue: asyncio.Queue = asyncio.Queue()
        self.active_tasks: Dict[str, TaskResult] = {}
        self.completed_tasks: Dict[str, TaskResult] = {}
        self.running_tasks: int = 0
        self._workers_started = False
        
    async def start_workers(self):
        """Start background worker tasks"""
        if self._workers_started:
            return
        
        self._workers_started = True
        # Start worker coroutines
        for i in range(self.max_concurrent_tasks):
            asyncio.create_task(self._worker(f"worker-{i}"))
    
    async def _worker(self, worker_name: str):
        """Background worker that processes tasks from the queue"""
        while True:
            try:
                task_result = await self.task_queue.get()
                await self._execute_task(task_result)
                self.task_queue.task_done()
            except Exception as e:
                print(f"Worker {worker_name} error: {e}")
                await asyncio.sleep(1)  # Brief pause before retrying
    
    async def _execute_task(self, task_result: TaskResult):
        """Execute a single agent task"""
        task_result.status = TaskStatus.RUNNING
        task_result.started_at = datetime.utcnow()
        self.running_tasks += 1
        
        try:
            from app.services.agent_service import AgentService
            
            # Get agent details
            agent = AgentService._agents.get(task_result.agent_id)
            if not agent:
                raise ValueError(f"Agent {task_result.agent_id} not found")
            
            # Check user access
            if agent.get("user_id") != task_result.user_id:
                raise ValueError(f"Agent {task_result.agent_id} not accessible")
            
            # Update agent status
            agent["status"] = "active"
            agent["execution_count"] += 1
            agent["last_execution"] = datetime.utcnow().isoformat()
            
            # Simulate more realistic agent processing with varying delays
            processing_time = self._calculate_processing_time(agent, task_result.task_data)
            await asyncio.sleep(processing_time)
            
            # Generate result based on agent type and task
            result = await self._generate_agent_result(agent, task_result.task_data)
            
            # Update task result
            task_result.status = TaskStatus.COMPLETED
            task_result.result = result
            task_result.completed_at = datetime.utcnow()
            
            # Update agent status
            agent["status"] = "inactive"
            
        except Exception as e:
            task_result.status = TaskStatus.FAILED
            task_result.error = str(e)
            task_result.completed_at = datetime.utcnow()
            
        finally:
            self.running_tasks -= 1
            # Move to completed tasks
            self.completed_tasks[task_result.task_id] = task_result
            if task_result.task_id in self.active_tasks:
                del self.active_tasks[task_result.task_id]
    
    def _calculate_processing_time(self, agent: Dict[str, Any], task_data: Dict[str, Any]) -> float:
        """Calculate realistic processing time based on agent type and task complexity"""
        base_time = 0.5  # Base processing time
        
        # Adjust based on agent type
        agent_type = agent.get("type", "custom")
        type_multipliers = {
            "coding": 2.0,
            "data_analysis": 1.5,
            "customer_support": 0.8,
            "workflow": 1.2,
            "automation": 1.0
        }
        
        multiplier = type_multipliers.get(agent_type, 1.0)
        
        # Adjust based on task complexity (simplified)
        task_complexity = len(task_data.get("description", "")) / 100.0  # Rough complexity measure
        complexity_factor = min(task_complexity, 2.0)  # Cap at 2x
        
        return base_time * multiplier * (1 + complexity_factor)
    
    async def _generate_agent_result(self, agent: Dict[str, Any], task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate result based on agent type and task"""
        agent_type = agent.get("type", "custom")
        task_type = task_data.get("type", "unknown")
        
        if agent_type == "customer_support":
            return {
                "response": f"I've analyzed the {task_type} inquiry and generated a professional response.",
                "confidence": 0.92,
                "sentiment": "neutral",
                "actions_taken": [
                    "analyzed_sentiment",
                    "searched_knowledge_base",
                    "generated_response",
                    "applied_brand_guidelines"
                ],
                "response_time_ms": 847
            }
        elif agent_type == "coding":
            return {
                "code_generated": f"// Generated code for {task_type}\\nfunction handle{task_type.title()}() {{\\n  // Implementation here\\n  return 'Task completed successfully';\\n}}",
                "language": "javascript",
                "confidence": 0.89,
                "code_quality_score": 0.94,
                "security_issues": [],
                "performance_score": 0.88
            }
        elif agent_type == "data_analysis":
            return {
                "analysis_type": task_type,
                "insights_found": 7,
                "data_points_processed": 1547,
                "anomalies_detected": 2,
                "confidence": 0.91,
                "recommendations": [
                    "Increase monitoring frequency",
                    "Optimize data collection process",
                    "Review anomaly patterns"
                ]
            }
        elif agent_type == "automation":
            return {
                "automation_created": True,
                "workflow_steps": 5,
                "estimated_time_saved": "2.5 hours per week",
                "success_rate": 0.96,
                "actions_automated": [
                    "data_collection",
                    "validation",
                    "processing",
                    "notification",
                    "archival"
                ]
            }
        else:
            return {
                "message": f"Task '{task_type}' executed successfully by {agent['name']}",
                "task_type": task_type,
                "status": "completed",
                "agent_type": agent_type,
                "execution_time": datetime.utcnow().isoformat()
            }
    
    async def submit_task(self, agent_id: str, task_data: Dict[str, Any], user_id: str) -> str:
        """Submit a task for async execution"""
        task_id = str(uuid.uuid4())
        task_result = TaskResult(task_id, agent_id, task_data, user_id)
        
        self.active_tasks[task_id] = task_result
        
        # Start workers if not already started
        await self.start_workers()
        
        # Add to queue
        await self.task_queue.put(task_result)
        
        return task_id
    
    def get_task_status(self, task_id: str) -> Optional[Dict[str, Any]]:
        """Get status of a task"""
        # Check active tasks
        if task_id in self.active_tasks:
            task = self.active_tasks[task_id]
            return {
                "task_id": task_id,
                "status": task.status.value,
                "created_at": task.created_at.isoformat(),
                "started_at": task.started_at.isoformat() if task.started_at else None,
                "completed_at": task.completed_at.isoformat() if task.completed_at else None,
                "result": task.result,
                "error": task.error
            }
        
        # Check completed tasks
        if task_id in self.completed_tasks:
            task = self.completed_tasks[task_id]
            return {
                "task_id": task_id,
                "status": task.status.value,
                "created_at": task.created_at.isoformat(),
                "started_at": task.started_at.isoformat() if task.started_at else None,
                "completed_at": task.completed_at.isoformat() if task.completed_at else None,
                "result": task.result,
                "error": task.error
            }
        
        return None
    
    def get_queue_status(self) -> Dict[str, Any]:
        """Get overall queue status"""
        return {
            "queued_tasks": self.task_queue.qsize(),
            "active_tasks": len(self.active_tasks),
            "running_tasks": self.running_tasks,
            "completed_tasks": len(self.completed_tasks),
            "max_concurrent": self.max_concurrent_tasks
        }

# Global execution engine instance
execution_engine = AgentExecutionEngine(max_concurrent_tasks=5)