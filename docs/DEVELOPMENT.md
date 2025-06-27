# Watch Tower - Development Guide

## 🚀 Getting Started with Claude Code & Cursor

This guide is optimized for development with Claude Code and Cursor, taking into account AI model knowledge cutoffs and providing all necessary context.

## 📁 Project Structure

```
~/Downloads/watch-tower-experiments/watch-tower-1/
├── backend/
│   ├── api/              # API endpoints
│   ├── services/         # Business logic
│   ├── models/           # Database models
│   ├── schemas/          # Pydantic schemas
│   ├── utils/            # Helper functions
│   ├── tests/            # Test files
│   ├── main.py          # FastAPI app entry
│   └── requirements.txt  # Python dependencies
├── slack-bot/
│   ├── handlers/         # Slack event handlers
│   ├── commands/         # Slash commands
│   └── app.py           # Slack app setup
├── scripts/
│   ├── sync_sheets.py    # Google Sheets sync
│   ├── init_db.py       # Database setup
│   └── test_loconav.py   # API testing
├── docs/
│   ├── loconav/          # LocoNav API docs
│   └── open-ai/          # OpenAI guides
└── .env.example          # Environment template
```

## 🔧 Initial Setup

### 1. Environment Configuration

Create `.env` file in the root directory:

```bash
# LocoNav API
LOCONAV_API_BASE_URL=https://api.a.loconav.com
LOCONAV_USER_TOKEN=your_token_here

# Supabase
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your_anon_key_here
SUPABASE_SERVICE_KEY=your_service_key_here

# OpenAI
OPENAI_API_KEY=your_openai_key_here

# Google Sheets
GOOGLE_SHEETS_CREDENTIALS_JSON='{...}' # Service account JSON
TRUCKS_SHEET_ID=1hgoDIV0yuYFZLraAXFgTFRLven-NKXD9UV5sW2QKLuU
TRIPS_SHEET_ID=1CbfTUKS3lcj498M-9wH3FNolzipMNY4zWyGZjFeXm4k

# Slack
SLACK_BOT_TOKEN=xoxb-your-token
SLACK_APP_TOKEN=xapp-your-token

# Timezone
TZ=Africa/Lagos
```

### 2. Database Setup with Supabase

```python
# scripts/init_db.py
import os
from supabase import create_client

# Initialize Supabase client
supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_SERVICE_KEY")
)

# Run this script to create tables
# python scripts/init_db.py
```

### 3. Virtual Environment Setup

```bash
# Create virtual environment
python3 -m venv venv

# Activate (Linux/Mac)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## 🏗️ Core Implementation Guide

### 1. FastAPI Backend Structure

```python
# backend/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import uvicorn

from api import trips, trucks, analytics
from services.sync_service import start_sync_scheduler

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await start_sync_scheduler()
    yield
    # Shutdown
    
app = FastAPI(
    title="Watch Tower API",
    version="1.0.0",
    lifespan=lifespan
)

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(trips.router, prefix="/api/v1/trips", tags=["trips"])
app.include_router(trucks.router, prefix="/api/v1/trucks", tags=["trucks"])
app.include_router(analytics.router, prefix="/api/v1/analytics", tags=["analytics"])

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
```

### 2. LocoNav Service Implementation

```python
# backend/services/loconav_service.py
import httpx
from typing import Dict, List, Optional
from datetime import datetime
import os

class LocoNavService:
    def __init__(self):
        self.base_url = os.getenv("LOCONAV_API_BASE_URL")
        self.auth_token = os.getenv("LOCONAV_USER_TOKEN")
        self.headers = {
            "User-Authentication": self.auth_token,
            "Content-Type": "application/json"
        }
    
    async def create_trip(self, trip_data: Dict) -> Dict:
        """Create a trip in LocoNav"""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/integration/api/v1/trips",
                json={"trip": trip_data},
                headers=self.headers
            )
            response.raise_for_status()
            return response.json()
    
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
```

### 3. AI Service for Natural Language

```python
# backend/services/ai_service.py
from openai import AsyncOpenAI
import json
from typing import Dict, Any
import os

