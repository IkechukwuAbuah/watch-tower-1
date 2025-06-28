"""
AI function implementations for Watch Tower natural language interface
"""

import logging
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from geoalchemy2.functions import ST_AsText

from db.session import get_async_session
from models import Truck, Trip, VehiclePosition
from services.loconav_service import loconav_api_service
from core.config import settings

logger = logging.getLogger(__name__)


async def get_truck_location(truck_number: str) -> Dict[str, Any]:
    """Get current location and status of a specific truck"""
    try:
        async with get_async_session() as session:
            # Find truck by number
            result = await session.execute(
                select(Truck).where(Truck.truck_number == truck_number.upper())
            )
            truck = result.scalar_one_or_none()
            
            if not truck:
                return {
                    "error": f"Truck {truck_number} not found",
                    "available_trucks": "Check truck number and try again"
                }
            
            # Get latest position
            position_result = await session.execute(
                select(VehiclePosition, ST_AsText(VehiclePosition.location))
                .where(VehiclePosition.truck_id == truck.id)
                .order_by(VehiclePosition.timestamp.desc())
                .limit(1)
            )
            position_row = position_result.first()
            
            if not position_row:
                return {
                    "truck_number": truck_number,
                    "status": truck.status,
                    "company": truck.company,
                    "location": "No recent location data",
                    "last_update": "No data available"
                }
            
            position, location_wkt = position_row
            
            # Parse location coordinates
            coordinates = location_wkt.replace("POINT(", "").replace(")", "").split()
            longitude, latitude = float(coordinates[0]), float(coordinates[1])
            
            # Get current trip if any
            trip_result = await session.execute(
                select(Trip)
                .where(
                    Trip.truck_id == truck.id,
                    Trip.status.in_(["scheduled", "in_progress"])
                )
                .order_by(Trip.created_at.desc())
                .limit(1)
            )
            current_trip = trip_result.scalar_one_or_none()
            
            response = {
                "truck_number": truck_number,
                "status": truck.status,
                "company": truck.company,
                "fleet_manager": truck.fleet_manager,
                "location": {
                    "latitude": latitude,
                    "longitude": longitude,
                    "address": f"Lat: {latitude:.6f}, Lng: {longitude:.6f}"
                },
                "last_update": position.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                "speed": position.speed,
                "ignition": "On" if position.ignition else "Off"
            }
            
            if current_trip:
                response["current_trip"] = {
                    "vpc_id": current_trip.vpc_id,
                    "status": current_trip.status,
                    "origin": current_trip.origin_name,
                    "destination": current_trip.destination_name,
                    "scheduled_departure": current_trip.scheduled_departure_time.strftime("%Y-%m-%d %H:%M") if current_trip.scheduled_departure_time else None
                }
            
            logger.info(f"Retrieved location for truck {truck_number}")
            return response
            
    except Exception as e:
        logger.error(f"Error getting truck location {truck_number}: {e}")
        return {"error": f"Failed to get location for truck {truck_number}: {str(e)}"}


