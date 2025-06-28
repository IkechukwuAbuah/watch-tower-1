"""
Event handlers for Watch Tower
"""

import logging
from typing import Dict, Any
from datetime import datetime
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .consumer import EventHandler
from .schemas import EventType
from models import VehiclePosition, Trip, Truck
from db.session import get_async_session
from core.config import settings
from services.slack_service import slack_service

logger = logging.getLogger(__name__)


class PositionUpdateHandler(EventHandler):
    """Handles position update events"""
    
    async def handle(self, event: Dict[str, Any]) -> None:
        """Store position update in database"""
        try:
            async with get_async_session() as session:
                # Create position record
                position = VehiclePosition(
                    truck_id=event["truck_id"],
                    timestamp=event.get("timestamp", datetime.utcnow()),
                    location=f"POINT({event['lng']} {event['lat']})",
                    speed=event.get("speed"),
                    heading=event.get("heading"),
                    ignition=event.get("ignition"),
                    altitude=event.get("altitude"),
                    accuracy=event.get("accuracy")
                )
                
                session.add(position)
                await session.commit()
                
                logger.info(
                    f"Stored position update for truck {event['truck_number']}",
                    extra={"truck_id": event["truck_id"]}
                )
                
        except Exception as e:
            logger.error(f"Failed to handle position update: {e}")
            raise


class TripStatusHandler(EventHandler):
    """Handles trip status change events"""
    
    async def handle(self, event: Dict[str, Any]) -> None:
        """Update trip status in database"""
        try:
            async with get_async_session() as session:
                # Get trip
                result = await session.execute(
                    select(Trip).where(Trip.id == event["trip_id"])
                )
                trip = result.scalar_one_or_none()
                
                if not trip:
                    logger.error(f"Trip {event['trip_id']} not found")
                    return
                
                # Update status
                trip.status = event["new_status"]
                
                # Update timestamps based on status
                if event["new_status"] == "in_progress" and not trip.started_at:
                    trip.started_at = event.get("timestamp", datetime.utcnow())
                elif event["new_status"] == "completed" and not trip.completed_at:
                    trip.completed_at = event.get("timestamp", datetime.utcnow())
                
                await session.commit()
                
                logger.info(
                    f"Updated trip {event['vpc_id']} status to {event['new_status']}",
                    extra={"trip_id": event["trip_id"]}
                )
                
        except Exception as e:
            logger.error(f"Failed to handle trip status change: {e}")
            raise


class AlertHandler(EventHandler):
    """Handles alert events"""
    
    async def handle(self, event: Dict[str, Any]) -> None:
        """Process alerts and send notifications"""
        try:
            logger.info(
                f"Processing {event['severity']} alert: {event['title']}",
                extra={
                    "alert_type": event["alert_type"],
                    "truck_id": event.get("truck_id"),
                    "trip_id": event.get("trip_id")
                }
            )
            
            # Send Slack notification
            if event.get("notify_slack", True) and settings.slack_bot_token:
                await slack_service.send_alert({
                    "severity": event["severity"],
                    "title": event["title"],
                    "alert_type": event["alert_type"],
                    "description": event.get("description", ""),
                    "truck_number": event.get("truck_number"),
                    "location": event.get("location")
                })
            
            # TODO: Implement email notification
            if event.get("notify_email", False):
                # Send email
                pass
                
        except Exception as e:
            logger.error(f"Failed to handle alert: {e}")
            raise


class WebhookReceivedHandler(EventHandler):
    """Handles webhook received events"""
    
    async def handle(self, event: Dict[str, Any]) -> None:
        """Process webhook data"""
        try:
            logger.info(
                f"Processing {event['webhook_type']} webhook",
                extra={
                    "source": event["source"],
                    "signature_valid": event["signature_valid"]
                }
            )
            
            # Webhook processing is handled by specific services
            # This handler is mainly for logging and metrics
            
        except Exception as e:
            logger.error(f"Failed to handle webhook: {e}")
            raise


class ErrorHandler(EventHandler):
    """Handles error events"""
    
    async def handle(self, event: Dict[str, Any]) -> None:
        """Process error events"""
        try:
            logger.error(
                f"System error in {event['service']}: {event['error_message']}",
                extra={
                    "error_type": event["error_type"],
                    "operation": event["operation"],
                    "recoverable": event.get("recoverable", True),
                    "retry_count": event.get("retry_count", 0)
                }
            )
            
            # Implement error recovery logic
            if event.get("recoverable", True) and event.get("retry_count", 0) < 3:
                # Send error alert to Slack for critical errors
                if event["error_type"] == "critical" and settings.slack_bot_token:
                    await slack_service.send_alert({
                        "severity": "critical",
                        "title": f"System Error in {event['service']}",
                        "alert_type": "system_error",
                        "description": f"Operation: {event['operation']}\nError: {event['error_message']}\nRetry: {event.get('retry_count', 0)}/3"
                    })
                
        except Exception as e:
            logger.error(f"Failed to handle error event: {e}")
            raise