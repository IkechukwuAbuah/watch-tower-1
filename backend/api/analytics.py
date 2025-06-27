"""
Analytics API endpoints for fleet metrics and reporting
"""

from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_, case
from typing import Optional
from datetime import datetime, timedelta, date
from uuid import UUID

from db.session import get_db
from models import Truck, Trip, VehiclePosition
from schemas import (
    DailyMetricsResponse,
    TruckMetricsResponse,
    ErrorResponse
)

router = APIRouter()


@router.get("/daily", response_model=DailyMetricsResponse)
async def get_daily_metrics(
    date_filter: Optional[date] = Query(None, description="Date for metrics (default: today)"),
    db: AsyncSession = Depends(get_db)
):
    """
    Get daily fleet metrics
    
    Returns aggregated metrics for the entire fleet on a specific date:
    - Total and active trucks
    - Trip counts and completion rates
    - Total distance traveled
    - Average speed across fleet
    """
    # Default to today if no date provided
    target_date = date_filter or date.today()
    start_time = datetime.combine(target_date, datetime.min.time())
    end_time = datetime.combine(target_date, datetime.max.time())
    
    # Get total trucks
    total_trucks_result = await db.execute(
        select(func.count(Truck.id))
    )
    total_trucks = total_trucks_result.scalar() or 0
    
    # Get active trucks (trucks that had trips on this date)
    active_trucks_result = await db.execute(
        select(func.count(func.distinct(Trip.truck_id)))
        .where(
            and_(
                Trip.created_at >= start_time,
                Trip.created_at <= end_time
            )
        )
    )
    active_trucks = active_trucks_result.scalar() or 0
    
    # Get trip statistics
    trip_stats_result = await db.execute(
        select(
            func.count(Trip.id).label('total_trips'),
            func.count(case((Trip.status == 'completed', Trip.id))).label('completed_trips'),
            func.sum(Trip.distance_km).label('total_distance')
        )
        .where(
            and_(
                Trip.created_at >= start_time,
                Trip.created_at <= end_time
            )
        )
    )
    trip_stats = trip_stats_result.one()
    
    total_trips = trip_stats.total_trips or 0
    completed_trips = trip_stats.completed_trips or 0
    total_distance = float(trip_stats.total_distance or 0)
    
    # Get average speed from vehicle positions
    avg_speed_result = await db.execute(
        select(func.avg(VehiclePosition.speed))
        .where(
            and_(
                VehiclePosition.timestamp >= start_time,
                VehiclePosition.timestamp <= end_time,
                VehiclePosition.speed > 0  # Only consider moving vehicles
            )
        )
    )
    avg_speed = float(avg_speed_result.scalar() or 0)
    
    return DailyMetricsResponse(
        date=start_time,
        total_trucks=total_trucks,
        active_trucks=active_trucks,
        total_trips=total_trips,
        completed_trips=completed_trips,
        total_distance_km=round(total_distance, 2),
        average_speed_kmh=round(avg_speed, 2),
        fuel_efficiency_score=None  # To be implemented with fuel data
    )


@router.get("/trucks/{truck_id}", response_model=TruckMetricsResponse)
async def get_truck_metrics(
    truck_id: UUID,
    date_filter: Optional[date] = Query(None, description="Date for metrics (default: today)"),
    db: AsyncSession = Depends(get_db)
):
    """
    Get metrics for a specific truck
    
    Returns detailed metrics for a single truck on a specific date:
    - Distance traveled
    - Number of trips
    - Active hours (time with ignition on)
    - Speed statistics
    """
    # Verify truck exists
    truck_result = await db.execute(
        select(Truck).where(Truck.id == truck_id)
    )
    truck = truck_result.scalar_one_or_none()
    
    if not truck:
        raise HTTPException(
            status_code=404,
            detail=f"Truck with ID {truck_id} not found"
        )
    
    # Default to today if no date provided
    target_date = date_filter or date.today()
    start_time = datetime.combine(target_date, datetime.min.time())
    end_time = datetime.combine(target_date, datetime.max.time())
    
    # Get trip statistics for the truck
    trip_stats_result = await db.execute(
        select(
            func.count(Trip.id).label('trips_count'),
            func.sum(Trip.distance_km).label('total_distance')
        )
        .where(
            and_(
                Trip.truck_id == truck_id,
                Trip.created_at >= start_time,
                Trip.created_at <= end_time
            )
        )
    )
    trip_stats = trip_stats_result.one()
    
    trips_count = trip_stats.trips_count or 0
    total_distance = float(trip_stats.total_distance or 0)
    
    # Get position statistics
    position_stats_result = await db.execute(
        select(
            func.avg(VehiclePosition.speed).label('avg_speed'),
            func.max(VehiclePosition.speed).label('max_speed'),
            func.count(case((VehiclePosition.ignition == True, 1))).label('ignition_on_count'),
            func.count(VehiclePosition.id).label('total_positions')
        )
        .where(
            and_(
                VehiclePosition.truck_id == truck_id,
                VehiclePosition.timestamp >= start_time,
                VehiclePosition.timestamp <= end_time
            )
        )
    )
    position_stats = position_stats_result.one()
    
    avg_speed = float(position_stats.avg_speed or 0)
    max_speed = float(position_stats.max_speed or 0)
    
    # Calculate active hours (rough estimate based on position frequency)
    # Assuming positions are recorded every 30 seconds when ignition is on
    ignition_on_count = position_stats.ignition_on_count or 0
    active_hours = round(ignition_on_count * 0.5 / 60, 1)  # Convert to hours
    
    return TruckMetricsResponse(
        truck_id=truck_id,
        truck_number=truck.truck_number,
        date=start_time,
        distance_km=round(total_distance, 2),
        trips_count=trips_count,
        active_hours=active_hours,
        average_speed_kmh=round(avg_speed, 2),
        max_speed_kmh=round(max_speed, 2)
    )


