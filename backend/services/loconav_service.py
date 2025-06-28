"""
LocoNav API Integration Service - Complete implementation
"""

import httpx
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime
from core.config import settings

logger = logging.getLogger(__name__)


class LocoNavAPIService:
    """Enhanced LocoNav API client with comprehensive fleet management features"""
    
    def __init__(self):
        self.base_url = settings.loconav_base_url
        self.user_token = settings.loconav_user_token
        self.timeout = settings.loconav_timeout
        
        if not self.user_token:
            raise ValueError("LOCONAV_USER_TOKEN not configured")
            
        self.headers = {
            "User-Authentication": self.user_token,
            "Content-Type": "application/json"
        }
    
    async def test_connection(self) -> bool:
        """Test LocoNav API connection"""
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(
                    f"{self.base_url}/integration/api/v1/user",
                    headers=self.headers
                )
                success = response.status_code == 200
                logger.info(f"LocoNav connection test: {'success' if success else 'failed'}")
                return success
        except Exception as e:
            logger.error(f"LocoNav connection error: {e}")
            return False
    
    async def get_vehicle_location(self, vehicle_id: str) -> Optional[Dict[str, Any]]:
        """Get current vehicle location and telemetry"""
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    f"{self.base_url}/integration/api/v1/vehicles/telematics/last_known",
                    json={
                        "vehicleIds": [vehicle_id],
                        "sensors": ["gps", "ignition", "speed", "heading", "altitude"]
                    },
                    headers=self.headers
                )
                response.raise_for_status()
                data = response.json()
                
                logger.info(f"Retrieved location for vehicle {vehicle_id}")
                return data
                
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error getting vehicle location {vehicle_id}: {e.response.status_code}")
            return None
        except Exception as e:
            logger.error(f"Error getting vehicle location {vehicle_id}: {e}")
            return None
    
    async def get_vehicles_list(self, page: int = 1, limit: int = 100) -> Optional[Dict[str, Any]]:
        """Get list of all vehicles with pagination"""
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(
                    f"{self.base_url}/integration/api/v1/vehicles",
                    params={"page": page, "limit": limit},
                    headers=self.headers
                )
                response.raise_for_status()
                return response.json()
                
        except Exception as e:
            logger.error(f"Error getting vehicles list: {e}")
            return None
    
    async def create_trip(self, trip_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Create a new trip in LocoNav"""
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    f"{self.base_url}/integration/api/v1/trips",
                    json={"trip": trip_data},
                    headers=self.headers
                )
                response.raise_for_status()
                result = response.json()
                
                logger.info(f"Created trip {result.get('trip', {}).get('id', 'unknown')}")
                return result
                
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error creating trip: {e.response.status_code} - {e.response.text}")
            return None
        except Exception as e:
            logger.error(f"Error creating trip: {e}")
            return None
    
    async def get_trip_details(self, trip_id: str) -> Optional[Dict[str, Any]]:
        """Get details of a specific trip"""
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(
                    f"{self.base_url}/integration/api/v1/trips/{trip_id}",
                    headers=self.headers
                )
                response.raise_for_status()
                return response.json()
                
        except Exception as e:
            logger.error(f"Error getting trip details {trip_id}: {e}")
            return None
    
    async def update_trip_status(self, trip_id: str, status: str) -> bool:
        """Update trip status"""
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.patch(
                    f"{self.base_url}/integration/api/v1/trips/{trip_id}",
                    json={"status": status},
                    headers=self.headers
                )
                response.raise_for_status()
                
                logger.info(f"Updated trip {trip_id} status to {status}")
                return True
                
        except Exception as e:
            logger.error(f"Error updating trip status {trip_id}: {e}")
            return False
    
    async def get_geofences(self) -> Optional[List[Dict[str, Any]]]:
        """Get all geofences"""
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(
                    f"{self.base_url}/integration/api/v1/geofences",
                    headers=self.headers
                )
                response.raise_for_status()
                return response.json()
                
        except Exception as e:
            logger.error(f"Error getting geofences: {e}")
            return None
    
    async def get_vehicle_trips(
        self, 
        vehicle_id: str, 
        start_date: datetime, 
        end_date: datetime
    ) -> Optional[List[Dict[str, Any]]]:
        """Get trips for a vehicle in date range"""
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(
                    f"{self.base_url}/integration/api/v1/vehicles/{vehicle_id}/trips",
                    params={
                        "startDate": start_date.isoformat(),
                        "endDate": end_date.isoformat()
                    },
                    headers=self.headers
                )
                response.raise_for_status()
                return response.json()
                
        except Exception as e:
            logger.error(f"Error getting vehicle trips {vehicle_id}: {e}")
            return None
    
    async def get_vehicle_route_history(
        self, 
        vehicle_id: str, 
        start_time: datetime, 
        end_time: datetime
    ) -> Optional[List[Dict[str, Any]]]:
        """Get vehicle route history (GPS points)"""
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    f"{self.base_url}/integration/api/v1/vehicles/telematics/history",
                    json={
                        "vehicleIds": [vehicle_id],
                        "startTime": start_time.isoformat(),
                        "endTime": end_time.isoformat(),
                        "sensors": ["gps", "speed", "ignition"]
                    },
                    headers=self.headers
                )
                response.raise_for_status()
                return response.json()
                
        except Exception as e:
            logger.error(f"Error getting vehicle route history {vehicle_id}: {e}")
            return None
    
    async def create_geofence(self, geofence_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Create a new geofence"""
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    f"{self.base_url}/integration/api/v1/geofences",
                    json=geofence_data,
                    headers=self.headers
                )
                response.raise_for_status()
                result = response.json()
                
                logger.info(f"Created geofence {result.get('id', 'unknown')}")
                return result
                
        except Exception as e:
            logger.error(f"Error creating geofence: {e}")
            return None


# Global instance
loconav_api_service = LocoNavAPIService()
