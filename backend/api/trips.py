from fastapi import APIRouter, HTTPException
from typing import List

router = APIRouter()

@router.get("/")
async def list_trips():
    """List all trips"""
    return {"message": "List trips endpoint"}

@router.post("/")
async def create_trips():
    """Create new trips"""
    return {"message": "Create trips endpoint"}

@router.get("/{id}")
async def get_trips(id: str):
    """Get specific trips"""
    return {"message": f"Get trips {id}"}
