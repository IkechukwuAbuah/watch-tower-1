# Watch Tower - Fleet Tracking System Technical Proposal

## What problem are you trying to solve?

VPC operates 84+ container trucks in Lagos, Nigeria, using LocoNav for GPS tracking. Currently, our operations team faces significant friction in daily fleet management tasks:

- **Trip creation takes 10-15 minutes** per trip through LocoNav's complex UI
- **Fleet visibility requires multiple clicks** to answer simple questions like "where is truck T11985LA?"
- **Performance reporting is inconsistent**, with managers manually compiling data from multiple sources
- **Critical alerts get lost** in email/SMS, lacking context and actionability

We need a unified, intelligent interface that simplifies fleet operations while maintaining the robust tracking capabilities of LocoNav.

## 📖 Background

### Current State
- **Fleet Size**: 84 trucks across 4 operators (VPC, FM, LH, PC)
- **Daily Operations**: ~45 container trips between ESSLIBRA terminal and client locations
- **Data Sources**: 
  - LocoNav (GPS tracking, trip management, geofencing)
  - Google Sheets (master data for trucks, drivers, clients, locations)
  - Manual tracking sheets for trip progress

### Pain Points Observed
1. Operations team spends 2+ hours daily on repetitive data entry
2. Delayed response to trip delays due to poor alert visibility  
3. Management lacks real-time fleet utilization metrics
4. Customer complaints about shipment visibility

### Previous Attempts
- Excel macros for reporting (broke frequently)
- WhatsApp groups for alerts (too noisy, no context)
- Direct LocoNav access for all team members (too complex)

## 🤷🏿‍♂️ Why should we solve it?

### Quantitative Impact
- **Time Savings**: 2.5 hours/day × 5 operators = 12.5 hours daily
- **Trip Creation**: Reduce from 15 min to 2 min = 85% improvement
- **Response Time**: Alert to action from 45 min to 5 min
- **Revenue Impact**: 20% more trips possible with optimized TAT

### Qualitative Impact
- **Team Morale**: Reduce frustration with repetitive tasks
- **Decision Making**: Real-time data for better resource allocation
- **Customer Satisfaction**: Proactive delay notifications
- **Competitive Advantage**: Faster turnaround than competitors

### Cost of Inaction
- Losing 1-2 trips per truck monthly due to inefficiency
- Risk of losing contracts to more tech-enabled competitors
- Growing operational costs as fleet expands

## 📓 Requirements

### Core Problem
Our fleet operations team needs a conversational interface to manage trips and monitor trucks without navigating complex UIs or switching between multiple systems.

### Functional Requirements
1. **Natural Language Fleet Queries**
   - "Where is truck T11985LA?"
   - "Which trucks are at ESSLIBRA terminal?"
   - "Show delays in the last 24 hours"

2. **Simplified Trip Creation**
   - Create trips via Slack: "Create trip T28737LA from ESSLIBRA to ECLAT tomorrow 8am"
   - Auto-populate from master data
   - Validate truck availability

3. **Proactive Intelligence**
   - Alert on trip delays (2+ hours after scheduled departure)
   - Geofence entry/exit notifications during active trips
   - Daily/weekly performance summaries

4. **Data Synchronization**
   - Bi-directional sync with Google Sheets (15-min intervals)
   - Real-time GPS data from LocoNav
   - Historical data retention (6 months)

### Non-Functional Requirements
- Response time < 2 seconds for queries
- 99.5% uptime for critical services
- Support Lagos timezone (Africa/Lagos)
- Mobile-friendly interfaces

### What are you not trying to solve?
- Route optimization (drivers know best routes)
- Customer billing integration
- Driver performance scoring
- Maintenance scheduling
- Fuel management

## 👨🏿‍🔧 Technical Overview

### Architecture Overview
```
┌─────────────────┐     ┌──────────────┐     ┌─────────────┐
│   Slack Bot     │────▶│  FastAPI     │────▶│  Supabase   │
│   Interface     │     │  Backend     │     │  Database   │
└─────────────────┘     └──────┬───────┘     └─────────────┘
                               │
                    ┌──────────┴──────────┐
                    │                     │
              ┌─────▼──────┐      ┌──────▼──────┐
              │  LocoNav    │      │   Google    │
              │    API      │      │   Sheets    │
              └────────────┘      └─────────────┘
```

### Major Components

1. **Slack Bot (Primary Interface)**
   - Natural language command parser
   - Real-time notifications
   - Interactive responses

