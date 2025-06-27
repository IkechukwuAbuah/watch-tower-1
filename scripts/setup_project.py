#!/usr/bin/env python3
"""
Quick setup script for Watch Tower backend
Run: python scripts/setup_project.py
"""

import os
import sys
from pathlib import Path

def create_directory_structure():
    """Create the backend directory structure"""
    
    base_dir = Path.cwd()
    
    # Backend directories
    backend_dirs = [
        "backend/api",
        "backend/services", 
        "backend/models",
        "backend/schemas",
        "backend/utils",
        "backend/tests",
        "slack-bot/handlers",
        "slack-bot/commands",
        "scripts",
        "logs"
    ]
    
    for dir_path in backend_dirs:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
        print(f"✓ Created {dir_path}")
        
        # Create __init__.py for Python packages
        if "backend" in dir_path or "slack-bot" in dir_path:
            init_file = Path(dir_path) / "__init__.py"
            if not init_file.exists():
                init_file.touch()

def create_initial_files():
    """Create initial Python files with basic structure"""
    
    # Main FastAPI app
    main_content = '''"""
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
from api import trips, trucks, analytics

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handle startup and shutdown events"""
    # Startup
    print("🚀 Starting Watch Tower API...")
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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
'''
    
    with open("backend/main.py", "w") as f:
        f.write(main_content)
    print("✓ Created backend/main.py")
    
    # Basic API routers
    router_template = '''from fastapi import APIRouter, HTTPException
from typing import List

router = APIRouter()

@router.get("/")
async def list_{name}():
    """List all {name}"""
    return {{"message": "List {name} endpoint"}}

@router.post("/")
async def create_{name}():
    """Create new {name}"""
    return {{"message": "Create {name} endpoint"}}

@router.get("/{{id}}")
async def get_{name}(id: str):
    """Get specific {name}"""
    return {{"message": f"Get {name} {{id}}"}}
'''
    
    for name in ["trips", "trucks", "analytics"]:
        with open(f"backend/api/{name}.py", "w") as f:
            f.write(router_template.format(name=name))
        print(f"✓ Created backend/api/{name}.py")
    
    # LocoNav service
    loconav_service = '''"""
LocoNav API Integration Service
"""

import httpx
import os
from typing import Dict, List, Optional
from datetime import datetime

class LocoNavService:
    def __init__(self):
        self.base_url = os.getenv("LOCONAV_API_BASE_URL", "https://api.a.loconav.com")
        self.auth_token = os.getenv("LOCONAV_USER_TOKEN")
        
        if not self.auth_token:
            raise ValueError("LOCONAV_USER_TOKEN not set in environment")
            
        self.headers = {
            "User-Authentication": self.auth_token,
            "Content-Type": "application/json"
        }
    
    async def test_connection(self) -> bool:
        """Test LocoNav API connection"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/integration/api/v1/user",
                    headers=self.headers
                )
                return response.status_code == 200
        except Exception as e:
            print(f"LocoNav connection error: {e}")
            return False
    
    async def get_vehicle_location(self, vehicle_id: str) -> Dict:
        """Get current vehicle location"""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/integration/api/v1/vehicles/telematics/last_known",
                json={
                    "vehicleIds": [vehicle_id],
                    "sensors": ["gps", "ignition", "speed"]
                },
                headers=self.headers
            )
            response.raise_for_status()
            return response.json()
    
    async def create_trip(self, trip_data: Dict) -> Dict:
        """Create a new trip in LocoNav"""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/integration/api/v1/trips",
                json={"trip": trip_data},
                headers=self.headers
            )
            response.raise_for_status()
            return response.json()
'''
    
    with open("backend/services/loconav_service.py", "w") as f:
        f.write(loconav_service)
    print("✓ Created backend/services/loconav_service.py")
    
    # Database models
    models_init = '''"""
SQLAlchemy models for Watch Tower
"""

from sqlalchemy import create_engine, Column, String, Float, DateTime, Boolean, ForeignKey, DECIMAL, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid

Base = declarative_base()

class Truck(Base):
    __tablename__ = "trucks"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    truck_number = Column(String(50), unique=True, nullable=False)
    loconav_vehicle_id = Column(String(100), unique=True)
    company = Column(String(100))
    fleet_manager = Column(String(100))
    status = Column(String(50), default="operational")
    brand = Column(String(50))
    trailer_size = Column(String(20))
    operating_location = Column(String(100))
    
    # Relationships
    trips = relationship("Trip", back_populates="truck")
    positions = relationship("VehiclePosition", back_populates="truck")

class Trip(Base):
    __tablename__ = "trips"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    vpc_id = Column(String(100), unique=True)
    loconav_trip_id = Column(String(100), unique=True)
    truck_id = Column(UUID(as_uuid=True), ForeignKey("trucks.id"))
    status = Column(String(50), default="scheduled")
    
    # Relationships
    truck = relationship("Truck", back_populates="trips")

class VehiclePosition(Base):
    __tablename__ = "vehicle_positions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    truck_id = Column(UUID(as_uuid=True), ForeignKey("trucks.id"))
    timestamp = Column(DateTime, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    speed = Column(DECIMAL(5, 2))
    heading = Column(Integer)
    ignition = Column(Boolean)
    
    # Relationships
    truck = relationship("Truck", back_populates="positions")
'''
    
    with open("backend/models/__init__.py", "w") as f:
        f.write(models_init)
    print("✓ Created backend/models/__init__.py")

