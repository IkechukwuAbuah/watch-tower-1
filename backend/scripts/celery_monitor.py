#!/usr/bin/env python3
"""
Celery monitoring and management script
"""

import asyncio
import redis
from celery import Celery
from datetime import datetime, timedelta
from core.config import settings

# Connect to Redis
redis_client = redis.from_url(settings.celery_broker_url)

# Connect to Celery
celery_app = Celery(broker=settings.celery_broker_url)


def check_celery_workers():
    """Check active Celery workers"""
    try:
        active_workers = celery_app.control.active()
        print(f"Active Workers: {len(active_workers)}")
        
        for worker_name, tasks in active_workers.items():
            print(f"  {worker_name}: {len(tasks)} active tasks")
            
        return len(active_workers) > 0
    except Exception as e:
        print(f"Error checking workers: {e}")
        return False


def check_scheduled_tasks():
    """Check scheduled tasks in beat"""
    try:
        scheduled = celery_app.control.inspect().scheduled()
        print(f"Scheduled Tasks: {len(scheduled) if scheduled else 0}")
        
        if scheduled:
            for worker, tasks in scheduled.items():
                print(f"  {worker}: {len(tasks)} scheduled")
                
    except Exception as e:
        print(f"Error checking scheduled tasks: {e}")


def check_failed_tasks():
    """Check for failed tasks"""
    try:
        # Check Redis for failed task info
        failed_keys = redis_client.keys("celery-task-meta-*")
        failed_count = 0
        
        for key in failed_keys[:10]:  # Check last 10
            task_data = redis_client.get(key)
            if task_data and b'"FAILURE"' in task_data:
                failed_count += 1
                
        print(f"Recent Failed Tasks: {failed_count}")
        
    except Exception as e:
        print(f"Error checking failed tasks: {e}")


def get_queue_stats():
    """Get queue statistics"""
    try:
        # Check default queue length
        queue_length = redis_client.llen("celery")
        print(f"Queue Length: {queue_length}")
        
        # Check if beat is running
        beat_key = "redbeat:watch_tower"
        beat_active = redis_client.exists(beat_key)
        print(f"Beat Scheduler: {'Active' if beat_active else 'Inactive'}")
        
    except Exception as e:
        print(f"Error getting queue stats: {e}")


def main():
    """Main monitoring function"""
    print("=== Watch Tower Celery Monitor ===")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Broker: {settings.celery_broker_url}")
    print()
    
    print("Worker Status:")
    workers_active = check_celery_workers()
    print()
    
    print("Task Scheduling:")
    check_scheduled_tasks()
    print()
    
    print("Queue Information:")
    get_queue_stats()
    print()
    
    print("Error Tracking:")
    check_failed_tasks()
    print()
    
    if workers_active:
        print("✅ Celery system appears healthy")
    else:
        print("❌ No active workers detected")
    
    print("\n=== End Monitor Report ===")


if __name__ == "__main__":
    main()