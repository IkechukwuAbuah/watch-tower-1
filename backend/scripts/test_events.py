"""
Test script for Redis Streams event sourcing
"""

import asyncio
import sys
from datetime import datetime
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from events import (
    EventPublisher,
    EventConsumer,
    EventType,
    PositionUpdatedEvent,
    TripCreatedEvent,
    AlertTriggeredEvent,
)
from events.handlers import PositionUpdateHandler, AlertHandler
from db.redis import health_check as redis_health_check, close_redis_pool


async def test_publish_events():
    """Test publishing various events"""
    publisher = EventPublisher()
    
    print("Testing event publishing...")
    
    # Test position update event
    position_event = PositionUpdatedEvent(
        truck_id="123e4567-e89b-12d3-a456-426614174000",
        truck_number="TRUCK-001",
        lat=6.5244,
        lng=3.3792,
        speed=45.5,
        heading=180,
        ignition=True,
        distance_from_last=1250.5,
        time_since_last=300
    )
    
    entry_id = await publisher.publish(position_event)
    print(f"✅ Published position event: {entry_id}")
    
    # Test trip created event
    trip_event = TripCreatedEvent(
        trip_id="456e7890-e89b-12d3-a456-426614174000",
        vpc_id="VPC-2024-001",
        truck_id="123e4567-e89b-12d3-a456-426614174000",
        truck_number="TRUCK-001",
        origin_lat=6.5244,
        origin_lng=3.3792,
        destination_lat=6.6052,
        destination_lng=3.3490,
        created_by="api"
    )
    
    entry_id = await publisher.publish(trip_event)
    print(f"✅ Published trip event: {entry_id}")
    
    # Test alert event
    alert_event = AlertTriggeredEvent(
        alert_type="speed_violation",
        severity="high",
        truck_id="123e4567-e89b-12d3-a456-426614174000",
        title="Speed Violation Alert",
        description="Truck TRUCK-001 exceeded speed limit (75 km/h in 60 km/h zone)",
        location_lat=6.5244,
        location_lng=3.3792,
        data={
            "actual_speed": 75,
            "speed_limit": 60,
            "duration_seconds": 45
        }
    )
    
    entry_id = await publisher.publish(alert_event)
    print(f"✅ Published alert event: {entry_id}")
    
    # Get stream info
    for event_type in [EventType.POSITION_UPDATED, EventType.TRIP_CREATED, EventType.ALERT_TRIGGERED]:
        info = await publisher.get_stream_info(event_type.value)
        print(f"\n📊 Stream info for {event_type.value}:")
        print(f"   Length: {info.get('length', 0)}")
        print(f"   Groups: {info.get('groups', 0)}")


async def test_consume_events():
    """Test consuming events"""
    consumer = EventConsumer("test_consumer")
    group = consumer.create_group("test_consumers")
    
    # Register simple handlers that just print
    class PrintHandler:
        def __init__(self, event_type):
            self.event_type = event_type
            
        async def handle(self, event):
            print(f"\n🎯 Received {self.event_type} event:")
            print(f"   Event ID: {event.get('event_id')}")
            print(f"   Timestamp: {event.get('timestamp')}")
            if self.event_type == EventType.POSITION_UPDATED:
                print(f"   Truck: {event.get('truck_number')}")
                print(f"   Location: ({event.get('lat')}, {event.get('lng')})")
                print(f"   Speed: {event.get('speed')} km/h")
            elif self.event_type == EventType.ALERT_TRIGGERED:
                print(f"   Alert: {event.get('title')}")
                print(f"   Severity: {event.get('severity')}")
    
    # Register handlers
    group.register_handler(EventType.POSITION_UPDATED, PrintHandler(EventType.POSITION_UPDATED))
    group.register_handler(EventType.TRIP_CREATED, PrintHandler(EventType.TRIP_CREATED))
    group.register_handler(EventType.ALERT_TRIGGERED, PrintHandler(EventType.ALERT_TRIGGERED))
    
    print("\n🔊 Starting consumer (press Ctrl+C to stop)...")
    
    try:
        # Start consuming
        await consumer.start_all()
    except KeyboardInterrupt:
        print("\n⏹️  Stopping consumer...")
        consumer.stop_all()


async def main():
    """Main test function"""
    print("🚀 Watch Tower Event System Test\n")
    
    # Check Redis connection
    if not await redis_health_check():
        print("❌ Redis is not available. Please start Redis first.")
        return
    
    print("✅ Redis connection successful\n")
    
    # Ask user what to test
    print("What would you like to test?")
    print("1. Publish events")
    print("2. Consume events")
    print("3. Both (publish then consume)")
    
    choice = input("\nEnter choice (1-3): ").strip()
    
    if choice == "1":
        await test_publish_events()
    elif choice == "2":
        await test_consume_events()
    elif choice == "3":
        await test_publish_events()
        print("\n" + "="*50 + "\n")
        await test_consume_events()
    else:
        print("Invalid choice")
    
    # Cleanup
    await close_redis_pool()
    print("\n✅ Test complete!")


if __name__ == "__main__":
    asyncio.run(main())