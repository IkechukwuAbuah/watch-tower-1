#!/usr/bin/env python3
"""
Test LocoNav API connection
Run: python scripts/test_loconav.py
"""

import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.services.loconav_service import LocoNavService
from dotenv import load_dotenv

async def main():
    # Load environment variables
    load_dotenv()
    
    print("🔍 Testing LocoNav API connection...")
    
    try:
        service = LocoNavService()
        
        # Test connection
        connected = await service.test_connection()
        if connected:
            print("✅ Successfully connected to LocoNav API!")
        else:
            print("❌ Failed to connect to LocoNav API")
            return
            
        # Test getting user info
        print("\n📋 Testing user endpoint...")
        # Add more tests here
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
