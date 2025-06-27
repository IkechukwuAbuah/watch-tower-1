# Watch Tower Implementation Scratch Pad

## Background and Motivation

VPC operates 84 container trucks in Lagos, moving cargo between ports and client locations. The current workflow is inefficient:
- Trip creation takes 5-7 minutes per trip
- No real-time visibility into fleet status
- Manual reporting takes 2-3 hours daily
- Data scattered across LocoNav and Google Sheets

Watch Tower aims to solve these problems with:
- Natural language interface via Slack
- Real-time fleet tracking
- Automated reporting
- Unified data platform

The O3 implementation plan recommends significant architectural improvements including event sourcing, async-first design, PostGIS for geospatial queries, and the new OpenAI Responses API.

## Key Challenges and Analysis

### Technical Challenges
1. **PostGIS Integration**: Need to update models to use geography types for efficient geofence queries
2. **Async Everything**: Ensure all I/O operations are non-blocking
3. **Event Sourcing**: Implement Redis Streams for audit trail and real-time updates
4. **AI Integration**: Use OpenAI Responses API with function calling pattern

### Business Challenges
1. **User Adoption**: Operations team needs simple interface
2. **Data Quality**: Ensure sync between LocoNav and Sheets is reliable
3. **Performance**: <2 second response times for all queries
4. **Reliability**: 99.5% uptime requirement

### Integration Challenges
1. **LocoNav API**: Handle rate limits and potential downtime
2. **Google Sheets**: Respect 250 calls/minute quota
3. **Slack**: Use Socket Mode for reliability
4. **Supabase**: Configure real-time subscriptions

## High-level Task Breakdown

### Immediate Tasks (Week 1)
1. **Database Models** - Upgrade to PostGIS geography types
2. **Pydantic Schemas** - Create comprehensive validation
3. **Core Services** - LocoNav, Sheets, basic AI
4. **API Endpoints** - Replace placeholders with real logic

### Next Phase (Week 2)
1. **Event Sourcing** - Redis Streams setup
2. **Background Tasks** - Celery configuration
3. **Webhook Service** - Separate ingestion layer

### Future Phases
1. **Advanced AI** - Complex natural language queries
2. **Analytics** - Predictive insights
3. **Monitoring** - Full observability

## Project Status Board

### Current Sprint Tasks
- [ ] Update Truck model with geography(Point,4326)
- [ ] Update VehiclePosition with geography field
- [ ] Create missing models (Driver, Organization, Analytics)
- [ ] Setup Alembic for migrations
- [ ] Create TruckSchema with all variants
- [ ] Create TripSchema with validation
- [ ] Implement Google Sheets service
- [ ] Wire up truck API endpoints

### Completed Tasks
- ✅ Project planning and analysis
- ✅ Toy-box documentation created
- ✅ Identified all missing components
- ✅ Created workflow process documentation
- ✅ Established clear working methodology
- ✅ Created Cursor Rules for project navigation

### In Progress
- 🔄 Ready to start database model updates

## Executor's Feedback or Assistance Requests

### Current Status
**Mode**: Planner Mode (just created Cursor Rules)
**Next Action**: Ready to switch to Executor mode for database models implementation

### Planner Update - [Current Timestamp #2]
**Task**: Create Cursor Rules
**Status**: Completed
**Result**: Created comprehensive Cursor Rules for project navigation
**New Files**: 
- `.cursor/rules/watch-tower-workflow.mdc` - Toy-box workflow rules
- `.cursor/rules/watch-tower-o3-implementation.mdc` - O3 technical guidelines
- `.cursor/rules/watch-tower-project-structure.mdc` - Project structure guide
- Updated existing `.cursor/rules/watch-tower-1-workflow.mdc` with proper metadata
**Benefits**: Cursor will now understand our workflow and provide better assistance

### Planner Update - [Current Timestamp]
**Task**: Establish workflow process
**Status**: Completed
**Result**: Created comprehensive workflow documentation
**New Files**: 
- `workflow-process.md` - Complete workflow guide
- `errors-fixes.md` - Error tracking template
**Next Steps**: Switch to Executor mode to implement first task

### Questions for Human
1. **Approval to proceed?** The workflow and Cursor Rules are now documented. Should I switch to Executor mode and start implementing the database models?
2. **Google Sheets specifics**: Which sheets need syncing? (truck master, driver info, client locations?)
3. **Supabase setup**: Do you have a project created? Need URL and keys for `.env`

### Workflow Summary for Human
The toy-box now has a clear workflow:
1. **Planner** breaks down work into <2 hour tasks
2. **Executor** implements ONE task at a time
3. **Human** reviews and approves each task
4. **Documentation** happens continuously
5. **Communication** flows through scratch-pad.md

### Notes
- The existing models need significant updates to use PostGIS
- Database session is already configured for async which is great
- Need to be careful about backwards compatibility during migration
- geoalchemy2 package may need to be added to requirements.txt

## Technical Decisions Made

1. **Start Simple**: Implement core features first, add event sourcing later
2. **PostGIS First**: Update models to use geography types immediately
3. **Incremental Migration**: Use Alembic for safe schema changes
4. **API-First**: Get endpoints working before adding complex features
5. **Clear Workflow**: Established documented process for planning/execution

## Next Immediate Steps

Following the new workflow, the first Executor task will be:
1. Update backend/models/__init__.py to use PostGIS types
2. Add geoalchemy2 to requirements.txt if needed
3. Test the model changes locally
4. Create Alembic migration
5. Report completion for human review

---

**Current Mode**: Planner ✅
**Current Focus**: Workflow and Cursor Rules established, ready for execution
**Awaiting**: Human confirmation to proceed with database model implementation 