# O3 Technical Implementation Plan - Watch Tower

## Overview
This document tracks the implementation of O3's recommended improvements to modernize the Watch Tower stack with async-first architecture, event sourcing, and the new OpenAI Responses API.

## Key Improvements

### 1. Modern Dependencies
- OpenAI Responses API (>=1.30.0) replacing Assistants API
- Async SQLAlchemy 2 for non-blocking DB I/O
- Supabase async client (acreate_client)
- Redis Streams for event sourcing
- PostGIS for geospatial queries
- Structlog for structured logging

### 2. Architecture Changes
- Event-sourced ingestion layer with Redis Streams
- Separate webhook ingestion microservice
- Async-first data access patterns
- Function-calling pattern with Pydantic validation
- Stateless, horizontally scalable services

### 3. Data Layer Upgrades
- PostGIS with geography(Point,4326) for 50ms geofence lookups
- pgvector for future semantic search
- Materialized views for analytics
- Event sourcing for all inbound data

### 4. AI/LLM Improvements
- OpenAI Responses API with streaming
- Tool definitions with Pydantic schemas
- Context window optimization with embeddings
- Deterministic function-calling pattern

### 5. Integration Patterns
- Redis Streams consumer groups for different workloads
- Exponential backoff for Google Sheets API
- HMAC validation for webhooks
- Socket Mode isolation for Slack bot

## Implementation Status

- [x] Project structure created
- [ ] Dependencies updated for async-first
- [ ] Database models with async SQLAlchemy 2
- [ ] PostGIS extensions enabled
- [ ] Redis Streams setup
- [ ] Webhook ingestion service
- [ ] OpenAI Responses API integration
- [ ] Sheets sync with rate limiting
- [ ] Slack bot with Socket Mode
- [ ] Analytics engine with Celery beat

## References
- OpenAI Responses API: https://platform.openai.com/docs/guides/function-calling
- Redis Streams Architecture: https://www.harness.io/blog/event-driven-architecture-redis-streams
- PostGIS Performance: https://postgis.net/docs/ST_DWithin.html
- Async SQLAlchemy: https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html
