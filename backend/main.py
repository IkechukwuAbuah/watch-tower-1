"""
Watch Tower - Fleet Management System
Main FastAPI application
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import os
import asyncio
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import routers
from api import trips, trucks, analytics, webhooks, admin, ai

# Import models to register them with Base
from models import Truck, Trip, VehiclePosition

# Import database initialization
from db.session import init_db

# Import Redis and event sourcing
from db.redis import health_check as redis_health_check, close_redis_pool
from events import EventPublisher, EventConsumer, EventType
from events.publisher import event_publisher
from events.handlers import (
    PositionUpdateHandler,
    TripStatusHandler,
    AlertHandler,
    WebhookReceivedHandler,
    ErrorHandler,
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handle startup and shutdown events"""
    # Startup
    logger.info("🚀 Starting Watch Tower API...")
    
    # Initialize database
    logger.info("📊 Initializing database...")
    try:
        await init_db()
        logger.info("✅ Database initialized successfully")
    except Exception as e:
        logger.error(f"❌ Database initialization failed: {e}")
        raise
    
    # Initialize Redis
    logger.info("🔴 Initializing Redis...")
    try:
        if await redis_health_check():
            logger.info("✅ Redis connection established")
            
            # Create consumer groups for all event types
            for event_type in EventType:
                await event_publisher.create_consumer_group(
                    event_type.value,
                    "watch_tower_consumers"
                )
        else:
            logger.warning("⚠️ Redis connection failed - events will not be processed")
    except Exception as e:
        logger.error(f"❌ Redis initialization failed: {e}")
        # Don't fail startup - app can work without Redis
    
    # Store event consumer for graceful shutdown
    app.state.event_consumer = None
    
    # Start event consumers in background (optional)
    if await redis_health_check():
        try:
            consumer = EventConsumer("api_consumer")
            group = consumer.create_group("watch_tower_consumers")
            
            # Register handlers
            group.register_handler(EventType.POSITION_UPDATED, PositionUpdateHandler())
            group.register_handler(EventType.TRIP_STATUS_CHANGED, TripStatusHandler())
            group.register_handler(EventType.ALERT_TRIGGERED, AlertHandler())
            group.register_handler(EventType.WEBHOOK_RECEIVED, WebhookReceivedHandler())
            group.register_handler(EventType.ERROR_OCCURRED, ErrorHandler())
            
            # Start consumer in background
            app.state.event_consumer = consumer
            app.state.consumer_task = asyncio.create_task(consumer.start_all())
            
            logger.info("✅ Event consumers started")
        except Exception as e:
            logger.error(f"Failed to start event consumers: {e}")
    
    yield
    
    # Shutdown
    logger.info("👋 Shutting down Watch Tower API...")
    
    # Stop event consumers
    if app.state.event_consumer:
        app.state.event_consumer.stop_all()
        if hasattr(app.state, 'consumer_task'):
            app.state.consumer_task.cancel()
            try:
                await app.state.consumer_task
            except asyncio.CancelledError:
                pass
    
    # Close Redis connections
    await close_redis_pool()
    
    logger.info("✅ Shutdown complete")

# Create FastAPI app
app = FastAPI(
    title="Watch Tower API",
    description="Fleet Management System for VPC",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure properly for production
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint with component status"""
    health_status = {
        "status": "healthy",
        "service": "watch-tower",
        "components": {
            "database": "healthy",  # Assumed healthy if app started
            "redis": "unknown"
        }
    }
    
    # Check Redis
    try:
        if await redis_health_check():
            health_status["components"]["redis"] = "healthy"
        else:
            health_status["components"]["redis"] = "unhealthy"
            health_status["status"] = "degraded"
    except Exception:
        health_status["components"]["redis"] = "error"
        health_status["status"] = "degraded"
    
    return health_status

# Include routers
app.include_router(trips.router, prefix="/api/v1/trips", tags=["trips"])
app.include_router(trucks.router, prefix="/api/v1/trucks", tags=["trucks"])
app.include_router(analytics.router, prefix="/api/v1/analytics", tags=["analytics"])
app.include_router(webhooks.router, prefix="/api/v1/webhooks", tags=["webhooks"])
app.include_router(admin.router, prefix="/api/v1/admin", tags=["admin"])
app.include_router(ai.router, prefix="/api/v1")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