async def create_new_trip(
    truck_number: str, 
    origin: str, 
    destination: str, 
    scheduled_date: Optional[str] = None
) -> Dict[str, Any]:
    """Create a new trip for a truck"""
    try:
        async with get_async_session() as session:
            # Find truck
            result = await session.execute(
                select(Truck).where(Truck.truck_number == truck_number.upper())
            )
            truck = result.scalar_one_or_none()
            
            if not truck:
                return {"error": f"Truck {truck_number} not found"}
            
            # Parse scheduled time
            scheduled_time = None
            if scheduled_date:
                try:
                    if "tomorrow" in scheduled_date.lower():
                        scheduled_time = datetime.now() + timedelta(days=1)
                        if "8am" in scheduled_date.lower() or "8:00" in scheduled_date:
                            scheduled_time = scheduled_time.replace(hour=8, minute=0, second=0)
                        elif "9am" in scheduled_date.lower() or "9:00" in scheduled_date:
                            scheduled_time = scheduled_time.replace(hour=9, minute=0, second=0)
                        else:
                            scheduled_time = scheduled_time.replace(hour=9, minute=0, second=0)
                    else:
                        # Try to parse date string
                        scheduled_time = datetime.fromisoformat(scheduled_date)
                except:
                    scheduled_time = datetime.now() + timedelta(hours=1)
            else:
                scheduled_time = datetime.now() + timedelta(hours=1)
            
            # Generate VPC ID
            vpc_id = f"VPC{datetime.now().strftime('%Y%m%d')}{truck.truck_number[-4:]}"
            
            # Create trip
            new_trip = Trip(
                vpc_id=vpc_id,
                truck_id=truck.id,
                origin_name=origin.upper(),
                destination_name=destination.upper(),
                status="scheduled",
                scheduled_departure_time=scheduled_time,
                created_at=datetime.utcnow()
            )
            
            session.add(new_trip)
            await session.commit()
            await session.refresh(new_trip)
            
            response = {
                "success": True,
                "trip_id": new_trip.vpc_id,
                "truck_number": truck_number,
                "origin": origin.upper(),
                "destination": destination.upper(),
                "scheduled_departure": scheduled_time.strftime("%Y-%m-%d %H:%M"),
                "status": "scheduled",
                "message": f"Trip {new_trip.vpc_id} created successfully"
            }
            
            logger.info(f"Created trip {new_trip.vpc_id} for truck {truck_number}")
            return response
            
    except Exception as e:
        logger.error(f"Error creating trip: {e}")
        return {"error": f"Failed to create trip: {str(e)}"}


async def get_fleet_status(filter: Optional[str] = None) -> Dict[str, Any]:
    """Get overall fleet status and summary"""
    try:
        async with get_async_session() as session:
            # Get all trucks
            truck_query = select(Truck)
            if filter:
                if filter.lower() == "active":
                    truck_query = truck_query.where(Truck.status.in_(["active", "in_trip"]))
                elif filter.lower() == "idle":
                    truck_query = truck_query.where(Truck.status == "idle")
                elif filter.lower() == "maintenance":
                    truck_query = truck_query.where(Truck.status == "maintenance")
            
            truck_result = await session.execute(truck_query)
            trucks = truck_result.scalars().all()
            
            # Count by status
            status_counts = {}
            company_counts = {}
            
            for truck in trucks:
                status_counts[truck.status] = status_counts.get(truck.status, 0) + 1
                company_counts[truck.company] = company_counts.get(truck.company, 0) + 1
            
            # Get active trips
            trip_result = await session.execute(
                select(Trip).where(Trip.status.in_(["scheduled", "in_progress"]))
            )
            active_trips = trip_result.scalars().all()
            
            # Get recent positions count (trucks with updates in last hour)
            one_hour_ago = datetime.utcnow() - timedelta(hours=1)
            recent_positions = await session.execute(
                select(VehiclePosition.truck_id)
                .where(VehiclePosition.timestamp > one_hour_ago)
                .distinct()
            )
            trucks_reporting = len(recent_positions.scalars().all())
            
            response = {
                "total_trucks": len(trucks),
                "trucks_reporting": trucks_reporting,
                "connectivity_percentage": round((trucks_reporting / len(trucks)) * 100, 1) if trucks else 0,
                "status_breakdown": status_counts,
                "company_breakdown": company_counts,
                "active_trips": len(active_trips),
                "filter_applied": filter or "none",
                "last_updated": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
            }
            
            if filter:
                response["filtered_trucks"] = len(trucks)
            
            logger.info(f"Retrieved fleet status (filter: {filter})")
            return response
            
    except Exception as e:
        logger.error(f"Error getting fleet status: {e}")
        return {"error": f"Failed to get fleet status: {str(e)}"}


