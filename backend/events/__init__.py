"""
Event sourcing infrastructure for Watch Tower
"""

from .schemas import (
    EventType,
    BaseEvent,
    WebhookReceivedEvent,
    TripCreatedEvent,
    TripStatusChangedEvent,
    PositionUpdatedEvent,
    TruckStatusChangedEvent,
    AlertTriggeredEvent,
)
from .publisher import EventPublisher
from .consumer import EventConsumer, ConsumerGroup

__all__ = [
    "EventType",
    "BaseEvent",
    "WebhookReceivedEvent",
    "TripCreatedEvent",
    "TripStatusChangedEvent",
    "PositionUpdatedEvent",
    "TruckStatusChangedEvent",
    "AlertTriggeredEvent",
    "EventPublisher",
    "EventConsumer",
    "ConsumerGroup",
]