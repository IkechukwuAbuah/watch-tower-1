"""
AI-powered natural language interface API endpoints
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import Optional, Dict, Any
import logging

from services.ai_service import ai_service
from schemas import SuccessResponse

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/ai", tags=["AI Interface"])


class QueryRequest(BaseModel):
    """Natural language query request"""
    query: str
    user_context: Optional[Dict[str, Any]] = None


class QueryResponse(BaseModel):
    """AI query response"""
    response: str
    function_calls: list = []
    status: str
    processing_time_ms: Optional[int] = None


@router.post("/query", response_model=QueryResponse)
async def process_natural_language_query(request: QueryRequest):
    """
    Process natural language queries about fleet status and operations
    
    Examples:
    - "Where is truck T11985LA?"
    - "Create trip for T28737LA from ESSLIBRA to ECLAT tomorrow 8am"
    - "Show me fleet status"
    - "What trips are scheduled for today?"
    """
    try:
        logger.info(f"Processing AI query: {request.query[:100]}...")
        
        import time
        start_time = time.time()
        
        result = await ai_service.process_natural_language_query(
            request.query,
            request.user_context
        )
        
        processing_time = int((time.time() - start_time) * 1000)
        
        return QueryResponse(
            response=result["response"],
            function_calls=result.get("function_calls", []),
            status=result["status"],
            processing_time_ms=processing_time
        )
        
    except Exception as e:
        logger.error(f"AI query processing failed: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process query: {str(e)}"
        )


@router.post("/trip/create", response_model=QueryResponse)
async def create_trip_from_description(request: QueryRequest):
    """
    Create a trip from natural language description
    
    Example: "Create trip for T28737LA from ESSLIBRA to ECLAT tomorrow 8am"
    """
    try:
        logger.info(f"Creating trip from description: {request.query[:100]}...")
        
        result = await ai_service.create_trip_from_natural_language(
            request.query,
            request.user_context
        )
        
        return QueryResponse(
            response=result["response"],
            function_calls=result.get("function_calls", []),
            status=result["status"]
        )
        
    except Exception as e:
        logger.error(f"Trip creation from description failed: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to create trip: {str(e)}"
        )


@router.post("/fleet/status", response_model=QueryResponse)
async def get_fleet_status_ai(request: QueryRequest):
    """
    Get fleet status using natural language query
    
    Examples:
    - "Show me all active trucks"
    - "What's the fleet status?"
    - "How many trucks are idle?"
    """
    try:
        logger.info(f"Fleet status query: {request.query[:100]}...")
        
        result = await ai_service.query_fleet_status(
            request.query,
            request.user_context
        )
        
        return QueryResponse(
            response=result["response"],
            function_calls=result.get("function_calls", []),
            status=result["status"]
        )
        
    except Exception as e:
        logger.error(f"Fleet status query failed: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get fleet status: {str(e)}"
        )


@router.get("/functions", response_model=Dict[str, Any])
async def list_available_functions():
    """List all available AI functions and their descriptions"""
    try:
        functions = {
            "get_truck_location": {
                "description": "Get current location and status of a specific truck",
                "parameters": ["truck_number"],
                "example": "Where is truck T11985LA?"
            },
            "create_new_trip": {
                "description": "Create a new trip for a truck",
                "parameters": ["truck_number", "origin", "destination", "scheduled_date (optional)"],
                "example": "Create trip for T28737LA from ESSLIBRA to ECLAT tomorrow 8am"
            },
            "get_fleet_status": {
                "description": "Get overall fleet status and summary",
                "parameters": ["filter (optional)"],
                "example": "Show me fleet status" or "Show me active trucks"
            },
            "get_trip_details": {
                "description": "Get details of a specific trip",
                "parameters": ["trip_id"],
                "example": "Show me details for trip VPC20241225T123"
            },
            "get_daily_summary": {
                "description": "Get daily fleet performance summary",
                "parameters": ["date (optional)"],
                "example": "Show me today's summary" or "Daily summary for 2024-12-25"
            }
        }
        
        return {
            "available_functions": functions,
            "total_functions": len(functions),
            "usage_examples": [
                "Where is truck T11985LA?",
                "Create trip for T28737LA from ESSLIBRA to ECLAT tomorrow 8am",
                "Show me fleet status",
                "What's the daily summary?",
                "Show me details for trip VPC20241225T123"
            ]
        }
        
    except Exception as e:
        logger.error(f"Failed to list functions: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to list functions: {str(e)}"
        )


@router.post("/test/connection")
async def test_ai_connection():
    """Test OpenAI API connection"""
    try:
        # Simple test query
        result = await ai_service.process_natural_language_query(
            "Test connection - what is Watch Tower?",
            {"test": True}
        )
        
        return SuccessResponse(
            message="AI service connection successful",
            data={
                "status": result["status"],
                "response_length": len(result["response"]),
                "functions_available": len(ai_service.function_registry)
            }
        )
        
    except Exception as e:
        logger.error(f"AI connection test failed: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"AI connection test failed: {str(e)}"
        )