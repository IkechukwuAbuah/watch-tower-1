"""
Celery application for Watch Tower background tasks
"""

from celery import Celery
from celery.schedules import crontab
from core.config import settings

# Create Celery instance
celery_app = Celery(
    "watch_tower",
    broker=settings.celery_broker_url,
    backend=settings.celery_result_backend,
    include=[
        "tasks.sync_tasks",
        "tasks.analytics_tasks", 
        "tasks.notification_tasks"
    ]
)

# Configure Celery
celery_app.conf.update(
    timezone=settings.celery_timezone,
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    task_track_started=True,
    task_time_limit=30 * 60,  # 30 minutes
    task_soft_time_limit=25 * 60,  # 25 minutes
    worker_prefetch_multiplier=1,
    worker_max_tasks_per_child=1000,
)

# Beat schedule for periodic tasks
celery_app.conf.beat_schedule = {
    # Sync Google Sheets data every 10 minutes
    "sync-google-sheets": {
        "task": "tasks.sync_tasks.sync_google_sheets_data",
        "schedule": 600.0,  # 10 minutes
    },
    
    # Generate daily analytics at 6 AM Lagos time
    "daily-analytics": {
        "task": "tasks.analytics_tasks.generate_daily_analytics",
        "schedule": crontab(hour=6, minute=0),
    },
    
    # Send daily summary at 7 AM Lagos time
    "daily-summary": {
        "task": "tasks.notification_tasks.send_daily_summary",
        "schedule": crontab(hour=7, minute=0),
    },
    
    # Clean old vehicle positions (keep last 30 days)
    "cleanup-old-positions": {
        "task": "tasks.sync_tasks.cleanup_old_positions",
        "schedule": crontab(hour=2, minute=0),  # 2 AM daily
    },
    
    # Check vehicle connection status every 5 minutes
    "check-vehicle-connectivity": {
        "task": "tasks.analytics_tasks.check_vehicle_connectivity",
        "schedule": 300.0,  # 5 minutes
    },
    
    # Weekly fleet performance report every Monday at 8 AM
    "weekly-fleet-report": {
        "task": "tasks.analytics_tasks.generate_weekly_report",
        "schedule": crontab(hour=8, minute=0, day_of_week=1),
    },
}

# Configure Redis for beat schedule persistence
if "redis" in settings.celery_broker_url:
    celery_app.conf.beat_scheduler = 'redbeat.RedBeatScheduler'
    celery_app.conf.redbeat_redis_url = settings.celery_broker_url