def create_test_script():
    """Create test script for LocoNav connection"""
    
    test_script = '''#!/usr/bin/env python3
"""
Test LocoNav API connection
Run: python scripts/test_loconav.py
"""

import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.services.loconav_service import LocoNavService
from dotenv import load_dotenv

async def main():
    # Load environment variables
    load_dotenv()
    
    print("🔍 Testing LocoNav API connection...")
    
    try:
        service = LocoNavService()
        
        # Test connection
        connected = await service.test_connection()
        if connected:
            print("✅ Successfully connected to LocoNav API!")
        else:
            print("❌ Failed to connect to LocoNav API")
            return
            
        # Test getting user info
        print("\\n📋 Testing user endpoint...")
        # Add more tests here
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
'''
    
    with open("scripts/test_loconav.py", "w") as f:
        f.write(test_script)
    os.chmod("scripts/test_loconav.py", 0o755)
    print("✓ Created scripts/test_loconav.py")

def create_docker_files():
    """Create Docker configuration files"""
    
    dockerfile = '''FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \\
    gcc \\
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY backend/ ./backend/
COPY scripts/ ./scripts/

# Set Python path
ENV PYTHONPATH=/app

# Expose port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
'''
    
    with open("Dockerfile", "w") as f:
        f.write(dockerfile)
    print("✓ Created Dockerfile")
    
    docker_compose = '''version: '3.8'

services:
  api:
    build: .
    ports:
      - "8000:8000"
    env_file:
      - .env
    volumes:
      - ./backend:/app/backend
      - ./scripts:/app/scripts
    depends_on:
      - redis
    command: uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

  worker:
    build: .
    env_file:
      - .env
    depends_on:
      - redis
    command: celery -A backend.tasks worker --loglevel=info
    volumes:
      - ./backend:/app/backend

  beat:
    build: .
    env_file:
      - .env
    depends_on:
      - redis
    command: celery -A backend.tasks beat --loglevel=info
    volumes:
      - ./backend:/app/backend

volumes:
  redis_data:
'''
    
    with open("docker-compose.yml", "w") as f:
        f.write(docker_compose)
    print("✓ Created docker-compose.yml")

def main():
    print("\n🚀 Setting up Watch Tower project structure...\n")
    
    # Create directories
    create_directory_structure()
    
    # Create initial files
    print("\n📝 Creating initial files...\n")
    create_initial_files()
    
    # Create test scripts
    print("\n🧪 Creating test scripts...\n")
    create_test_script()
    
    # Create Docker files
    print("\n🐳 Creating Docker configuration...\n")
    create_docker_files()
    
    print("\n✅ Project setup complete!")
    print("\n📋 Next steps:")
    print("1. Copy .env.example to .env and fill in your credentials")
    print("2. Create a virtual environment: python -m venv venv")
    print("3. Activate it: source venv/bin/activate (or venv\\Scripts\\activate on Windows)")
    print("4. Install dependencies: pip install -r requirements.txt")
    print("5. Test LocoNav connection: python scripts/test_loconav.py")
    print("6. Run the API: python backend/main.py")
    print("\n🎉 Happy coding!")

if __name__ == "__main__":
    main()