2. **API Gateway (FastAPI)**
   - RESTful endpoints
   - WebSocket for real-time updates
   - Authentication & rate limiting

3. **AI Service (OpenAI GPT-4)**
   - Natural language understanding
   - Command extraction
   - Response generation

4. **Integration Layer**
   - LocoNav API client
   - Google Sheets sync service
   - Webhook handlers

5. **Data Layer (Supabase)**
   - PostgreSQL database
   - Real-time subscriptions
   - Row-level security

6. **Background Workers (Celery)**
   - Scheduled data sync
   - Alert processing
   - Report generation

## 💬 API

### Core Endpoints

```yaml
# Trip Management
POST /api/v1/trips
{
  "truck_number": "T11985LA",
  "pickup_location": "ESSLIBRA",
  "delivery_location": "ECLAT", 
  "scheduled_departure": "2025-04-02T08:00:00+01:00"
}

Response:
{
  "trip_id": "vpc-2025-04-02-001",
  "loconav_trip_id": "trip_12345",
  "status": "scheduled",
  "tracking_url": "https://track.vpc.ng/t/vpc-2025-04-02-001"
}

# Fleet Status
GET /api/v1/trucks/{truck_number}/location
Response:
{
  "truck_number": "T11985LA",
  "current_location": {
    "coordinates": [3.3792, 6.5244],
    "address": "ESSLIBRA Terminal, Ibeshe",
    "geofence": "ESSLIBRA"
  },
  "status": "idle",
  "last_update": "2025-04-01T14:30:00+01:00",
  "driver": "Moruf Fatai"
}

# Analytics
GET /api/v1/analytics/daily
Response:
{
  "date": "2025-04-01",
  "metrics": {
    "total_trips": 45,
    "completed_trips": 42,
    "average_tat_hours": 28.5,
    "fleet_utilization": 78.5,
    "delays": 3
  },
  "by_fleet": {
    "VPC": { "trips": 20, "utilization": 85 },
    "FM": { "trips": 15, "utilization": 75 }
  }
}
```

## 💽 Data Model

### Core Tables

```sql
-- Trucks (synced from Sheets)
CREATE TABLE trucks (
    id UUID PRIMARY KEY,
    truck_number VARCHAR(50) UNIQUE NOT NULL,
    loconav_vehicle_id VARCHAR(100),
    company VARCHAR(100),
    status VARCHAR(50),
    INDEX idx_truck_number (truck_number)
);

-- Trips (operational data)
CREATE TABLE trips (
    id UUID PRIMARY KEY,
    vpc_id VARCHAR(100) UNIQUE,
    loconav_trip_id VARCHAR(100),
    truck_id UUID REFERENCES trucks(id),
    pickup_location_id UUID,
    delivery_location_id UUID,
    status VARCHAR(50),
    scheduled_departure TIMESTAMP,
    actual_departure TIMESTAMP,
    INDEX idx_status_schedule (status, scheduled_departure)
);

-- Vehicle Positions (time-series)
CREATE TABLE vehicle_positions (
    truck_id UUID,
    timestamp TIMESTAMP,
    coordinates POINT,
    speed DECIMAL(5,2),
    PRIMARY KEY (truck_id, timestamp)
) PARTITION BY RANGE (timestamp);
```

### Data Access Patterns
- **High-frequency reads**: Current truck locations (cached)
- **Write-heavy**: GPS positions (5-min intervals)
- **Analytics**: Daily aggregations (materialized views)

## 🎒 Backend

### New Services

1. **LocoNav Integration Service**
   - Trip CRUD operations
   - Real-time location polling
   - Webhook processing

2. **Sheets Sync Service**  
   - Bi-directional sync every 15 minutes
   - Conflict resolution
   - Change detection

3. **AI Command Service**
   - Natural language parsing
   - Intent classification
   - Response generation

### API Structure
```
backend/
├── api/v1/
│   ├── trips.py
│   ├── trucks.py
│   └── analytics.py
├── services/
│   ├── loconav.py
│   ├── sheets.py
│   └── ai.py
└── workers/
    ├── sync.py
    └── alerts.py
```

## 🕸️ Web

### Phase 1: Slack-Only
No web interface initially. All interactions via Slack bot.

### Phase 3: Dashboard
- Mobile-first React dashboard
- Real-time trip tracking
- Performance metrics
- No complex mapping (users have LocoNav)

## 💽 Data and Event Logging