@router.get("/fleet/summary")
async def get_fleet_summary(
    days: int = Query(7, ge=1, le=30, description="Number of days to analyze"),
    db: AsyncSession = Depends(get_db)
):
    """
    Get fleet summary statistics over a period
    
    Returns aggregated fleet metrics over the specified number of days:
    - Fleet utilization trends
    - Trip completion rates
    - Distance and speed analytics
    """
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=days)
    
    # Get daily metrics
    daily_metrics_result = await db.execute(
        select(
            func.date(Trip.created_at).label('date'),
            func.count(func.distinct(Trip.truck_id)).label('active_trucks'),
            func.count(Trip.id).label('total_trips'),
            func.count(case((Trip.status == 'completed', Trip.id))).label('completed_trips'),
            func.sum(Trip.distance_km).label('total_distance')
        )
        .where(Trip.created_at >= start_date)
        .group_by(func.date(Trip.created_at))
        .order_by(func.date(Trip.created_at))
    )
    
    daily_data = []
    for row in daily_metrics_result:
        daily_data.append({
            "date": row.date,
            "active_trucks": row.active_trucks,
            "total_trips": row.total_trips,
            "completed_trips": row.completed_trips,
            "total_distance_km": float(row.total_distance or 0),
            "completion_rate": (
                round(row.completed_trips / row.total_trips * 100, 1)
                if row.total_trips > 0 else 0
            )
        })
    
    # Get total fleet size
    total_trucks_result = await db.execute(
        select(func.count(Truck.id))
    )
    total_trucks = total_trucks_result.scalar() or 0
    
    # Calculate averages
    if daily_data:
        avg_active_trucks = sum(d["active_trucks"] for d in daily_data) / len(daily_data)
        avg_trips_per_day = sum(d["total_trips"] for d in daily_data) / len(daily_data)
        avg_distance_per_day = sum(d["total_distance_km"] for d in daily_data) / len(daily_data)
        avg_completion_rate = sum(d["completion_rate"] for d in daily_data) / len(daily_data)
    else:
        avg_active_trucks = 0
        avg_trips_per_day = 0
        avg_distance_per_day = 0
        avg_completion_rate = 0
    
    return {
        "period_days": days,
        "total_fleet_size": total_trucks,
        "average_active_trucks_per_day": round(avg_active_trucks, 1),
        "average_trips_per_day": round(avg_trips_per_day, 1),
        "average_distance_per_day_km": round(avg_distance_per_day, 1),
        "average_completion_rate": round(avg_completion_rate, 1),
        "daily_metrics": daily_data,
        "fleet_utilization_percentage": (
            round(avg_active_trucks / total_trucks * 100, 1)
            if total_trucks > 0 else 0
        )
    }


@router.get("/trips/by-status")
async def get_trips_by_status(
    days: int = Query(7, ge=1, le=30, description="Number of days to analyze"),
    db: AsyncSession = Depends(get_db)
):
    """
    Get trip breakdown by status over a period
    """
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=days)
    
    # Get trip counts by status
    status_result = await db.execute(
        select(
            Trip.status,
            func.count(Trip.id).label('count')
        )
        .where(Trip.created_at >= start_date)
        .group_by(Trip.status)
    )
    
    status_breakdown = {row.status: row.count for row in status_result}
    total_trips = sum(status_breakdown.values())
    
    # Calculate percentages
    status_percentages = {
        status: round(count / total_trips * 100, 1) if total_trips > 0 else 0
        for status, count in status_breakdown.items()
    }
    
    return {
        "period_days": days,
        "total_trips": total_trips,
        "status_counts": status_breakdown,
        "status_percentages": status_percentages
    }


@router.get("/performance/top-trucks")
async def get_top_performing_trucks(
    days: int = Query(7, ge=1, le=30, description="Number of days to analyze"),
    limit: int = Query(10, ge=1, le=50, description="Number of trucks to return"),
    db: AsyncSession = Depends(get_db)
):
    """
    Get top performing trucks by distance traveled and trip completion
    """
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=days)
    
    # Get truck performance metrics
    performance_result = await db.execute(
        select(
            Trip.truck_id,
            Truck.truck_number,
            func.count(Trip.id).label('total_trips'),
            func.count(case((Trip.status == 'completed', Trip.id))).label('completed_trips'),
            func.sum(Trip.distance_km).label('total_distance')
        )
        .join(Truck, Trip.truck_id == Truck.id)
        .where(Trip.created_at >= start_date)
        .group_by(Trip.truck_id, Truck.truck_number)
        .order_by(func.sum(Trip.distance_km).desc())
        .limit(limit)
    )
    
    top_trucks = []
    for row in performance_result:
        completion_rate = (
            round(row.completed_trips / row.total_trips * 100, 1)
            if row.total_trips > 0 else 0
        )
        
        top_trucks.append({
            "truck_id": str(row.truck_id),
            "truck_number": row.truck_number,
            "total_trips": row.total_trips,
            "completed_trips": row.completed_trips,
            "total_distance_km": float(row.total_distance or 0),
            "completion_rate": completion_rate
        })
    
    return {
        "period_days": days,
        "top_trucks": top_trucks
    }