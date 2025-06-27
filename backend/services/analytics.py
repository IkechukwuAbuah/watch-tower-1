"""
Analytics service for fleet metrics and insights
"""

from typing import Dict, List, Any, Optional
from datetime import datetime, date, timedelta
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_, case, text


class AnalyticsService:
    """Calculate advanced analytics and metrics for fleet operations"""
    
    async def calculate_geofence_violations(
        self,
        db: AsyncSession,
        truck_id: UUID,
        start_time: datetime,
        end_time: datetime,
        geofence_wkt: str
    ) -> int:
        """
        Count geofence violations using PostGIS
        
        Args:
            db: Database session
            truck_id: ID of the truck
            start_time: Start of period
            end_time: End of period
            geofence_wkt: WKT representation of geofence polygon
            
        Returns:
            Number of position records outside geofence
        """
        query = """
        SELECT COUNT(*) as violations
        FROM vehicle_positions
        WHERE truck_id = :truck_id
            AND timestamp >= :start_time
            AND timestamp <= :end_time
            AND NOT ST_Within(
                location::geometry,
                ST_GeomFromText(:geofence_wkt, 4326)
            )
        """
        
        result = await db.execute(
            text(query),
            {
                "truck_id": truck_id,
                "start_time": start_time,
                "end_time": end_time,
                "geofence_wkt": geofence_wkt
            }
        )
        
        return result.scalar() or 0
    
    async def find_trucks_near_location(
        self,
        db: AsyncSession,
        latitude: float,
        longitude: float,
        radius_km: float,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Find trucks near a specific location using PostGIS
        
        Args:
            db: Database session
            latitude: Target latitude
            longitude: Target longitude
            radius_km: Search radius in kilometers
            limit: Maximum number of results
            
        Returns:
            List of trucks with distance information
        """
        # Convert radius to meters for PostGIS
        radius_m = radius_km * 1000
        
        query = """
        WITH latest_positions AS (
            SELECT DISTINCT ON (truck_id)
                truck_id,
                location,
                timestamp,
                speed,
                heading
            FROM vehicle_positions
            ORDER BY truck_id, timestamp DESC
        )
        SELECT 
            t.id,
            t.truck_number,
            t.status,
            ST_Distance(
                lp.location::geography,
                ST_SetSRID(ST_MakePoint(:longitude, :latitude), 4326)::geography
            ) / 1000 as distance_km,
            ST_X(lp.location::geometry) as longitude,
            ST_Y(lp.location::geometry) as latitude,
            lp.timestamp as last_seen,
            lp.speed,
            lp.heading
        FROM trucks t
        JOIN latest_positions lp ON t.id = lp.truck_id
        WHERE ST_DWithin(
            lp.location::geography,
            ST_SetSRID(ST_MakePoint(:longitude, :latitude), 4326)::geography,
            :radius_m
        )
        ORDER BY distance_km
        LIMIT :limit
        """
        
        result = await db.execute(
            text(query),
            {
                "latitude": latitude,
                "longitude": longitude,
                "radius_m": radius_m,
                "limit": limit
            }
        )
        
        trucks = []
        for row in result:
            trucks.append({
                "truck_id": str(row.id),
                "truck_number": row.truck_number,
                "status": row.status,
                "distance_km": round(row.distance_km, 2),
                "location": {
                    "latitude": row.latitude,
                    "longitude": row.longitude
                },
                "last_seen": row.last_seen.isoformat(),
                "speed": float(row.speed) if row.speed else None,
                "heading": row.heading
            })
        
        return trucks
    
    async def calculate_idle_time(
        self,
        db: AsyncSession,
        truck_id: UUID,
        start_time: datetime,
        end_time: datetime,
        idle_speed_threshold: float = 5.0
    ) -> Dict[str, Any]:
        """
        Calculate idle time statistics
        
        Args:
            db: Database session
            truck_id: ID of the truck
            start_time: Start of period
            end_time: End of period
            idle_speed_threshold: Speed below which truck is considered idle (km/h)
            
        Returns:
            Dict with idle time statistics
        """
        query = """
        WITH position_intervals AS (
            SELECT 
                timestamp,
                speed,
                ignition,
                LEAD(timestamp) OVER (ORDER BY timestamp) as next_timestamp
            FROM vehicle_positions
            WHERE truck_id = :truck_id
                AND timestamp >= :start_time
                AND timestamp <= :end_time
            ORDER BY timestamp
        )
        SELECT 
            COUNT(*) as total_positions,
            COUNT(CASE WHEN speed < :idle_threshold AND ignition = true THEN 1 END) as idle_positions,
            SUM(
                CASE 
                    WHEN speed < :idle_threshold AND ignition = true AND next_timestamp IS NOT NULL
                    THEN EXTRACT(EPOCH FROM (next_timestamp - timestamp))
                    ELSE 0
                END
            ) / 3600 as idle_hours,
            SUM(
                CASE 
                    WHEN ignition = true AND next_timestamp IS NOT NULL
                    THEN EXTRACT(EPOCH FROM (next_timestamp - timestamp))
                    ELSE 0
                END
            ) / 3600 as total_engine_hours
        FROM position_intervals
        """
        
        result = await db.execute(
            text(query),
            {
                "truck_id": truck_id,
                "start_time": start_time,
                "end_time": end_time,
                "idle_threshold": idle_speed_threshold
            }
        )
        
        row = result.one()
        
        idle_percentage = 0
        if row.total_engine_hours and row.total_engine_hours > 0:
            idle_percentage = (row.idle_hours / row.total_engine_hours) * 100
        
        return {
            "truck_id": str(truck_id),
            "period": {
                "start": start_time.isoformat(),
                "end": end_time.isoformat()
            },
            "idle_hours": round(row.idle_hours or 0, 2),
            "total_engine_hours": round(row.total_engine_hours or 0, 2),
            "idle_percentage": round(idle_percentage, 1),
            "total_positions": row.total_positions,
            "idle_positions": row.idle_positions
        }
    
    async def generate_trip_efficiency_report(
        self,
        db: AsyncSession,
        trip_id: UUID
    ) -> Dict[str, Any]:
        """
        Generate comprehensive trip efficiency report
        
        Args:
            db: Database session
            trip_id: ID of the trip
            
        Returns:
            Dict with trip efficiency metrics
        """
        # Get trip details
        from models import Trip
        trip_result = await db.execute(
            select(Trip).where(Trip.id == trip_id)
        )
        trip = trip_result.scalar_one_or_none()
        
        if not trip:
            return {"error": "Trip not found"}
        
        # Calculate actual vs planned metrics
        metrics = {
            "trip_id": str(trip_id),
            "vpc_id": trip.vpc_id,
            "status": trip.status,
            "planned": {
                "distance_km": float(trip.distance_km) if trip.distance_km else None,
                "duration_minutes": trip.estimated_duration_minutes
            },
            "actual": {}
        }
        
        # If trip is completed, calculate actual metrics
        if trip.completed_at and trip.started_at:
            # Actual duration
            actual_duration = (trip.completed_at - trip.started_at).total_seconds() / 60
            metrics["actual"]["duration_minutes"] = round(actual_duration, 1)
            
            # Calculate actual distance if we have position data
            if trip.started_at:
                from services.loconav import LocoNavService
                service = LocoNavService()
                
                actual_distance = await service.calculate_distance_traveled(
                    db,
                    trip.truck_id,
                    trip.started_at,
                    trip.completed_at
                )
                metrics["actual"]["distance_km"] = round(actual_distance, 2)
                
                # Calculate efficiency scores
                if trip.distance_km and actual_distance > 0:
                    distance_efficiency = (float(trip.distance_km) / actual_distance) * 100
                    metrics["efficiency"] = {
                        "distance_efficiency": round(min(distance_efficiency, 100), 1),
                        "extra_distance_km": round(max(actual_distance - float(trip.distance_km), 0), 2)
                    }
                
                if trip.estimated_duration_minutes and actual_duration > 0:
                    time_efficiency = (trip.estimated_duration_minutes / actual_duration) * 100
                    metrics["efficiency"]["time_efficiency"] = round(min(time_efficiency, 100), 1)
                    metrics["efficiency"]["extra_time_minutes"] = round(
                        max(actual_duration - trip.estimated_duration_minutes, 0), 1
                    )
        
        return metrics