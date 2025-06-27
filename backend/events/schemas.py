"""
Event schemas for Watch Tower event sourcing
"""

from enum import Enum
from datetime import datetime
from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field, ConfigDict
import uuid


class EventType(str, Enum):
    """Event types in the system"""
    WEBHOOK_RECEIVED = "webhook.received"
    TRIP_CREATED = "trip.created"
    TRIP_STATUS_CHANGED = "trip.status_changed"
    POSITION_UPDATED = "position.updated"
    TRUCK_STATUS_CHANGED = "truck.status_changed"
    ALERT_TRIGGERED = "alert.triggered"
    SYNC_COMPLETED = "sync.completed"
    ERROR_OCCURRED = "error.occurred"


class BaseEvent(BaseModel):
    """Base event schema"""
    model_config = ConfigDict(use_enum_values=True)
    
    event_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    event_type: EventType
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    version: str = "1.0"
    correlation_id: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)


class WebhookReceivedEvent(BaseEvent):
    """Event when webhook is received from LocoNav"""
    event_type: EventType = EventType.WEBHOOK_RECEIVED
    
    webhook_type: str  # e.g., "position_update", "trip_update"
    source: str = "loconav"
    payload: Dict[str, Any]
    headers: Dict[str, str]
    signature_valid: bool


class TripCreatedEvent(BaseEvent):
    """Event when a new trip is created"""
    event_type: EventType = EventType.TRIP_CREATED
    
    trip_id: str
    vpc_id: str
    truck_id: str
    truck_number: str
    origin_lat: float
    origin_lng: float
    destination_lat: float
    destination_lng: float
    created_by: str  # "system", "api", "webhook"


class TripStatusChangedEvent(BaseEvent):
    """Event when trip status changes"""
    event_type: EventType = EventType.TRIP_STATUS_CHANGED
    
    trip_id: str
    vpc_id: str
    truck_id: str
    old_status: str
    new_status: str
    reason: Optional[str] = None
    location_lat: Optional[float] = None
    location_lng: Optional[float] = None


class PositionUpdatedEvent(BaseEvent):
    """Event when vehicle position is updated"""
    event_type: EventType = EventType.POSITION_UPDATED
    
    truck_id: str
    truck_number: str
    lat: float
    lng: float
    speed: Optional[float] = None
    heading: Optional[int] = None
    ignition: Optional[bool] = None
    altitude: Optional[float] = None
    accuracy: Optional[float] = None
    trip_id: Optional[str] = None  # If currently on a trip
    
    # Calculated fields
    distance_from_last: Optional[float] = None  # meters
    time_since_last: Optional[int] = None  # seconds


class TruckStatusChangedEvent(BaseEvent):
    """Event when truck status changes"""
    event_type: EventType = EventType.TRUCK_STATUS_CHANGED
    
    truck_id: str
    truck_number: str
    old_status: str
    new_status: str
    reason: Optional[str] = None


class AlertTriggeredEvent(BaseEvent):
    """Event when an alert is triggered"""
    event_type: EventType = EventType.ALERT_TRIGGERED
    
    alert_type: str  # "geofence_exit", "speed_violation", "long_stop", etc.
    severity: str  # "low", "medium", "high", "critical"
    truck_id: Optional[str] = None
    trip_id: Optional[str] = None
    
    title: str
    description: str
    location_lat: Optional[float] = None
    location_lng: Optional[float] = None
    
    # Alert specific data
    data: Dict[str, Any] = Field(default_factory=dict)
    
    # Notification settings
    notify_slack: bool = True
    notify_email: bool = False
    recipients: List[str] = Field(default_factory=list)


class SyncCompletedEvent(BaseEvent):
    """Event when a sync operation completes"""
    event_type: EventType = EventType.SYNC_COMPLETED
    
    sync_type: str  # "google_sheets", "loconav_trips", etc.
    records_processed: int
    records_created: int
    records_updated: int
    records_failed: int
    duration_seconds: float
    errors: List[str] = Field(default_factory=list)


class ErrorOccurredEvent(BaseEvent):
    """Event when an error occurs in the system"""
    event_type: EventType = EventType.ERROR_OCCURRED
    
    error_type: str
    error_message: str
    error_code: Optional[str] = None
    service: str  # Which service had the error
    operation: str  # What operation was being performed
    
    # Context about the error
    context: Dict[str, Any] = Field(default_factory=dict)
    stack_trace: Optional[str] = None
    
    # Recovery information
    retry_count: int = 0
    recoverable: bool = True