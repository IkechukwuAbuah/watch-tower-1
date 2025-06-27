"""
LocoNav GPS tracking service integration
"""

import os
import hmac
import hashlib
from typing import Optional, Dict, Any
from datetime import datetime
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from geoalchemy2 import WKTElement

from models import Truck, VehiclePosition
from schemas import LocoNavWebhookPayload, VehiclePositionCreate


class LocoNavService:
    """Handle LocoNav GPS tracking webhooks and data processing"""
    
    def __init__(self):
        self.webhook_secret = os.getenv("LOCONAV_WEBHOOK_SECRET", "")
        self.api_key = os.getenv("LOCONAV_API_KEY", "")
    
    def verify_webhook_signature(self, payload: str, signature: str) -> bool:
        """
        Verify webhook signature using HMAC
        
        Args:
            payload: Raw webhook payload
            signature: HMAC signature from webhook header
            
        Returns:
            bool: True if signature is valid
        """
        if not self.webhook_secret:
            # If no secret configured, skip verification (dev mode)
            return True
            
        expected_signature = hmac.new(
            self.webhook_secret.encode(),
            payload.encode(),
            hashlib.sha256
        ).hexdigest()
        
        return hmac.compare_digest(expected_signature, signature)
    
    async def process_position_update(
        self,
        db: AsyncSession,
        payload: LocoNavWebhookPayload
    ) -> Optional[VehiclePosition]:
        """
        Process GPS position update from LocoNav
        
        Args:
            db: Database session
            payload: Validated webhook payload
            
        Returns:
            VehiclePosition if created successfully
        """
        # Find truck by LocoNav vehicle ID
        result = await db.execute(
            select(Truck).where(Truck.loconav_vehicle_id == payload.vehicle_id)
        )
        truck = result.scalar_one_or_none()
        
        if not truck:
            # Log unknown vehicle ID but don't fail
            print(f"Warning: Unknown LocoNav vehicle ID: {payload.vehicle_id}")
            return None
        
        # Create position record
        position = VehiclePosition(
            truck_id=truck.id,
            timestamp=payload.timestamp,
            location=WKTElement(f"POINT({payload.longitude} {payload.latitude})", srid=4326),
            speed=payload.speed,
            heading=payload.heading,
            ignition=payload.ignition,
            altitude=payload.altitude,
            accuracy=payload.accuracy
        )
        
        db.add(position)
        await db.commit()
        await db.refresh(position)
        
        # Handle special events
        if payload.event_type:
            await self._handle_event(db, truck.id, payload.event_type, payload)
        
        return position
    
    async def _handle_event(
        self,
        db: AsyncSession,
        truck_id: UUID,
        event_type: str,
        payload: LocoNavWebhookPayload
    ) -> None:
        """
        Handle special events from LocoNav
        
        Args:
            db: Database session
            truck_id: ID of the truck
            event_type: Type of event (trip_start, trip_end, etc.)
            payload: Full webhook payload
        """
        if event_type == "trip_start" and payload.trip_id:
            # Update trip status if we have the LocoNav trip ID
            from models import Trip
            result = await db.execute(
                select(Trip).where(
                    Trip.loconav_trip_id == payload.trip_id,
                    Trip.truck_id == truck_id
                )
            )
            trip = result.scalar_one_or_none()
            
            if trip and trip.status == "scheduled":
                trip.status = "in_progress"
                trip.started_at = payload.timestamp
                await db.commit()
                
        elif event_type == "trip_end" and payload.trip_id:
            # Mark trip as completed
            from models import Trip
            result = await db.execute(
                select(Trip).where(
                    Trip.loconav_trip_id == payload.trip_id,
                    Trip.truck_id == truck_id
                )
            )
            trip = result.scalar_one_or_none()
            
            if trip and trip.status == "in_progress":
                trip.status = "completed"
                trip.completed_at = payload.timestamp
                await db.commit()
    
    async def get_latest_position(
        self,
        db: AsyncSession,
        truck_id: UUID
    ) -> Optional[VehiclePosition]:
        """
        Get the latest position for a truck
        
        Args:
            db: Database session
            truck_id: ID of the truck
            
        Returns:
            Latest VehiclePosition or None
        """
        result = await db.execute(
            select(VehiclePosition)
            .where(VehiclePosition.truck_id == truck_id)
            .order_by(VehiclePosition.timestamp.desc())
            .limit(1)
        )
        return result.scalar_one_or_none()
    
    async def calculate_distance_traveled(
        self,
        db: AsyncSession,
        truck_id: UUID,
        start_time: datetime,
        end_time: datetime
    ) -> float:
        """
        Calculate total distance traveled by a truck in a time period
        
        Uses PostGIS ST_Distance to calculate distances between consecutive points
        
        Args:
            db: Database session
            truck_id: ID of the truck
            start_time: Start of period
            end_time: End of period
            
        Returns:
            Total distance in kilometers
        """
        # This query uses PostGIS window functions to calculate distance
        query = """
        WITH ordered_positions AS (
            SELECT 
                location,
                timestamp,
                LAG(location) OVER (ORDER BY timestamp) as prev_location
            FROM vehicle_positions
            WHERE truck_id = :truck_id
                AND timestamp >= :start_time
                AND timestamp <= :end_time
                AND location IS NOT NULL
            ORDER BY timestamp
        )
        SELECT 
            COALESCE(SUM(
                ST_Distance(location::geography, prev_location::geography) / 1000
            ), 0) as total_distance_km
        FROM ordered_positions
        WHERE prev_location IS NOT NULL;
        """
        
        result = await db.execute(
            query,
            {
                "truck_id": truck_id,
                "start_time": start_time,
                "end_time": end_time
            }
        )
        
        return result.scalar() or 0.0