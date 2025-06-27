"""
Trip management API endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_
from sqlalchemy.orm import selectinload
from geoalchemy2 import WKTElement
from typing import List, Optional
from uuid import UUID
from datetime import datetime

from db.session import get_db
from models import Trip, Truck
from schemas import (
    TripCreate,
    TripUpdate,
    TripResponse,
    TripQueryParams,
    ErrorResponse,
    SuccessResponse,
    LocationSchema,
    GeoJSONPointSchema
)

router = APIRouter()


def location_to_geojson(location) -> Optional[GeoJSONPointSchema]:
    """Convert PostGIS Geography to GeoJSON"""
    if not location:
        return None
    # Extract coordinates from WKT format
    coords = location.to_shape().__geo_interface__['coordinates']
    return GeoJSONPointSchema(coordinates=coords)


@router.get("/", response_model=List[TripResponse])
async def list_trips(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(20, ge=1, le=100, description="Max records to return"),
    status: Optional[str] = Query(None, description="Filter by status"),
    truck_id: Optional[UUID] = Query(None, description="Filter by truck ID"),
    date_from: Optional[datetime] = Query(None, description="Filter from date"),
    date_to: Optional[datetime] = Query(None, description="Filter to date"),
    db: AsyncSession = Depends(get_db)
):
    """
    List all trips with optional filtering
    
    - **skip**: Number of records to skip for pagination
    - **limit**: Maximum number of records to return (max 100)
    - **status**: Filter by trip status (scheduled, in_progress, completed, cancelled)
    - **truck_id**: Filter by assigned truck
    - **date_from**: Filter trips created after this date
    - **date_to**: Filter trips created before this date
    """
    query = select(Trip).options(selectinload(Trip.truck))
    
    # Apply filters
    conditions = []
    if status:
        conditions.append(Trip.status == status)
    if truck_id:
        conditions.append(Trip.truck_id == truck_id)
    if date_from:
        conditions.append(Trip.created_at >= date_from)
    if date_to:
        conditions.append(Trip.created_at <= date_to)
    
    if conditions:
        query = query.where(and_(*conditions))
    
    # Order by created_at desc and apply pagination
    query = query.order_by(Trip.created_at.desc()).offset(skip).limit(limit)
    
    result = await db.execute(query)
    trips = result.scalars().all()
    
    # Convert to response model with GeoJSON
    response_trips = []
    for trip in trips:
        trip_dict = {
            "id": trip.id,
            "vpc_id": trip.vpc_id,
            "loconav_trip_id": trip.loconav_trip_id,
            "truck_id": trip.truck_id,
            "status": trip.status,
            "origin_address": trip.origin_address,
            "destination_address": trip.destination_address,
            "distance_km": trip.distance_km,
            "estimated_duration_minutes": trip.estimated_duration_minutes,
            "created_at": trip.created_at,
            "started_at": trip.started_at,
            "completed_at": trip.completed_at,
            "origin_geojson": location_to_geojson(trip.origin_location),
            "destination_geojson": location_to_geojson(trip.destination_location)
        }
        response_trips.append(TripResponse(**trip_dict))
    
    return response_trips


@router.post("/", response_model=TripResponse, status_code=201)
async def create_trip(
    trip_data: TripCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Create a new trip
    
    - **vpc_id**: Unique VPC identifier for the trip
    - **truck_id**: ID of the truck assigned to this trip
    - **origin_location**: Origin coordinates (latitude, longitude)
    - **destination_location**: Destination coordinates (latitude, longitude)
    - **status**: Trip status (default: scheduled)
    """
    # Verify truck exists
    truck_result = await db.execute(
        select(Truck).where(Truck.id == trip_data.truck_id)
    )
    truck = truck_result.scalar_one_or_none()
    
    if not truck:
        raise HTTPException(
            status_code=404,
            detail=f"Truck with ID {trip_data.truck_id} not found"
        )
    
    # Check if VPC ID already exists
    existing = await db.execute(
        select(Trip).where(Trip.vpc_id == trip_data.vpc_id)
    )
    if existing.scalar_one_or_none():
        raise HTTPException(
            status_code=400,
            detail=f"Trip with VPC ID {trip_data.vpc_id} already exists"
        )
    
    # Create trip with PostGIS geography points
    trip_dict = trip_data.model_dump(exclude={'origin_location', 'destination_location'})
    trip = Trip(**trip_dict)
    
    # Convert location schemas to PostGIS WKT
    if trip_data.origin_location:
        trip.origin_location = WKTElement(
            trip_data.origin_location.to_wkt(),
            srid=4326
        )
    
    if trip_data.destination_location:
        trip.destination_location = WKTElement(
            trip_data.destination_location.to_wkt(),
            srid=4326
        )
    
    db.add(trip)
    await db.commit()
    await db.refresh(trip)
    
    # Prepare response
    trip_response = TripResponse(
        id=trip.id,
        vpc_id=trip.vpc_id,
        loconav_trip_id=trip.loconav_trip_id,
        truck_id=trip.truck_id,
        status=trip.status,
        origin_address=trip.origin_address,
        destination_address=trip.destination_address,
        distance_km=trip.distance_km,
        estimated_duration_minutes=trip.estimated_duration_minutes,
        created_at=trip.created_at,
        started_at=trip.started_at,
        completed_at=trip.completed_at,
        origin_geojson=location_to_geojson(trip.origin_location),
        destination_geojson=location_to_geojson(trip.destination_location)
    )
    
    return trip_response


