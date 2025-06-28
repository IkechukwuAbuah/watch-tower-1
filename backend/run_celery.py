#!/usr/bin/env python3
"""
Celery worker startup script for Watch Tower
"""

import os
import sys
from celery_app import celery_app

if __name__ == "__main__":
    # Set environment for Celery
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "")
    
    # Start Celery worker
    if len(sys.argv) > 1 and sys.argv[1] == "beat":
        # Start beat scheduler
        celery_app.start([
            "celery", "beat", 
            "--loglevel=info",
            "--scheduler=redbeat.RedBeatScheduler"
        ])
    else:
        # Start worker
        celery_app.start([
            "celery", "worker", 
            "--loglevel=info",
            "--concurrency=2",
            "--pool=prefork",
            "--max-tasks-per-child=1000"
        ])