async def get_trip_details(trip_id: str) -> Dict[str, Any]:
    """Get details of a specific trip"""
    try:
        async with get_async_session() as session:
            # Find trip by VPC ID or database ID
            trip_result = await session.execute(
                select(Trip, Truck)
                .join(Truck, Trip.truck_id == Truck.id)
                .where(Trip.vpc_id == trip_id.upper())
            )
            trip_row = trip_result.first()
            
            if not trip_row:
                return {"error": f"Trip {trip_id} not found"}
            
            trip, truck = trip_row
            
            response = {
                "trip_id": trip.vpc_id,
                "truck_number": truck.truck_number,
                "truck_company": truck.company,
                "origin": trip.origin_name,
                "destination": trip.destination_name,
                "status": trip.status,
                "created_at": trip.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                "scheduled_departure": trip.scheduled_departure_time.strftime("%Y-%m-%d %H:%M:%S") if trip.scheduled_departure_time else None,
                "started_at": trip.started_at.strftime("%Y-%m-%d %H:%M:%S") if trip.started_at else None,
                "completed_at": trip.completed_at.strftime("%Y-%m-%d %H:%M:%S") if trip.completed_at else None
            }
            
            # Calculate duration if trip is completed
            if trip.started_at and trip.completed_at:
                duration = trip.completed_at - trip.started_at
                response["duration_hours"] = round(duration.total_seconds() / 3600, 2)
            
            # Add distance if available
            if trip.distance_km:
                response["distance_km"] = trip.distance_km
            
            logger.info(f"Retrieved details for trip {trip_id}")
            return response
            
    except Exception as e:
        logger.error(f"Error getting trip details {trip_id}: {e}")
        return {"error": f"Failed to get trip details: {str(e)}"}


async def get_daily_summary(date: Optional[str] = None) -> Dict[str, Any]:
    """Get daily fleet performance summary"""
    try:
        # Parse date
        if date == "today" or not date:
            target_date = datetime.utcnow().date()
        else:
            try:
                target_date = datetime.fromisoformat(date).date()
            except:
                target_date = datetime.utcnow().date()
        
        start_time = datetime.combine(target_date, datetime.min.time())
        end_time = start_time + timedelta(days=1)
        
        async with get_async_session() as session:
            # Count trips for the day
            trip_result = await session.execute(
                select(Trip)
                .where(
                    Trip.created_at >= start_time,
                    Trip.created_at < end_time
                )
            )
            daily_trips = trip_result.scalars().all()
            
            # Count by status
            completed_trips = [t for t in daily_trips if t.status == "completed"]
            in_progress_trips = [t for t in daily_trips if t.status == "in_progress"]
            scheduled_trips = [t for t in daily_trips if t.status == "scheduled"]
            
            # Get active trucks count
            truck_result = await session.execute(
                select(Truck).where(Truck.status.in_(["active", "in_trip"]))
            )
            active_trucks = len(truck_result.scalars().all())
            
            # Calculate total distance for completed trips
            total_distance = sum(t.distance_km for t in completed_trips if t.distance_km)
            
            # Calculate average trip time for completed trips
            trip_durations = []
            for trip in completed_trips:
                if trip.started_at and trip.completed_at:
                    duration = (trip.completed_at - trip.started_at).total_seconds() / 3600
                    trip_durations.append(duration)
            
            avg_trip_time = sum(trip_durations) / len(trip_durations) if trip_durations else 0
            
            response = {
                "date": target_date.strftime("%Y-%m-%d"),
                "total_trips": len(daily_trips),
                "completed_trips": len(completed_trips),
                "in_progress_trips": len(in_progress_trips),
                "scheduled_trips": len(scheduled_trips),
                "active_trucks": active_trucks,
                "total_distance_km": round(total_distance, 1),
                "average_trip_time_hours": round(avg_trip_time, 2),
                "completion_rate": round((len(completed_trips) / len(daily_trips)) * 100, 1) if daily_trips else 0
            }
            
            logger.info(f"Generated daily summary for {target_date}")
            return response
            
    except Exception as e:
        logger.error(f"Error generating daily summary: {e}")
        return {"error": f"Failed to generate daily summary: {str(e)}"}