class AIService:
    def __init__(self):
        self.client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
    async def parse_trip_command(self, command: str) -> Dict:
        """Parse natural language trip creation command"""
        
        system_prompt = """
        You are a fleet management assistant. Parse trip creation commands and extract:
        - truck_number
        - pickup_location 
        - delivery_location
        - scheduled_time (in ISO format)
        
        Return as JSON.
        
        Example:
        Input: "Create trip for T28737LA from ESSLIBRA to ECLAT tomorrow 8am"
        Output: {
            "truck_number": "T28737LA",
            "pickup_location": "ESSLIBRA",
            "delivery_location": "ECLAT",
            "scheduled_time": "2024-04-02T08:00:00+01:00"
        }
        """
        
        response = await self.client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": command}
            ],
            response_format={"type": "json_object"}
        )
        
        return json.loads(response.choices[0].message.content)
```

### 4. Google Sheets Sync Service

```python
# backend/services/sheets_service.py
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
from typing import List, Dict
import json
import os

class SheetsService:
    def __init__(self):
        creds_dict = json.loads(os.getenv("GOOGLE_SHEETS_CREDENTIALS_JSON"))
        creds = Credentials.from_service_account_info(
            creds_dict,
            scopes=['https://www.googleapis.com/auth/spreadsheets']
        )
        self.gc = gspread.authorize(creds)
        
    async def sync_trucks(self) -> List[Dict]:
        """Sync truck data from Google Sheets"""
        sheet = self.gc.open_by_key(os.getenv("TRUCKS_SHEET_ID"))
        worksheet = sheet.worksheet("Trucks & Drivers")
        
        # Get all records
        records = worksheet.get_all_records()
        
        # Transform to our schema
        trucks = []
        for record in records:
            if record.get('Truck Number'):
                trucks.append({
                    'truck_number': record['Truck Number'],
                    'loconav_reg_id': record.get('Loconav Reg ID'),
                    'company': record.get('Company'),
                    'fleet_manager': record.get('Fleet Manager'),
                    'status': record.get('Truck State', 'operational'),
                    'brand': record.get('Brand'),
                    'trailer_size': record.get('Trailer Size'),
                    'driver_name': record.get('Driver Name'),
                    'driver_phone': record.get('Driver Phone Number')
                })
        
        return trucks
```

### 5. Slack Bot Implementation

```python
# slack-bot/app.py
from slack_bolt.async_app import AsyncApp
from slack_bolt.adapter.socket_mode.async_handler import AsyncSocketModeHandler
import os
import re

app = AsyncApp(
    token=os.getenv("SLACK_BOT_TOKEN"),
    signing_secret=os.getenv("SLACK_SIGNING_SECRET")
)

@app.message(re.compile("where is", re.IGNORECASE))
async def handle_location_query(message, say):
    """Handle truck location queries"""
    text = message['text']
    
    # Extract truck number
    truck_match = re.search(r'T\d+LA', text, re.IGNORECASE)
    if not truck_match:
        await say("Please specify a truck number (e.g., T11985LA)")
        return
    
    truck_number = truck_match.group().upper()
    
    # Get location from backend
    location = await get_truck_location(truck_number)
    
    if location:
        await say(f"🚛 *{truck_number}* is currently at:\n"
                 f"📍 {location['address']}\n"
                 f"🚦 Status: {location['status']}\n"
                 f"⏱️ Last update: {location['timestamp']}")
    else:
        await say(f"Unable to find location for {truck_number}")

# Start bot
async def main():
    handler = AsyncSocketModeHandler(app, os.getenv("SLACK_APP_TOKEN"))
    await handler.start_async()
```

## 🧪 Testing

### 1. Test LocoNav Connection

```python
# scripts/test_loconav.py
import asyncio
from services.loconav_service import LocoNavService

async def test_connection():
    service = LocoNavService()
    
    # Test vehicle list
    vehicles = await service.list_vehicles()
    print(f"Found {len(vehicles)} vehicles")
    
    # Test location for first vehicle
    if vehicles:
        location = await service.get_vehicle_location(vehicles[0]['id'])
        print(f"Location: {location}")

if __name__ == "__main__":
    asyncio.run(test_connection())
```

### 2. Test Database Connection

```python
# scripts/test_db.py
from supabase import create_client
import os

# Test Supabase connection
supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_KEY")
)

# Try to fetch trucks
result = supabase.table('trucks').select("*").limit(5).execute()
print(f"Trucks in database: {len(result.data)}")
```

## 🚀 Running the Application

### Development Mode

```bash
# Terminal 1: Backend
cd backend
uvicorn main:app --reload --port 8000

# Terminal 2: Slack Bot
cd slack-bot
python app.py

# Terminal 3: Celery Worker (for background tasks)
cd backend
celery -A tasks worker --loglevel=info

