"""
Event consumer for Redis Streams
"""

import json
import logging
import asyncio
from typing import Dict, Any, Optional, Callable, List
from datetime import datetime
from abc import ABC, abstractmethod

from db.redis import get_redis_client
from core.config import settings
from .schemas import BaseEvent, EventType

logger = logging.getLogger(__name__)


class EventHandler(ABC):
    """Base class for event handlers"""
    
    @abstractmethod
    async def handle(self, event: Dict[str, Any]) -> None:
        """Handle an event"""
        pass


class ConsumerGroup:
    """Manages a consumer group for Redis Streams"""
    
    def __init__(
        self,
        group_name: str,
        consumer_name: str,
        stream_prefix: Optional[str] = None
    ):
        self.group_name = group_name
        self.consumer_name = consumer_name
        self.stream_prefix = stream_prefix or settings.event_stream_prefix
        self.handlers: Dict[EventType, List[EventHandler]] = {}
        self.running = False
        
    def _get_stream_name(self, event_type: str) -> str:
        """Get stream name for event type"""
        return f"{self.stream_prefix}:{event_type}"
    
    def register_handler(self, event_type: EventType, handler: EventHandler) -> None:
        """Register handler for event type"""
        if event_type not in self.handlers:
            self.handlers[event_type] = []
        self.handlers[event_type].append(handler)
        logger.info(f"Registered handler for {event_type}")
    
    def _deserialize_event(self, data: Dict[str, bytes]) -> Dict[str, Any]:
        """Deserialize event from Redis"""
        result = {}
        
        for key, value in data.items():
            # Decode bytes to string
            if isinstance(value, bytes):
                value = value.decode('utf-8')
            
            # Try to parse JSON fields
            if key in ['metadata', 'payload', 'headers', 'data', 'context', 'errors']:
                try:
                    result[key] = json.loads(value)
                except json.JSONDecodeError:
                    result[key] = value
            # Parse datetime fields
            elif key in ['timestamp'] and isinstance(value, str):
                try:
                    result[key] = datetime.fromisoformat(value)
                except ValueError:
                    result[key] = value
            # Parse numeric fields
            elif key in ['lat', 'lng', 'speed', 'altitude', 'accuracy', 'distance_from_last',
                        'records_processed', 'records_created', 'records_updated', 
                        'records_failed', 'duration_seconds', 'retry_count']:
                try:
                    result[key] = float(value)
                except ValueError:
                    result[key] = value
            elif key in ['heading', 'time_since_last']:
                try:
                    result[key] = int(value)
                except ValueError:
                    result[key] = value
            # Parse boolean fields
            elif key in ['ignition', 'signature_valid', 'notify_slack', 'notify_email', 'recoverable']:
                result[key] = value.lower() == 'true' if isinstance(value, str) else value
            else:
                result[key] = value
        
        return result
    
    async def _process_message(
        self,
        stream_name: str,
        message_id: str,
        data: Dict[str, bytes]
    ) -> bool:
        """
        Process a single message
        
        Returns:
            True if processed successfully
        """
        try:
            # Deserialize event
            event_data = self._deserialize_event(data)
            event_type = EventType(event_data.get('event_type'))
            
            # Get handlers for this event type
            handlers = self.handlers.get(event_type, [])
            
            if not handlers:
                logger.warning(f"No handlers registered for {event_type}")
                return True  # Still acknowledge as processed
            
            # Execute all handlers
            for handler in handlers:
                try:
                    await handler.handle(event_data)
                except Exception as e:
                    logger.error(
                        f"Handler failed for {event_type}: {e}",
                        extra={"event_id": event_data.get('event_id')}
                    )
                    # Continue with other handlers
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to process message: {e}", extra={"message_id": message_id})
            return False
    
    async def consume(
        self,
        event_types: List[EventType],
        batch_size: Optional[int] = None,
        block_ms: Optional[int] = None
    ) -> None:
        """
        Start consuming events from streams
        
        Args:
            event_types: List of event types to consume
            batch_size: Number of messages to read in each batch
            block_ms: Milliseconds to block waiting for messages
        """
        batch_size = batch_size or settings.event_batch_size
        block_ms = block_ms or settings.event_block_ms
        
        # Build stream dict for XREADGROUP
        streams = {
            self._get_stream_name(event_type): ">"
            for event_type in event_types
        }
        
        self.running = True
        logger.info(
            f"Starting consumer '{self.consumer_name}' in group '{self.group_name}'",
            extra={"streams": list(streams.keys())}
        )
        
        while self.running:
            try:
                client = await get_redis_client()
                
                # Read from streams
                messages = await client.xreadgroup(
                    self.group_name,
                    self.consumer_name,
                    streams,
                    count=batch_size,
                    block=block_ms
                )
                
                if not messages:
                    continue
                
                # Process messages
                for stream_name, stream_messages in messages:
                    for message_id, data in stream_messages:
                        success = await self._process_message(
                            stream_name,
                            message_id,
                            data
                        )
                        
                        if success:
                            # Acknowledge message
                            await client.xack(
                                stream_name,
                                self.group_name,
                                message_id
                            )
                
            except asyncio.CancelledError:
                logger.info("Consumer cancelled")
                break
            except Exception as e:
                logger.error(f"Consumer error: {e}")
                await asyncio.sleep(5)  # Wait before retrying
        
        logger.info(f"Consumer '{self.consumer_name}' stopped")
    
    async def get_pending_messages(self, event_type: EventType) -> List[Dict[str, Any]]:
        """Get pending messages for this consumer"""
        try:
            client = await get_redis_client()
            stream_name = self._get_stream_name(event_type)
            
            # Get pending messages
            pending = await client.xpending(
                stream_name,
                self.group_name,
                count=100
            )
            
            return [
                {
                    "message_id": msg[0],
                    "consumer": msg[1],
                    "idle_time_ms": msg[2],
                    "delivery_count": msg[3]
                }
                for msg in pending
            ]
            
        except Exception as e:
            logger.error(f"Failed to get pending messages: {e}")
            return []
    
    async def claim_pending_messages(
        self,
        event_type: EventType,
        min_idle_ms: int = 60000  # 1 minute
    ) -> int:
        """
        Claim pending messages from other consumers
        
        Returns:
            Number of messages claimed
        """
        try:
            client = await get_redis_client()
            stream_name = self._get_stream_name(event_type)
            
            # Get pending messages older than min_idle_ms
            pending = await self.get_pending_messages(event_type)
            old_messages = [
                msg["message_id"]
                for msg in pending
                if msg["idle_time_ms"] > min_idle_ms
            ]
            
            if not old_messages:
                return 0
            
            # Claim messages
            claimed = await client.xclaim(
                stream_name,
                self.group_name,
                self.consumer_name,
                min_idle_ms,
                old_messages
            )
            
            logger.info(f"Claimed {len(claimed)} pending messages")
            return len(claimed)
            
        except Exception as e:
            logger.error(f"Failed to claim messages: {e}")
            return 0
    
    def stop(self) -> None:
        """Stop consuming"""
        self.running = False


class EventConsumer:
    """High-level event consumer with automatic setup"""
    
    def __init__(self, consumer_name: str):
        self.consumer_name = consumer_name
        self.groups: Dict[str, ConsumerGroup] = {}
        
    def create_group(self, group_name: str) -> ConsumerGroup:
        """Create or get consumer group"""
        if group_name not in self.groups:
            self.groups[group_name] = ConsumerGroup(
                group_name,
                self.consumer_name
            )
        return self.groups[group_name]
    
    async def start_all(self) -> None:
        """Start all consumer groups"""
        tasks = []
        
        for group_name, group in self.groups.items():
            # Get all event types this group handles
            event_types = list(group.handlers.keys())
            
            if event_types:
                task = asyncio.create_task(
                    group.consume(event_types),
                    name=f"consumer_{group_name}"
                )
                tasks.append(task)
        
        if tasks:
            await asyncio.gather(*tasks)
    
    def stop_all(self) -> None:
        """Stop all consumer groups"""
        for group in self.groups.values():
            group.stop()