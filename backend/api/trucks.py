"""
Truck management API endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import List, Optional
from uuid import UUID

from db.session import get_db
from models import Truck
from schemas import (
    TruckCreate,
    TruckUpdate,
    TruckResponse,
    TruckQueryParams,
    ErrorResponse,
    SuccessResponse
)

router = APIRouter()


@router.get("/", response_model=List[TruckResponse])
async def list_trucks(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(20, ge=1, le=100, description="Max records to return"),
    status: Optional[str] = Query(None, description="Filter by status"),
    company: Optional[str] = Query(None, description="Filter by company"),
    location: Optional[str] = Query(None, description="Filter by operating location"),
    db: AsyncSession = Depends(get_db)
):
    """
    List all trucks with optional filtering
    
    - **skip**: Number of records to skip for pagination
    - **limit**: Maximum number of records to return (max 100)
    - **status**: Filter by truck status (e.g., operational, maintenance)
    - **company**: Filter by operating company
    - **location**: Filter by operating location
    """
    query = select(Truck)
    
    # Apply filters
    if status:
        query = query.where(Truck.status == status)
    if company:
        query = query.where(Truck.company == company)
    if location:
        query = query.where(Truck.operating_location == location)
    
    # Apply pagination
    query = query.offset(skip).limit(limit)
    
    result = await db.execute(query)
    trucks = result.scalars().all()
    
    return trucks


@router.post("/", response_model=TruckResponse, status_code=201)
async def create_truck(
    truck_data: TruckCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Create a new truck
    
    - **truck_number**: Unique identifier for the truck
    - **loconav_vehicle_id**: Optional LocoNav system ID
    - **company**: Operating company name
    - **fleet_manager**: Fleet manager name
    - **status**: Operational status (default: operational)
    """
    # Check if truck number already exists
    existing = await db.execute(
        select(Truck).where(Truck.truck_number == truck_data.truck_number)
    )
    if existing.scalar_one_or_none():
        raise HTTPException(
            status_code=400,
            detail=f"Truck with number {truck_data.truck_number} already exists"
        )
    
    # Create new truck
    truck = Truck(**truck_data.model_dump())
    db.add(truck)
    await db.commit()
    await db.refresh(truck)
    
    return truck


@router.get("/{truck_id}", response_model=TruckResponse)
async def get_truck(
    truck_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """
    Get a specific truck by ID
    """
    result = await db.execute(
        select(Truck).where(Truck.id == truck_id)
    )
    truck = result.scalar_one_or_none()
    
    if not truck:
        raise HTTPException(
            status_code=404,
            detail=f"Truck with ID {truck_id} not found"
        )
    
    return truck


@router.put("/{truck_id}", response_model=TruckResponse)
async def update_truck(
    truck_id: UUID,
    truck_update: TruckUpdate,
    db: AsyncSession = Depends(get_db)
):
    """
    Update a truck's information
    """
    # Get existing truck
    result = await db.execute(
        select(Truck).where(Truck.id == truck_id)
    )
    truck = result.scalar_one_or_none()
    
    if not truck:
        raise HTTPException(
            status_code=404,
            detail=f"Truck with ID {truck_id} not found"
        )
    
    # Update fields
    update_data = truck_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(truck, field, value)
    
    await db.commit()
    await db.refresh(truck)
    
    return truck


@router.delete("/{truck_id}", response_model=SuccessResponse)
async def delete_truck(
    truck_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """
    Delete a truck (soft delete by setting status to 'decommissioned')
    """
    result = await db.execute(
        select(Truck).where(Truck.id == truck_id)
    )
    truck = result.scalar_one_or_none()
    
    if not truck:
        raise HTTPException(
            status_code=404,
            detail=f"Truck with ID {truck_id} not found"
        )
    
    # Soft delete by updating status
    truck.status = "decommissioned"
    await db.commit()
    
    return SuccessResponse(
        message=f"Truck {truck.truck_number} has been decommissioned",
        data={"truck_id": str(truck_id), "truck_number": truck.truck_number}
    )


@router.get("/by-number/{truck_number}", response_model=TruckResponse)
async def get_truck_by_number(
    truck_number: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Get a truck by its truck number
    """
    result = await db.execute(
        select(Truck).where(Truck.truck_number == truck_number)
    )
    truck = result.scalar_one_or_none()
    
    if not truck:
        raise HTTPException(
            status_code=404,
            detail=f"Truck with number {truck_number} not found"
        )
    
    return truck


@router.get("/stats/summary")
async def get_truck_stats(
    db: AsyncSession = Depends(get_db)
):
    """
    Get summary statistics for all trucks
    """
    # Get total trucks
    total_result = await db.execute(
        select(func.count(Truck.id))
    )
    total_trucks = total_result.scalar()
    
    # Get trucks by status
    status_result = await db.execute(
        select(
            Truck.status,
            func.count(Truck.id)
        ).group_by(Truck.status)
    )
    status_counts = {status: count for status, count in status_result.all()}
    
    # Get trucks by company
    company_result = await db.execute(
        select(
            Truck.company,
            func.count(Truck.id)
        ).group_by(Truck.company)
    )
    company_counts = {company: count for company, count in company_result.all() if company}
    
    return {
        "total_trucks": total_trucks,
        "by_status": status_counts,
        "by_company": company_counts,
        "operational_percentage": (
            (status_counts.get("operational", 0) / total_trucks * 100)
            if total_trucks > 0 else 0
        )
    }
