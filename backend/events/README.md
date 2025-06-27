# Watch Tower Event Sourcing System

## Overview

The Watch Tower event sourcing system uses Redis Streams to capture and process all system events in real-time. This provides:

- **Audit Trail**: Complete history of all system changes
- **Event Replay**: Ability to replay events for debugging or recovery
- **Decoupling**: Services communicate through events, not direct calls
- **Scalability**: Multiple consumers can process events in parallel

## Architecture

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   API/Webhook   │────▶│  Redis Streams  │────▶│    Consumers    │
└─────────────────┘     └─────────────────┘     └─────────────────┘
        │                        │                        │
        ▼                        ▼                        ▼
   Publish Event          Store in Stream          Process Event
```

## Event Types

- **WEBHOOK_RECEIVED**: External webhook received
- **TRIP_CREATED**: New trip created
- **TRIP_STATUS_CHANGED**: Trip status updated
- **POSITION_UPDATED**: Vehicle GPS position updated
- **TRUCK_STATUS_CHANGED**: Truck operational status changed
- **ALERT_TRIGGERED**: System alert generated
- **SYNC_COMPLETED**: Data sync operation completed
- **ERROR_OCCURRED**: System error occurred

## Usage

### Publishing Events

```python
from events import PositionUpdatedEvent
from events.publisher import event_publisher

# Create event
event = PositionUpdatedEvent(
    truck_id="123",
    truck_number="TRUCK-001",
    lat=6.5244,
    lng=3.3792,
    speed=45.5
)

# Publish
entry_id = await event_publisher.publish(event)
```

### Consuming Events

```python
from events import EventConsumer, EventType
from events.consumer import EventHandler

# Create handler
class MyHandler(EventHandler):
    async def handle(self, event: Dict[str, Any]) -> None:
        print(f"Processing event: {event}")

# Setup consumer
consumer = EventConsumer("my_consumer")
group = consumer.create_group("my_group")
group.register_handler(EventType.POSITION_UPDATED, MyHandler())

# Start consuming
await consumer.start_all()
```

## Redis Streams Structure

Each event type has its own stream:
- `watch_tower:events:webhook.received`
- `watch_tower:events:trip.created`
- `watch_tower:events:position.updated`
- etc.

## Consumer Groups

Default consumer group: `watch_tower_consumers`

Multiple consumers in a group share the workload, ensuring each event is processed exactly once.

## Event Schema

All events include:
- `event_id`: Unique identifier
- `event_type`: Type of event
- `timestamp`: When event occurred
- `version`: Schema version
- `correlation_id`: For tracing related events
- `metadata`: Additional context

## Testing

Run the test script to verify the event system:

```bash
python scripts/test_events.py
```

## Monitoring

Check stream status:
```python
info = await event_publisher.get_stream_info(EventType.POSITION_UPDATED)
print(f"Events in stream: {info['length']}")
```

Check pending messages:
```python
pending = await group.get_pending_messages(EventType.POSITION_UPDATED)
print(f"Pending messages: {len(pending)}")
```

## Best Practices

1. **Always publish events** for state changes
2. **Make events immutable** - never modify after publishing
3. **Include sufficient context** in events
4. **Handle failures gracefully** in consumers
5. **Monitor consumer lag** to ensure timely processing