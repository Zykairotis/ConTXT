"""
Celery worker configuration.

This module sets up the Celery worker for background task processing,
configuring the broker, task routes, and other settings.
"""
import os
from celery import Celery

# Create Celery instance
celery_app = Celery(
    'contxt',
    broker=os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379/0'),
    backend=os.getenv('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0'),
)

# Configure Celery
celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
)

# Define task routes
celery_app.conf.task_routes = {
    'app.core.ingestion.*': {'queue': 'ingestion'},
    'app.processors.*': {'queue': 'processing'},
}

# Optional configuration based on environment
if os.getenv('DEBUG', 'false').lower() == 'true':
    celery_app.conf.update(
        task_always_eager=True,  # Execute tasks locally in debug mode
        task_eager_propagates=True,  # Propagate exceptions in eager mode
    )

# Auto-discover tasks from these modules
celery_app.autodiscover_tasks(['app.core', 'app.processors']) 