### Key Events

```json
{
  "event": "trip_created",
  "timestamp": "2025-04-01T08:00:00Z",
  "data": {
    "trip_id": "vpc-2025-04-01-001",
    "truck": "T11985LA",
    "user": "operations@vpc.ng",
    "method": "slack_command"
  }
}
```

### Metrics to Track
- Command usage by type
- Trip creation time (manual vs automated)
- Alert response times
- API latency percentiles
- Sync success rates

## ☣️ Risks and Failure

### Technical Risks

1. **LocoNav API Limits**
   - Risk: Rate limiting (500/min)
   - Mitigation: Request queuing, caching

2. **Google Sheets Sync Conflicts**
   - Risk: Concurrent edits
   - Mitigation: Last-write-wins + audit log

3. **AI Misinterpretation**
   - Risk: Wrong trip parameters
   - Mitigation: Confirmation before creation

### Operational Risks

1. **User Adoption**
   - Risk: Team prefers old methods
   - Mitigation: Training, champion users

2. **Data Quality**
   - Risk: Incorrect master data
   - Mitigation: Validation rules, alerts

### Infrastructure Risks

1. **Service Outages**
   - Risk: Slack/LocoNav downtime
   - Mitigation: Fallback to direct access

## 🥼 Testing

### Automated Testing
- Unit tests: 80% coverage target
- Integration tests: Critical paths
- Load testing: 100 concurrent users

### Manual Testing
- User acceptance: Operations team
- Edge cases: Network issues, conflicts
- Performance: Peak hours simulation

### Test Scenarios
1. Create 50 trips in 5 minutes
2. Handle conflicting truck assignments
3. Process 1000 GPS updates/minute
4. Recover from service outages

## 📉 Graceful Degradation

### Service Dependencies
```
Critical Path:
Slack → API → Database → LocoNav

Degradation Strategy:
- Slack down: Direct API access
- LocoNav down: Cached data (5 min)
- Database down: Read replicas
- AI down: Template responses
```

### Traffic Patterns
- Peak: 7-9 AM (trip creation)
- Steady: 9 AM - 6 PM (monitoring)
- Low: Night hours

### Capacity Planning
- 100 trips/day initially
- 500 GPS updates/minute
- 50 concurrent Slack users

## 📈 Monitoring and Observability

### Key Metrics

```yaml
User-Impact Alerts:
- No trips created for 2 hours (business hours)
- Sync failures for 30+ minutes
- Command response time > 5 seconds
- Failed trip creations > 10%

System Health:
- API latency p95 < 2s
- Database connections < 80%
- Queue depth < 1000
- Error rate < 1%
```

### Dashboards
1. Operations Dashboard
   - Active trips
   - Fleet utilization
   - Recent alerts

2. System Dashboard
   - API performance
   - Integration status
   - Error rates

## 🔐 Security

### Data Classification
- **Sensitive**: Driver phone numbers, client details
- **Internal**: Trip data, truck locations
- **Public**: Tracking URLs

### Security Measures
- API authentication (JWT tokens)
- Encryption at rest (Supabase)
- TLS for all communications
- Row-level security for multi-tenant data
- Audit logging for all actions

### Access Control
- Read: All VPC staff
- Write: Operations team
- Admin: System administrators

## ❓What do you still not know?

### Blocking Questions
1. What's the LocoNav API rate limit for our account?
2. Which Google account owns the master sheets?
3. What's the Slack workspace setup process?
4. Database hosting preference (Supabase region)?

### Non-Blocking Questions
1. Future integration needs (billing, maintenance)?
2. Desired analytics beyond basic metrics?
3. Multi-language support requirements?
4. Expansion plans affecting scale?

### Technical Uncertainties
1. LocoNav webhook reliability
2. Sheets API quota limits
3. GPS update frequency needs
4. Historical data migration approach

## 🚀 Implementation Plan

### Phase 1 (Weeks 1-2): Foundation
- Database setup
- Basic API structure
- LocoNav integration
- Simple Slack commands

### Phase 2 (Weeks 3-4): Intelligence
- AI command parsing
- Google Sheets sync
- Alert system
- Analytics engine

### Phase 3 (Month 2): Enhancement
- Web dashboard
- Advanced analytics
- Performance optimization
- User training

### Success Criteria
- 50% reduction in trip creation time
- 90% user adoption within 1 month
- 99.5% uptime after stabilization
- Positive ROI within 6 months
