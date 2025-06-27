# Claude Code Project Context - Watch Tower Fleet Management System

## Project Overview

You are helping build Watch Tower, a fleet management system for Virgo Point Capital (VPC) that tracks 84+ container trucks in Lagos, Nigeria. The system integrates with LocoNav GPS tracking and uses AI to provide natural language interfaces for fleet operations.

## Your Working Directory
```
~/Downloads/watch-tower-experiments/watch-tower-1/
```

## Key Project Goals

1. **Simplify Trip Creation**: Reduce time to create trips from complex LocoNav UI to simple natural language commands
2. **Real-time Fleet Visibility**: Answer "where is truck X?" instantly via Slack
3. **Automated Reporting**: Daily/weekly performance summaries
4. **Data Integration**: Sync Google Sheets master data with operational database

## Technical Stack You'll Use

- **Backend**: Python 3.11, FastAPI, SQLAlchemy, Celery
- **Database**: PostgreSQL (via Supabase)
- **AI**: OpenAI GPT-4 for natural language
- **Integrations**: LocoNav API, Google Sheets API, Slack Bot
- **Frontend**: React + TypeScript (Phase 3)

## Available Resources

### 1. LocoNav API Documentation
Location: `docs/loconav/loconav-docs.md`

Key endpoints you'll use:
- `POST /trips` - Create trips
- `POST /vehicles/telematics/last_known` - Get vehicle locations
- `GET /polygons` - List geofences
- Webhooks for alerts and live locations

Authentication: `User-Authentication` header with token

### 2. OpenAI Documentation
Location: `docs/open-ai/`

Relevant guides:
- `oai-function-calling.md` - For structured data extraction
- `oai-structured-output.md` - For JSON responses
- `oai-agents.md` - For building the AI assistant

### 3. Google Sheets
- Trucks Sheet: `1hgoDIV0yuYFZLraAXFgTFRLven-NKXD9UV5sW2QKLuU`
- Trips Sheet: `1CbfTUKS3lcj498M-9wH3FNolzipMNY4zWyGZjFeXm4k`

### 4. Supabase Access
You have MCP access to Supabase. Current projects are inactive but you can:
- Create new project for development
- Use SQL to create tables per schema in `TECHNICAL_ARCHITECTURE.md`

## Core Features to Implement

### Phase 1: Backend Foundation (Current Focus)

1. **Database Schema Setup**
   - Create tables: trucks, drivers, locations, trips, vehicle_positions
   - Set up indexes for performance
   - Configure RLS policies

2. **Google Sheets Sync Service**
   - Read truck/driver data every 15 minutes
   - Sync client and terminal locations
   - Handle data conflicts gracefully

3. **LocoNav Integration**
   - Implement authentication
   - Create trip creation service
   - Set up webhook handlers
   - Poll vehicle locations (5 min intervals)

4. **Slack Bot Commands**
   ```
   @vpc-tracker where is T11985LA
   @vpc-tracker create trip T28737LA from ESSLIBRA to ECLAT tomorrow 8am
   @vpc-tracker trucks at terminals
   @vpc-tracker daily summary
   ```

### Phase 2: AI Integration

1. **Natural Language Parser**
   - Extract trip details from commands
   - Understand location queries
   - Generate human-friendly responses

2. **Smart Trip Creation**
   - Map location names to geofence IDs
   - Validate truck availability
   - Set appropriate timings

3. **Analytics Engine**
   - Calculate TAT (Turnaround Time)
   - Generate daily summaries
   - Track fleet utilization

## Implementation Guidelines

### 1. Error Handling
```python
# Always wrap external API calls
try:
    result = await loconav_client.create_trip(data)
except Exception as e:
    logger.error(f"LocoNav error: {e}")
    # Fallback or retry logic
```

### 2. Timezone Handling
```python
# Always use Lagos timezone
from zoneinfo import ZoneInfo
lagos_tz = ZoneInfo('Africa/Lagos')
```

### 3. Data Validation
- Truck numbers format: `T\d+LA` (e.g., T11985LA)
- Container numbers: `[A-Z]{4}\d{7}` (e.g., TCNU3877560)
- Coordinates: Decimal degrees format

### 4. API Rate Limits
- LocoNav: 500 requests/minute
- Google Sheets: 100 requests/100 seconds
- Implement caching and request queuing

## Project Structure to Create

```
backend/
├── api/
│   ├── __init__.py
│   ├── trips.py        # Trip endpoints
│   ├── trucks.py       # Fleet endpoints
│   └── analytics.py    # Metrics endpoints
├── services/
│   ├── loconav_service.py
│   ├── sheets_service.py
│   ├── ai_service.py
│   └── analytics_service.py
├── models/
│   ├── __init__.py
│   ├── truck.py
│   ├── trip.py
│   └── location.py
├── schemas/
│   ├── __init__.py
│   └── trip.py
├── tasks.py           # Celery tasks
├── main.py           # FastAPI app
└── requirements.txt

slack-bot/
├── app.py
├── handlers/
└── commands/

scripts/
├── init_db.py
├── sync_sheets.py
└── test_loconav.py
```

## Environment Variables Needed

```bash
# Create .env file with:
LOCONAV_API_BASE_URL=https://api.a.loconav.com
LOCONAV_USER_TOKEN=<get from user>
SUPABASE_URL=<from your project>
SUPABASE_KEY=<from your project>
OPENAI_API_KEY=<get from user>
SLACK_BOT_TOKEN=<get from user>
GOOGLE_SHEETS_CREDENTIALS_JSON=<service account JSON>
```

## Testing Approach

1. **Unit Tests**: Test individual services
2. **Integration Tests**: Test API endpoints
3. **Manual Testing**: Use provided test scripts
4. **Slack Testing**: Create test workspace

## Common Patterns

### 1. Async Service Pattern
```python
class BaseService:
    async def __aenter__(self):
        self.client = httpx.AsyncClient()
        return self
    
    async def __aexit__(self, *args):
        await self.client.aclose()
```

### 2. Repository Pattern
```python
class TruckRepository:
    def __init__(self, db: Database):
        self.db = db
    
    async def get_by_number(self, truck_number: str):
        # Implementation
```

### 3. Response Models
```python
from pydantic import BaseModel

class TruckLocation(BaseModel):
    truck_number: str
    coordinates: tuple[float, float]
    timestamp: datetime
    status: str
```

## Key Business Rules

1. **Trip Creation**:
   - Must have valid pickup and delivery geofences
   - Scheduled time must be in future
   - Truck must be operational

2. **Alerts**:
   - Only track geofence entry/exit during active trips
   - Delay alert triggered 2 hours after scheduled departure

3. **Data Sync**:
   - Google Sheets is source of truth for master data
   - LocoNav is source of truth for real-time data

## Development Workflow

1. Start with database schema setup
2. Implement basic CRUD operations
3. Add LocoNav integration
4. Build Slack bot incrementally
5. Add AI features last
6. Test each component thoroughly

## Questions to Ask User

1. Do you have the LocoNav API token?
2. Should I create a new Supabase project or use existing?
3. Do you have Slack workspace setup with bot?
4. Do you have Google Cloud service account for Sheets?
5. What's the OpenAI API key for GPT-4 access?

## Remember

- This is a real business system for truck operations
- Reliability is more important than fancy features
- Start simple, iterate based on user feedback
- Lagos timezone (UTC+1) for all operations
- Focus on Slack interface first, web UI comes later

Ready to start building! What would you like to implement first?
