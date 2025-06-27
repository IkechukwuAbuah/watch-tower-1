"""
Event publisher for Redis Streams
"""

import json
import logging
from typing import Dict, Any, Optional
from datetime import datetime

from db.redis import get_redis_client
from core.config import settings
from .schemas import BaseEvent

logger = logging.getLogger(__name__)


class EventPublisher:
    """Publishes events to Redis Streams"""
    
    def __init__(self, stream_prefix: Optional[str] = None):
        self.stream_prefix = stream_prefix or settings.event_stream_prefix
        
    def _get_stream_name(self, event_type: str) -> str:
        """Get stream name for event type"""
        return f"{self.stream_prefix}:{event_type}"
    
    def _serialize_event(self, event: BaseEvent) -> Dict[str, Any]:
        """Serialize event for Redis"""
        # Convert to dict and handle datetime serialization
        event_dict = event.model_dump()
        
        # Convert datetime to ISO format
        for key, value in event_dict.items():
            if isinstance(value, datetime):
                event_dict[key] = value.isoformat()
        
        # Serialize nested objects to JSON strings
        return {
            k: json.dumps(v) if isinstance(v, (dict, list)) else str(v)
            for k, v in event_dict.items()
        }
    
    async def publish(self, event: BaseEvent) -> str:
        """
        Publish event to Redis Stream
        
        Returns:
            Stream entry ID
        """
        try:
            client = await get_redis_client()
            stream_name = self._get_stream_name(event.event_type)
            
            # Serialize event
            event_data = self._serialize_event(event)
            
            # Add to stream with automatic ID generation
            entry_id = await client.xadd(
                stream_name,
                event_data,
                maxlen=10000,  # Keep last 10k events per stream
                approximate=True  # Allow Redis to optimize trimming
            )
            
            logger.info(
                f"Published {event.event_type} event",
                extra={
                    "event_id": event.event_id,
                    "stream": stream_name,
                    "entry_id": entry_id
                }
            )
            
            return entry_id
            
        except Exception as e:
            logger.error(
                f"Failed to publish event: {e}",
                extra={
                    "event_type": event.event_type,
                    "event_id": event.event_id
                }
            )
            raise
    
    async def publish_batch(self, events: list[BaseEvent]) -> list[str]:
        """
        Publish multiple events in a batch
        
        Returns:
            List of stream entry IDs
        """
        entry_ids = []
        
        # Group events by type for efficient publishing
        events_by_type: Dict[str, list[BaseEvent]] = {}
        for event in events:
            if event.event_type not in events_by_type:
                events_by_type[event.event_type] = []
            events_by_type[event.event_type].append(event)
        
        # Publish each group
        for event_type, type_events in events_by_type.items():
            for event in type_events:
                entry_id = await self.publish(event)
                entry_ids.append(entry_id)
        
        return entry_ids
    
    async def get_stream_info(self, event_type: str) -> Dict[str, Any]:
        """Get information about a stream"""
        try:
            client = await get_redis_client()
            stream_name = self._get_stream_name(event_type)
            
            info = await client.xinfo_stream(stream_name)
            return {
                "length": info.get("length", 0),
                "first_entry": info.get("first-entry"),
                "last_entry": info.get("last-entry"),
                "groups": info.get("groups", 0)
            }
        except Exception as e:
            logger.error(f"Failed to get stream info: {e}")
            return {"error": str(e)}
    
    async def create_consumer_group(self, event_type: str, group_name: str, start_id: str = "$") -> bool:
        """
        Create consumer group for a stream
        
        Args:
            event_type: Type of event
            group_name: Name of consumer group
            start_id: Where to start reading ("0" for beginning, "$" for new messages only)
        """
        try:
            client = await get_redis_client()
            stream_name = self._get_stream_name(event_type)
            
            await client.xgroup_create(
                stream_name,
                group_name,
                id=start_id,
                mkstream=True  # Create stream if it doesn't exist
            )
            
            logger.info(f"Created consumer group '{group_name}' for stream '{stream_name}'")
            return True
            
        except Exception as e:
            if "BUSYGROUP" in str(e):
                logger.info(f"Consumer group '{group_name}' already exists")
                return True
            
            logger.error(f"Failed to create consumer group: {e}")
            raise


# Global publisher instance
event_publisher = EventPublisher()