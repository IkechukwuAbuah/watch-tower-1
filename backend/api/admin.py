"""
Admin API endpoints for system management
"""

import os
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, Any

from db.session import get_db
from services import GoogleSheetsService
from schemas import SuccessResponse

router = APIRouter()


@router.post("/sync/google-sheets", response_model=SuccessResponse)
async def trigger_google_sheets_sync(
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db)
):
    """
    Manually trigger Google Sheets sync
    
    This endpoint initiates a sync of truck master data from Google Sheets.
    The sync runs in the background and performs the following:
    - Fetches all truck data from the configured Google Sheet
    - Updates existing trucks with new information
    - Creates new trucks if they don't exist
    - Marks trucks as inactive if they're not in the sheet
    
    Note: In production, this would typically be triggered by a scheduled task
    """
    service = GoogleSheetsService()
    
    # Check if service is configured
    status = await service.get_sync_status(db)
    if not status['client_configured']:
        raise HTTPException(
            status_code=503,
            detail="Google Sheets client not configured. Check credentials and environment variables."
        )
    
    # Run sync in background
    async def run_sync():
        async with db:
            await service.sync_trucks(db)
    
    background_tasks.add_task(run_sync)
    
    return SuccessResponse(
        message="Google Sheets sync initiated",
        data={
            "current_trucks": status['total_trucks'],
            "spreadsheet_id": status['spreadsheet_id']
        }
    )


@router.get("/sync/google-sheets/status")
async def get_google_sheets_sync_status(
    db: AsyncSession = Depends(get_db)
) -> Dict[str, Any]:
    """
    Get Google Sheets sync status
    
    Returns information about:
    - Total trucks in database
    - Trucks with LocoNav IDs
    - Inactive trucks
    - Configuration status
    """
    service = GoogleSheetsService()
    return await service.get_sync_status(db)


@router.get("/system/status")
async def get_system_status(
    db: AsyncSession = Depends(get_db)
) -> Dict[str, Any]:
    """
    Get overall system status
    
    Returns health check for all integrated services
    """
    # Check database
    try:
        await db.execute("SELECT 1")
        db_status = "healthy"
    except Exception as e:
        db_status = f"unhealthy: {str(e)}"
    
    # Check services
    google_sheets_service = GoogleSheetsService()
    sheets_configured = google_sheets_service.client is not None
    
    return {
        "status": "operational",
        "services": {
            "database": db_status,
            "google_sheets": "configured" if sheets_configured else "not configured",
            "loconav_webhook": "active",  # Always active if endpoint is available
        },
        "environment": {
            "has_google_credentials": bool(os.getenv("GOOGLE_SHEETS_CREDENTIALS_PATH")),
            "has_loconav_key": bool(os.getenv("LOCONAV_API_KEY")),
            "has_openai_key": bool(os.getenv("OPENAI_API_KEY")),
            "has_slack_token": bool(os.getenv("SLACK_BOT_TOKEN")),
        }
    }