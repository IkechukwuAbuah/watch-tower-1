# Watch Tower Project Briefing for Claude Code

You're building a fleet tracking system for VPC's 84 container trucks in Lagos, Nigeria. The system integrates LocoNav GPS tracking with AI-powered natural language interfaces.

## Quick Context
- **Working Directory**: `~/Downloads/watch-tower-experiments/watch-tower-1/`
- **Docs Available**: LocoNav API (`docs/loconav/`), OpenAI guides (`docs/open-ai/`)
- **Tech Stack**: Python/FastAPI backend, Supabase database, Slack bot interface
- **Goal**: Replace complex LocoNav UI with simple commands like "create trip T28737LA from ESSLIBRA to ECLAT tomorrow 8am"

## Current Phase: Backend Foundation

Build these core components:

1. **Database Setup** (Supabase PostgreSQL)
   - Tables: trucks, drivers, locations, trips, vehicle_positions
   - You have Supabase MCP access - can create new project

2. **LocoNav Integration** 
   - API docs in `docs/loconav/loconav-docs.md`
   - Key: Create trips, get vehicle locations, handle webhooks
   - Auth: `User-Authentication` header

3. **Google Sheets Sync**
   - Trucks: `1hgoDIV0yuYFZLraAXFgTFRLven-NKXD9UV5sW2QKLuU`
   - Trips: `1CbfTUKS3lcj498M-9wH3FNolzipMNY4zWyGZjFeXm4k`
   - Sync every 15 minutes

4. **Slack Bot**
   - Commands: "where is [truck]", "create trip...", "daily summary"
   - Natural language via OpenAI GPT-4

## Key Files to Reference
- `docs/PROJECT_SPECIFICATION.md` - Full requirements
- `docs/TECHNICAL_ARCHITECTURE.md` - System design  
- `docs/DEVELOPMENT.md` - Implementation guide
- `README.md` - Project overview

## Business Context
- VPC runs container trucks between ports (ESSLIBRA terminal) and client locations
- Main metrics: Truck Turnaround Time (TAT), trips per truck, delays
- Users want simple Slack commands instead of complex UIs
- Lagos timezone (Africa/Lagos) for all timestamps

## Start With
1. Create `backend/` directory structure
2. Set up FastAPI app with basic endpoints
3. Design Supabase schema
4. Test LocoNav API connection

What would you like to implement first?