# Terminal 4: Celery Beat (for scheduled tasks)
cd backend
celery -A tasks beat --loglevel=info
```

### Docker Compose (Recommended)

```yaml
# docker-compose.yml
version: '3.8'

services:
  api:
    build: ./backend
    ports:
      - "8000:8000"
    env_file: .env
    depends_on:
      - redis
      
  slack-bot:
    build: ./slack-bot
    env_file: .env
    depends_on:
      - api
      
  worker:
    build: ./backend
    command: celery -A tasks worker --loglevel=info
    env_file: .env
    depends_on:
      - redis
      
  beat:
    build: ./backend  
    command: celery -A tasks beat --loglevel=info
    env_file: .env
    depends_on:
      - redis
      
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
```

## 📝 Common Development Tasks

### 1. Adding a New API Endpoint

```python
# backend/api/trips.py
from fastapi import APIRouter, HTTPException
from typing import List
from schemas.trip import TripCreate, TripResponse

router = APIRouter()

@router.post("/", response_model=TripResponse)
async def create_trip(trip: TripCreate):
    """Create a new trip"""
    # Implementation here
    pass
```

### 2. Adding a New Slack Command

```python
# slack-bot/commands/trip_commands.py
@app.command("/vpc-trip")
async def handle_trip_command(ack, command, respond):
    await ack()
    
    # Parse command text
    # Call backend API
    # Respond to user
    await respond(f"Trip created successfully!")
```

### 3. Adding a Background Task

```python
# backend/tasks.py
from celery import Celery

celery_app = Celery('watch_tower')

@celery_app.task
def sync_google_sheets():
    """Sync data from Google Sheets"""
    # Implementation
    pass

# Schedule in beat_schedule
celery_app.conf.beat_schedule = {
    'sync-sheets': {
        'task': 'tasks.sync_google_sheets',
        'schedule': 900.0,  # 15 minutes
    },
}
```

## 🐛 Debugging Tips

### 1. Enable Debug Logging

```python
# backend/utils/logging.py
import logging
import sys

def setup_logging():
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )
```

### 2. API Testing with HTTPie

```bash
# Test trip creation
http POST localhost:8000/api/v1/trips \
  truck_number=T11985LA \
  pickup_location=ESSLIBRA \
  delivery_location=ECLAT

# Get truck location
http GET localhost:8000/api/v1/trucks/T11985LA/location
```

### 3. Database Queries

```sql
-- Check recent trips
SELECT * FROM trips 
WHERE created_at > NOW() - INTERVAL '1 day'
ORDER BY created_at DESC;

-- Check truck locations
SELECT t.truck_number, vp.timestamp, vp.coordinates
FROM trucks t
JOIN vehicle_positions vp ON t.id = vp.truck_id
WHERE vp.timestamp > NOW() - INTERVAL '1 hour';
```

## 📚 Key References

### API Documentation
- LocoNav API: `docs/loconav/loconav-docs.md`
- OpenAI Best Practices: `docs/open-ai/oai-agents.md`

### External Resources
- FastAPI: https://fastapi.tiangolo.com/
- Supabase Python: https://supabase.com/docs/reference/python/introduction
- Slack Bolt: https://slack.dev/bolt-python/

## 🤖 Working with AI Models

### Knowledge Cutoff Considerations

When using Claude Code or Cursor, remember:

1. **LocoNav API**: Full documentation is in `docs/loconav/`
2. **Google Sheets IDs**: Hardcoded in `.env`
3. **Timezone**: Always use `Africa/Lagos`
4. **Supabase**: Using latest Python client (2.x)

### Prompting for Code Generation

Example prompt for Claude Code:
```
"Create a FastAPI endpoint to get all trucks currently at terminals. 
Use the Supabase client to query the trucks and locations tables. 
Filter by location type = 'terminal' and join with current positions.
Return truck number, terminal name, and time at location."
```

## 🚨 Troubleshooting

### Common Issues

1. **LocoNav API 401**: Check auth token in `.env`
2. **Supabase connection**: Verify URL and keys
3. **Slack not responding**: Check app/bot tokens
4. **Google Sheets sync fails**: Verify service account permissions

### Error Handling Pattern

```python
from fastapi import HTTPException
import logging

logger = logging.getLogger(__name__)

async def safe_api_call():
    try:
        result = await external_api_call()
        return result
    except httpx.HTTPStatusError as e:
        logger.error(f"API error: {e.response.status_code}")
        raise HTTPException(
            status_code=503,
            detail="External service unavailable"
        )
    except Exception as e:
        logger.exception("Unexpected error")
        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )
```
