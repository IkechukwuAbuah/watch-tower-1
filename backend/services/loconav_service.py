"""
LocoNav API Integration Service
"""

import httpx
import os
from typing import Dict, List, Optional
from datetime import datetime

class LocoNavService:
    def __init__(self):
        self.base_url = os.getenv("LOCONAV_API_BASE_URL", "https://api.a.loconav.com")
        self.auth_token = os.getenv("LOCONAV_USER_TOKEN")
        
        if not self.auth_token:
            raise ValueError("LOCONAV_USER_TOKEN not set in environment")
            
        self.headers = {
            "User-Authentication": self.auth_token,
            "Content-Type": "application/json"
        }
    
    async def test_connection(self) -> bool:
        """Test LocoNav API connection"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/integration/api/v1/user",
                    headers=self.headers
                )
                return response.status_code == 200
        except Exception as e:
            print(f"LocoNav connection error: {e}")
            return False
    
    async def get_vehicle_location(self, vehicle_id: str) -> Dict:
        """Get current vehicle location"""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/integration/api/v1/vehicles/telematics/last_known",
                json={
                    "vehicleIds": [vehicle_id],
                    "sensors": ["gps", "ignition", "speed"]
                },
                headers=self.headers
            )
            response.raise_for_status()
            return response.json()
    
    async def create_trip(self, trip_data: Dict) -> Dict:
        """Create a new trip in LocoNav"""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/integration/api/v1/trips",
                json={"trip": trip_data},
                headers=self.headers
            )
            response.raise_for_status()
            return response.json()
