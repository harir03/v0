from celery import Celery
from .config import settings

# Configure Celery
celery_app = Celery(
    "aether-agents",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
    include=['app.tasks.agent_tasks']
)

# Celery configuration
celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
    task_track_started=True,
    task_acks_late=True,
    worker_prefetch_multiplier=1,
    result_expires=3600,  # 1 hour
    broker_connection_retry_on_startup=True,
)

# Task routing
celery_app.conf.task_routes = {
    'app.tasks.agent_tasks.execute_agent_task': {'queue': 'agent_execution'},
    'app.tasks.agent_tasks.process_agent_workflow': {'queue': 'workflows'},
    'app.tasks.billing_tasks.*': {'queue': 'billing'},
}

# Beat schedule for periodic tasks
celery_app.conf.beat_schedule = {
    'cleanup-expired-executions': {
        'task': 'app.tasks.maintenance_tasks.cleanup_expired_executions',
        'schedule': 300.0,  # Every 5 minutes
    },
    'update-subscription-usage': {
        'task': 'app.tasks.billing_tasks.update_subscription_usage',
        'schedule': 3600.0,  # Every hour
    },
}