@router.get("/{trip_id}", response_model=TripResponse)
async def get_trip(
    trip_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """
    Get a specific trip by ID
    """
    result = await db.execute(
        select(Trip)
        .options(selectinload(Trip.truck))
        .where(Trip.id == trip_id)
    )
    trip = result.scalar_one_or_none()
    
    if not trip:
        raise HTTPException(
            status_code=404,
            detail=f"Trip with ID {trip_id} not found"
        )
    
    # Convert to response
    trip_response = TripResponse(
        id=trip.id,
        vpc_id=trip.vpc_id,
        loconav_trip_id=trip.loconav_trip_id,
        truck_id=trip.truck_id,
        status=trip.status,
        origin_address=trip.origin_address,
        destination_address=trip.destination_address,
        distance_km=trip.distance_km,
        estimated_duration_minutes=trip.estimated_duration_minutes,
        created_at=trip.created_at,
        started_at=trip.started_at,
        completed_at=trip.completed_at,
        origin_geojson=location_to_geojson(trip.origin_location),
        destination_geojson=location_to_geojson(trip.destination_location)
    )
    
    return trip_response


@router.put("/{trip_id}", response_model=TripResponse)
async def update_trip(
    trip_id: UUID,
    trip_update: TripUpdate,
    db: AsyncSession = Depends(get_db)
):
    """
    Update a trip's information
    """
    # Get existing trip
    result = await db.execute(
        select(Trip).where(Trip.id == trip_id)
    )
    trip = result.scalar_one_or_none()
    
    if not trip:
        raise HTTPException(
            status_code=404,
            detail=f"Trip with ID {trip_id} not found"
        )
    
    # Update fields
    update_data = trip_update.model_dump(exclude_unset=True, exclude={'origin_location', 'destination_location'})
    
    # Handle location updates
    if trip_update.origin_location is not None:
        trip.origin_location = WKTElement(
            trip_update.origin_location.to_wkt(),
            srid=4326
        )
    
    if trip_update.destination_location is not None:
        trip.destination_location = WKTElement(
            trip_update.destination_location.to_wkt(),
            srid=4326
        )
    
    # Update other fields
    for field, value in update_data.items():
        setattr(trip, field, value)
    
    await db.commit()
    await db.refresh(trip)
    
    # Prepare response
    trip_response = TripResponse(
        id=trip.id,
        vpc_id=trip.vpc_id,
        loconav_trip_id=trip.loconav_trip_id,
        truck_id=trip.truck_id,
        status=trip.status,
        origin_address=trip.origin_address,
        destination_address=trip.destination_address,
        distance_km=trip.distance_km,
        estimated_duration_minutes=trip.estimated_duration_minutes,
        created_at=trip.created_at,
        started_at=trip.started_at,
        completed_at=trip.completed_at,
        origin_geojson=location_to_geojson(trip.origin_location),
        destination_geojson=location_to_geojson(trip.destination_location)
    )
    
    return trip_response


@router.post("/{trip_id}/start", response_model=TripResponse)
async def start_trip(
    trip_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """
    Start a scheduled trip
    """
    result = await db.execute(
        select(Trip).where(Trip.id == trip_id)
    )
    trip = result.scalar_one_or_none()
    
    if not trip:
        raise HTTPException(
            status_code=404,
            detail=f"Trip with ID {trip_id} not found"
        )
    
    if trip.status != "scheduled":
        raise HTTPException(
            status_code=400,
            detail=f"Cannot start trip in status: {trip.status}"
        )
    
    trip.status = "in_progress"
    trip.started_at = datetime.utcnow()
    
    await db.commit()
    await db.refresh(trip)
    
    # Prepare response
    trip_response = TripResponse(
        id=trip.id,
        vpc_id=trip.vpc_id,
        loconav_trip_id=trip.loconav_trip_id,
        truck_id=trip.truck_id,
        status=trip.status,
        origin_address=trip.origin_address,
        destination_address=trip.destination_address,
        distance_km=trip.distance_km,
        estimated_duration_minutes=trip.estimated_duration_minutes,
        created_at=trip.created_at,
        started_at=trip.started_at,
        completed_at=trip.completed_at,
        origin_geojson=location_to_geojson(trip.origin_location),
        destination_geojson=location_to_geojson(trip.destination_location)
    )
    
    return trip_response


@router.post("/{trip_id}/complete", response_model=TripResponse)
async def complete_trip(
    trip_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """
    Complete an in-progress trip
    """
    result = await db.execute(
        select(Trip).where(Trip.id == trip_id)
    )
    trip = result.scalar_one_or_none()
    
    if not trip:
        raise HTTPException(
            status_code=404,
            detail=f"Trip with ID {trip_id} not found"
        )
    
    if trip.status != "in_progress":
        raise HTTPException(
            status_code=400,
            detail=f"Cannot complete trip in status: {trip.status}"
        )
    
    trip.status = "completed"
    trip.completed_at = datetime.utcnow()
    
    await db.commit()
    await db.refresh(trip)
    
    # Prepare response
    trip_response = TripResponse(
        id=trip.id,
        vpc_id=trip.vpc_id,
        loconav_trip_id=trip.loconav_trip_id,
        truck_id=trip.truck_id,
        status=trip.status,
        origin_address=trip.origin_address,
        destination_address=trip.destination_address,
        distance_km=trip.distance_km,
        estimated_duration_minutes=trip.estimated_duration_minutes,
        created_at=trip.created_at,
        started_at=trip.started_at,
        completed_at=trip.completed_at,
        origin_geojson=location_to_geojson(trip.origin_location),
        destination_geojson=location_to_geojson(trip.destination_location)
    )
    
    return trip_response


@router.post("/{trip_id}/cancel", response_model=SuccessResponse)
async def cancel_trip(
    trip_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """
    Cancel a scheduled or in-progress trip
    """
    result = await db.execute(
        select(Trip).where(Trip.id == trip_id)
    )
    trip = result.scalar_one_or_none()
    
    if not trip:
        raise HTTPException(
            status_code=404,
            detail=f"Trip with ID {trip_id} not found"
        )
    
    if trip.status in ["completed", "cancelled"]:
        raise HTTPException(
            status_code=400,
            detail=f"Cannot cancel trip in status: {trip.status}"
        )
    
    trip.status = "cancelled"
    
    await db.commit()
    
    return SuccessResponse(
        message=f"Trip {trip.vpc_id} has been cancelled",
        data={"trip_id": str(trip_id), "vpc_id": trip.vpc_id}
    )


@router.get("/by-vpc-id/{vpc_id}", response_model=TripResponse)
async def get_trip_by_vpc_id(
    vpc_id: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Get a trip by its VPC ID
    """
    result = await db.execute(
        select(Trip)
        .options(selectinload(Trip.truck))
        .where(Trip.vpc_id == vpc_id)
    )
    trip = result.scalar_one_or_none()
    
    if not trip:
        raise HTTPException(
            status_code=404,
            detail=f"Trip with VPC ID {vpc_id} not found"
        )
    
    # Convert to response
    trip_response = TripResponse(
        id=trip.id,
        vpc_id=trip.vpc_id,
        loconav_trip_id=trip.loconav_trip_id,
        truck_id=trip.truck_id,
        status=trip.status,
        origin_address=trip.origin_address,
        destination_address=trip.destination_address,
        distance_km=trip.distance_km,
        estimated_duration_minutes=trip.estimated_duration_minutes,
        created_at=trip.created_at,
        started_at=trip.started_at,
        completed_at=trip.completed_at,
        origin_geojson=location_to_geojson(trip.origin_location),
        destination_geojson=location_to_geojson(trip.destination_location)
    )
    
    return trip_response