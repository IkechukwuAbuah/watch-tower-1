# Watch Tower O3 Implementation Plan

## High-level Task Breakdown

### Phase 1: Foundation (Week 1) - CURRENT PHASE

#### 1. Database Models Enhancement
**Success Criteria**: All models use PostGIS geography types and async patterns

1.1 Update existing models with PostGIS types
- [ ] Modify Truck model to use geography(Point,4326) for location
- [ ] Update VehiclePosition with geography field
- [ ] Add indexes for geospatial queries

1.2 Create missing models
- [ ] Driver model with relationship to Truck
- [ ] Organization model for clients/transporters  
- [ ] DailyMetric and TruckMetric for analytics
- [ ] Event model for audit trail

1.3 Database migrations
- [ ] Create Alembic configuration
- [ ] Generate initial migrations
- [ ] Test migrations with rollback

#### 2. Pydantic Schemas Implementation
**Success Criteria**: Type-safe data validation for all endpoints

2.1 Core schemas
- [ ] TruckSchema (Create, Update, InDB, Location)
- [ ] TripSchema (Create, Update, Status, Public)
- [ ] DriverSchema (Create, Update, InDB)
- [ ] LocationSchema with GeoJSON support

2.2 Integration schemas
- [ ] LocoNavWebhook schemas
- [ ] GoogleSheetsSync schemas
- [ ] AIQuery and AIResponse schemas

#### 3. Services Layer Implementation
**Success Criteria**: All external integrations working with proper error handling

3.1 Complete LocoNav Service
- [ ] Implement all missing endpoints
- [ ] Add retry logic with exponential backoff
- [ ] Create webhook payload validators
- [ ] Add comprehensive error handling

3.2 Google Sheets Service
- [ ] Implement async Google Sheets client
- [ ] Create batch sync with rate limiting
- [ ] Add conflict resolution logic
- [ ] Implement incremental sync

3.3 Basic AI Service
- [ ] Setup OpenAI Responses API client
- [ ] Create function registry pattern
- [ ] Implement basic truck location query
- [ ] Add context management

#### 4. API Endpoints Implementation
**Success Criteria**: All endpoints return real data with <500ms response time

4.1 Truck endpoints
- [ ] GET /trucks (list with filters)
- [ ] POST /trucks (create with validation)
- [ ] GET /trucks/{id} (with current location)
- [ ] PUT /trucks/{id} (update)
- [ ] GET /trucks/{id}/location (real-time)

4.2 Trip endpoints
- [ ] POST /trips (create via LocoNav)
- [ ] GET /trips (list with status)
- [ ] PUT /trips/{id}/status
- [ ] GET /trips/{id}/tracking

4.3 Analytics endpoints
- [ ] GET /analytics/daily
- [ ] GET /analytics/trucks/{id}
- [ ] GET /analytics/tat

### Phase 2: Event Sourcing & Background Tasks (Week 2)

#### 5. Redis Streams Setup ✅ COMPLETED
**Success Criteria**: All events captured with <10ms latency ✅

5.1 Redis configuration
- [x] Setup Redis Streams consumers ✅
- [x] Create event publishers ✅
- [x] Implement consumer groups ✅
- [x] Add event replay capability ✅

5.2 Webhook ingestion
- [x] Create webhook receiver service ✅
- [x] Implement HMAC validation ✅
- [x] Add event publishing to streams ✅
- [x] Create dead letter queue ✅

#### 6. Celery Background Tasks
**Success Criteria**: Automated tasks running on schedule

6.1 Task configuration
- [ ] Setup Celery with Redis broker
- [ ] Configure Celery Beat scheduler
- [ ] Add task monitoring with Flower

6.2 Scheduled tasks
- [ ] Google Sheets sync (every 15 min)
- [ ] Daily analytics generation (6 AM Lagos)
- [ ] Trip status updates
- [ ] Alert processing

### Phase 3: AI Integration (Week 3)

#### 7. OpenAI Responses API Implementation
**Success Criteria**: Natural language queries working with 95% accuracy

7.1 Function calling setup
- [ ] Define all tool functions
- [ ] Create Pydantic models for tools
- [ ] Implement function router
- [ ] Add validation layer

7.2 Query handlers
- [ ] Truck location queries
- [ ] Trip creation commands
- [ ] Status check queries
- [ ] Analytics requests

#### 8. Slack Bot Implementation
**Success Criteria**: All commands working in Slack

