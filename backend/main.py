"""
Watch Tower - Fleet Management System
Main FastAPI application
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import routers
from api import trips, trucks, analytics, webhooks, admin

# Import models to register them with Base
from models import Truck, Trip, VehiclePosition

# Import database initialization
from db.session import init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handle startup and shutdown events"""
    # Startup
    print("🚀 Starting Watch Tower API...")
    print("📊 Initializing database...")
    try:
        await init_db()
        print("✅ Database initialized successfully")
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        raise
    
    yield
    
    # Shutdown
    print("👋 Shutting down Watch Tower API...")

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
    return {"status": "healthy", "service": "watch-tower"}

# Include routers
app.include_router(trips.router, prefix="/api/v1/trips", tags=["trips"])
app.include_router(trucks.router, prefix="/api/v1/trucks", tags=["trucks"])
app.include_router(analytics.router, prefix="/api/v1/analytics", tags=["analytics"])
app.include_router(webhooks.router, prefix="/api/v1/webhooks", tags=["webhooks"])
app.include_router(admin.router, prefix="/api/v1/admin", tags=["admin"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
