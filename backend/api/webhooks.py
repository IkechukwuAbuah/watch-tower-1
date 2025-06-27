"""
Webhook endpoints for external integrations
"""

from fastapi import APIRouter, Depends, HTTPException, Header, Request
from sqlalchemy.ext.asyncio import AsyncSession

from db.session import get_db
from services import LocoNavService
from schemas import LocoNavWebhookPayload, SuccessResponse

router = APIRouter()


@router.post("/loconav/position", response_model=SuccessResponse)
async def loconav_position_webhook(
    payload: LocoNavWebhookPayload,
    request: Request,
    x_loconav_signature: str = Header(None, alias="X-LocoNav-Signature"),
    db: AsyncSession = Depends(get_db)
):
    """
    Receive GPS position updates from LocoNav
    
    This webhook is called by LocoNav whenever a vehicle position is updated.
    The webhook payload includes:
    - Vehicle ID (must match a truck's loconav_vehicle_id)
    - GPS coordinates
    - Speed, heading, and other telemetry data
    - Optional event type (trip_start, trip_end, etc.)
    
    Security:
    - Validates HMAC signature if configured
    - Ignores unknown vehicle IDs (logs warning)
    """
    service = LocoNavService()
    
    # Verify webhook signature
    if x_loconav_signature:
        # Get raw body for signature verification
        body = await request.body()
        if not service.verify_webhook_signature(body.decode(), x_loconav_signature):
            raise HTTPException(
                status_code=401,
                detail="Invalid webhook signature"
            )
    
    # Process position update
    position = await service.process_position_update(db, payload)
    
    if position:
        return SuccessResponse(
            message="Position update processed successfully",
            data={
                "position_id": str(position.id),
                "truck_id": str(position.truck_id),
                "timestamp": position.timestamp.isoformat()
            }
        )
    else:
        return SuccessResponse(
            message="Position update received but vehicle not found",
            data={"vehicle_id": payload.vehicle_id}
        )


@router.get("/loconav/health")
async def loconav_webhook_health():
    """
    Health check endpoint for LocoNav webhook configuration
    
    LocoNav can use this endpoint to verify the webhook URL is active
    """
    return {"status": "healthy", "service": "loconav-webhook"}