from fastapi import APIRouter, HTTPException
from typing import List

router = APIRouter()

@router.get("/")
async def list_trucks():
    """List all trucks"""
    return {"message": "List trucks endpoint"}

@router.post("/")
async def create_trucks():
    """Create new trucks"""
    return {"message": "Create trucks endpoint"}

@router.get("/{id}")
async def get_trucks(id: str):
    """Get specific trucks"""
    return {"message": f"Get trucks {id}"}
