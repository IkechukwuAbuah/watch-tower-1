"""
Google Sheets integration for master data synchronization
"""

import os
import json
from typing import List, Dict, Any, Optional
from datetime import datetime

import gspread
from google.oauth2.service_account import Credentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from sqlalchemy.dialects.postgresql import insert

from models import Truck


class GoogleSheetsService:
    """Sync truck master data from Google Sheets"""
    
    SCOPES = [
        'https://www.googleapis.com/auth/spreadsheets.readonly',
        'https://www.googleapis.com/auth/drive.readonly'
    ]
    
    def __init__(self):
        self.credentials_path = os.getenv("GOOGLE_SHEETS_CREDENTIALS_PATH")
        self.spreadsheet_id = os.getenv("GOOGLE_SHEETS_SPREADSHEET_ID")
        self.client = None
        self._setup_client()
    
    def _setup_client(self):
        """Initialize Google Sheets client with service account"""
        if not self.credentials_path or not os.path.exists(self.credentials_path):
            print("Warning: Google Sheets credentials not found")
            return
            
        try:
            # Load credentials from JSON file
            with open(self.credentials_path, 'r') as f:
                creds_info = json.load(f)
            
            credentials = Credentials.from_service_account_info(
                creds_info,
                scopes=self.SCOPES
            )
            
            self.client = gspread.authorize(credentials)
        except Exception as e:
            print(f"Error setting up Google Sheets client: {e}")
    
    def fetch_truck_data(self) -> List[Dict[str, Any]]:
        """
        Fetch truck master data from Google Sheets
        
        Expected columns:
        - Truck Number
        - LocoNav Vehicle ID
        - Company
        - Fleet Manager
        - Status
        - Brand
        - Trailer Size
        - Operating Location
        
        Returns:
            List of truck data dictionaries
        """
        if not self.client or not self.spreadsheet_id:
            print("Google Sheets client not configured")
            return []
        
        try:
            # Open spreadsheet and get first sheet
            spreadsheet = self.client.open_by_key(self.spreadsheet_id)
            worksheet = spreadsheet.get_worksheet(0)  # First sheet
            
            # Get all records as list of dicts
            records = worksheet.get_all_records()
            
            # Map column names to our schema
            trucks = []
            for record in records:
                # Skip empty rows
                if not record.get('Truck Number'):
                    continue
                
                truck_data = {
                    'truck_number': str(record.get('Truck Number', '')).strip(),
                    'loconav_vehicle_id': str(record.get('LocoNav Vehicle ID', '')).strip() or None,
                    'company': str(record.get('Company', '')).strip() or None,
                    'fleet_manager': str(record.get('Fleet Manager', '')).strip() or None,
                    'status': str(record.get('Status', 'operational')).strip().lower(),
                    'brand': str(record.get('Brand', '')).strip() or None,
                    'trailer_size': str(record.get('Trailer Size', '')).strip() or None,
                    'operating_location': str(record.get('Operating Location', '')).strip() or None,
                }
                
                trucks.append(truck_data)
            
            return trucks
            
        except Exception as e:
            print(f"Error fetching data from Google Sheets: {e}")
            return []
    
    async def sync_trucks(self, db: AsyncSession) -> Dict[str, int]:
        """
        Sync truck data from Google Sheets to database
        
        This performs an upsert operation:
        - New trucks are inserted
        - Existing trucks are updated
        - Trucks not in sheet are marked as 'inactive'
        
        Args:
            db: Database session
            
        Returns:
            Dict with sync statistics
        """
        stats = {
            'fetched': 0,
            'created': 0,
            'updated': 0,
            'deactivated': 0,
            'errors': 0
        }
        
        # Fetch data from Google Sheets
        sheet_trucks = self.fetch_truck_data()
        stats['fetched'] = len(sheet_trucks)
        
        if not sheet_trucks:
            print("No truck data fetched from Google Sheets")
            return stats
        
        # Get all truck numbers from sheet
        sheet_truck_numbers = {truck['truck_number'] for truck in sheet_trucks}
        
        # Process each truck from sheet
        for truck_data in sheet_trucks:
            try:
                # Use PostgreSQL upsert
                stmt = insert(Truck).values(**truck_data)
                stmt = stmt.on_conflict_do_update(
                    index_elements=['truck_number'],
                    set_={
                        'loconav_vehicle_id': stmt.excluded.loconav_vehicle_id,
                        'company': stmt.excluded.company,
                        'fleet_manager': stmt.excluded.fleet_manager,
                        'status': stmt.excluded.status,
                        'brand': stmt.excluded.brand,
                        'trailer_size': stmt.excluded.trailer_size,
                        'operating_location': stmt.excluded.operating_location,
                    }
                )
                
                result = await db.execute(stmt)
                
                # Check if it was an insert or update
                if result.rowcount > 0:
                    # Need to check if it was insert or update
                    # For now, we'll count it as updated
                    stats['updated'] += 1
                    
            except Exception as e:
                print(f"Error syncing truck {truck_data.get('truck_number')}: {e}")
                stats['errors'] += 1
        
        # Mark trucks not in sheet as inactive
        inactive_stmt = (
            update(Truck)
            .where(~Truck.truck_number.in_(sheet_truck_numbers))
            .where(Truck.status != 'inactive')
            .values(status='inactive')
        )
        
        result = await db.execute(inactive_stmt)
        stats['deactivated'] = result.rowcount
        
        # Commit all changes
        await db.commit()
        
        print(f"Google Sheets sync completed: {stats}")
        return stats
    
    async def get_sync_status(self, db: AsyncSession) -> Dict[str, Any]:
        """
        Get current sync status and statistics
        
        Args:
            db: Database session
            
        Returns:
            Dict with sync status information
        """
        # Count trucks by source
        total_trucks = await db.execute(
            select(Truck).count()
        )
        
        trucks_with_loconav = await db.execute(
            select(Truck)
            .where(Truck.loconav_vehicle_id.isnot(None))
            .count()
        )
        
        inactive_trucks = await db.execute(
            select(Truck)
            .where(Truck.status == 'inactive')
            .count()
        )
        
        return {
            'total_trucks': total_trucks.scalar(),
            'trucks_with_loconav_id': trucks_with_loconav.scalar(),
            'inactive_trucks': inactive_trucks.scalar(),
            'spreadsheet_id': self.spreadsheet_id,
            'client_configured': self.client is not None
        }