8.1 Bot setup
- [ ] Configure Socket Mode
- [ ] Create slash commands
- [ ] Implement event handlers
- [ ] Add interactive components

8.2 Command implementation
- [ ] /truck command
- [ ] /trip command
- [ ] /report command
- [ ] Natural language handler

### Phase 4: Production Readiness (Week 4)

#### 9. Testing & Quality
**Success Criteria**: 80% test coverage, all critical paths tested

9.1 Unit tests
- [ ] Model tests
- [ ] Service tests
- [ ] API endpoint tests

9.2 Integration tests
- [ ] LocoNav integration
- [ ] Google Sheets sync
- [ ] End-to-end workflows

#### 10. Deployment & Monitoring
**Success Criteria**: Zero-downtime deployment, comprehensive monitoring

10.1 Infrastructure
- [ ] Docker configuration
- [ ] Environment management
- [ ] Secrets handling

10.2 Monitoring
- [ ] Structured logging setup
- [ ] Metrics collection
- [ ] Alert configuration
- [ ] Performance monitoring

## Current Status / Progress Tracking

### Week 1 Progress
- [x] Database models enhancement (PostGIS types) ✅ PR #14
- [x] Pydantic schemas ✅ PR #14
- [x] Core services (LocoNav, Google Sheets, Analytics) ✅ PR #14
- [x] API endpoints ✅ PR #14

### Week 2 Progress
- [x] Redis Streams event sourcing ✅ (Issue #8 COMPLETED)

### Blockers
- None identified yet

### Next Priority Tasks (Based on GitHub Issues)
1. ~~**Issue #8** - Set up Redis Streams for event sourcing [P0]~~ ✅ COMPLETED
2. **Issue #9** - Implement OpenAI Responses API integration [P0]
3. **Issue #7** - Create missing database models (Driver, Organization, Analytics) [P1]
4. **Issue #10** - Configure Celery for background tasks [P1]

### Next Steps
Updated priority after Redis Streams completion:
1. Implement OpenAI integration (Issue #9) - Core AI functionality [P0]
2. Configure Celery background tasks (Issue #10) - Automation [P1] 
3. Create missing database models (Issue #7) - Complete foundation [P1]

## Current Implementation: Redis Streams (Issue #8) ✅ COMPLETED

### Implementation Summary ✅
1. **Redis Connection Setup** ✅
   - Created Redis client with connection pooling ✅
   - Added Redis configuration to settings ✅
   - Implemented connection health check on startup ✅

2. **Event Schema Design** ✅
   - Defined base event structure with Pydantic schemas ✅
   - Created 8 event types (webhook_received, trip_created, position_updated, etc.) ✅
   - Implemented type-safe event serialization/deserialization ✅

3. **Publisher Implementation** ✅
   - Created EventPublisher service with XADD operations ✅
   - Added publish methods for each event type ✅
   - Implemented stream trimming and consumer group creation ✅

4. **Consumer Framework** ✅
   - Created EventConsumer base class with XREADGROUP ✅
   - Implemented consumer groups for scaling ✅
   - Added error handling and message acknowledgment ✅

5. **Integration Points** ✅
   - Webhook endpoint publishes events ✅
   - API endpoints ready for state change events ✅
   - Background event processing framework established ✅

## Next Implementation: OpenAI Responses API (Issue #9)

### Implementation Plan
1. **OpenAI Client Setup**
   - Configure OpenAI SDK with Responses API
   - Add OpenAI configuration to settings
   - Create response generation service

2. **Function Registry**
   - Define tool functions for fleet operations
   - Implement Pydantic schemas for function parameters
   - Create function router and dispatcher

3. **Query Handlers**
   - Truck location and status queries
   - Trip creation and management commands
   - Analytics and reporting requests

4. **Integration with Slack Bot**
   - Natural language command processing
   - Context management for conversations
   - Response formatting for Slack interface

## Risk Mitigation

1. **LocoNav API Reliability**: Implement circuit breaker pattern
2. **Google Sheets Quotas**: Use batch operations and caching
3. **PostGIS Complexity**: Start with simple queries, optimize later
4. **AI Accuracy**: Begin with deterministic queries, add NLP gradually

## Definition of Done

- [ ] All tests passing
- [ ] Documentation updated
- [ ] Code reviewed
- [ ] Performance benchmarks met
- [ ] Security scan passed
- [ ] Deployed to staging 