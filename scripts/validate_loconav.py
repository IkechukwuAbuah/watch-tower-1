#!/usr/bin/env python3
"""
Comprehensive LocoNav API validation test
Tests actual connectivity, authentication, and data retrieval
Run: python scripts/validate_loconav.py
"""

import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import directly to avoid broken services.__init__.py
import importlib.util
spec = importlib.util.spec_from_file_location("loconav_service", "backend/services/loconav_service.py")
loconav_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(loconav_module)
LocoNavAPIService = loconav_module.LocoNavAPIService

from backend.core.config import settings
from dotenv import load_dotenv

async def validate_loconav():
    print("🔍 LOCONAV VALIDATION TEST")
    print("=" * 50)
    
    # Load environment variables
    load_dotenv()
    
    # Check if credentials are configured
    print("\n1. 🔑 CHECKING CREDENTIALS...")
    
    if not settings.loconav_api_key or settings.loconav_api_key == "your_loconav_api_key_here":
        print("❌ LOCONAV_API_KEY not configured or still placeholder")
        print("   Current value:", settings.loconav_api_key)
        return "CREDENTIALS_MISSING"
    
    if not settings.loconav_api_secret or settings.loconav_api_secret == "your_loconav_api_secret_here":
        print("❌ LOCONAV_API_SECRET not configured or still placeholder")
        return "CREDENTIALS_MISSING"
    
    print("✅ Credentials appear to be configured")
    print(f"   API Key: {settings.loconav_api_key[:10]}..." if settings.loconav_api_key else "None")
    print(f"   Base URL: {settings.loconav_base_url}")
    
    # Test service instantiation
    print("\n2. 🏗️ TESTING SERVICE INSTANTIATION...")
    try:
        service = LocoNavAPIService()
        print("✅ LocoNavAPIService instantiated successfully")
    except Exception as e:
        print(f"❌ Failed to instantiate LocoNavAPIService: {e}")
        return "INSTANTIATION_FAILED"
    
    # Test API connection
    print("\n3. 🌐 TESTING API CONNECTION...")
    try:
        connected = await service.test_connection()
        if connected:
            print("✅ Successfully connected to LocoNav API!")
        else:
            print("❌ Connection test returned False")
            return "CONNECTION_FAILED"
    except Exception as e:
        print(f"❌ Connection test threw exception: {e}")
        return "CONNECTION_ERROR"
    
    # Test vehicle data retrieval
    print("\n4. 🚛 TESTING VEHICLE DATA RETRIEVAL...")
    try:
        vehicles = await service.get_vehicles_list(limit=5)
        if vehicles and len(vehicles) > 0:
            print(f"✅ Successfully retrieved {len(vehicles)} vehicles")
            
            # Show sample vehicle data
            sample_vehicle = vehicles[0]
            print(f"   Sample vehicle ID: {sample_vehicle.get('id', 'N/A')}")
            print(f"   Vehicle name: {sample_vehicle.get('name', 'N/A')}")
            print(f"   Registration: {sample_vehicle.get('registration_number', 'N/A')}")
            
            return "SUCCESS"
        else:
            print("⚠️ Connected but no vehicles found")
            print("   This might indicate:")
            print("   - No vehicles in LocoNav account")
            print("   - API permissions issue")
            print("   - Wrong account/credentials")
            return "NO_VEHICLES"
            
    except Exception as e:
        print(f"❌ Failed to retrieve vehicles: {e}")
        return "VEHICLE_RETRIEVAL_FAILED"

async def test_specific_vehicle_location():
    """Test getting location for a specific vehicle if vehicles exist"""
    print("\n5. 📍 TESTING SPECIFIC VEHICLE LOCATION...")
    
    try:
        service = LocoNavAPIService()
        vehicles = await service.get_vehicles_list(limit=1)
        
        if not vehicles:
            print("⚠️ No vehicles available to test location")
            return
            
        test_vehicle = vehicles[0]
        vehicle_id = test_vehicle.get('id')
        
        if not vehicle_id:
            print("⚠️ Vehicle has no ID field")
            return
            
        print(f"   Testing location for vehicle: {vehicle_id}")
        location = await service.get_vehicle_location(vehicle_id)
        
        if location:
            print("✅ Successfully retrieved vehicle location!")
            print(f"   Latitude: {location.get('latitude', 'N/A')}")
            print(f"   Longitude: {location.get('longitude', 'N/A')}")
            print(f"   Last updated: {location.get('timestamp', 'N/A')}")
        else:
            print("⚠️ No location data returned")
            
    except Exception as e:
        print(f"❌ Failed to get vehicle location: {e}")

async def main():
    print("🎯 STARTING LOCONAV VALIDATION")
    print("This test will determine if LocoNav integration actually works\n")
    
    result = await validate_loconav()
    
    if result == "SUCCESS":
        await test_specific_vehicle_location()
    
    print("\n" + "=" * 50)
    print("🎯 VALIDATION SUMMARY")
    
    if result == "CREDENTIALS_MISSING":
        print("❌ RESULT: LocoNav credentials not configured")
        print("📋 ACTION NEEDED:")
        print("   1. Get real LocoNav API credentials from VPC")
        print("   2. Update .env file with real values")
        print("   3. Re-run this test")
        
    elif result == "SUCCESS":
        print("✅ RESULT: LocoNav integration is WORKING!")
        print("🎯 NEXT STEPS:")
        print("   1. Test API endpoints that use LocoNav data")
        print("   2. Fix AI service to query this working data")
        print("   3. Natural language queries will be powerful!")
        
    else:
        print(f"❌ RESULT: LocoNav integration is BROKEN ({result})")
        print("📋 ACTION NEEDED:")
        print("   1. Check credentials and permissions")
        print("   2. Verify LocoNav account has vehicles")
        print("   3. Debug API connection issues")
        print("   4. Fix LocoNav service before proceeding")

if __name__ == "__main__":
    asyncio.run(main())