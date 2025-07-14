"""
Celery configuration for background tasks.
"""
from celery import Celery

from Backend.config.settings import settings

# Create Celery app
celery_app = Celery(
    "ai_context_builder",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
)

# Configure Celery
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=3600,  # 1 hour
    worker_max_tasks_per_child=200,
    worker_prefetch_multiplier=4,
)

# Import tasks to ensure they are registered
# This will be uncommented when we have actual tasks
# from Backend.processors.tasks import * 