#!/usr/bin/env python3
"""
Simple LocoNav API validation test
Tests credentials and basic connectivity without complex imports
"""

import asyncio
import httpx
import os
from dotenv import load_dotenv

async def test_loconav_simple():
    print("🔍 SIMPLE LOCONAV API TEST")
    print("=" * 40)
    
    # Load environment variables from correct path
    load_dotenv(dotenv_path=".env")
    
    # DEBUG: Check all env vars
    print(f"   All LOCONAV env vars:")
    for key, value in os.environ.items():
        if "LOCONAV" in key:
            print(f"     {key}={value}")
    
    # Get credentials - CORRECTED (force real token for test)
    user_token = "PRJX5q4K5Yhn7FFWfuTx"
    base_url = "https://api.a.loconav.com"
    
    print(f"\n1. 🔑 CHECKING CREDENTIALS")
    print(f"   User Token: {user_token}")
    print(f"   Base URL: {base_url}")
    
    if not user_token:
        print("❌ LOCONAV_USER_TOKEN not configured")
        print("📋 ACTION: Set LOCONAV_USER_TOKEN in .env")
        return "CREDENTIALS_MISSING"
    
    # Test basic API connectivity
    print(f"\n2. 🌐 TESTING API CONNECTION")
    
    headers = {
        "User-Authentication": user_token,
        "Content-Type": "application/json"
    }
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            # Try a simple endpoint - user info or health check
            test_url = f"{base_url}/integration/api/v1/user"
            print(f"   Testing: {test_url}")
            
            response = await client.get(test_url, headers=headers)
            print(f"   Status Code: {response.status_code}")
            
            if response.status_code == 200:
                print("✅ Successfully connected to LocoNav API!")
                data = response.json()
                print(f"   Response data keys: {list(data.keys()) if isinstance(data, dict) else 'Not a dict'}")
                return "CONNECTION_SUCCESS"
                
            elif response.status_code == 401:
                print("❌ Authentication failed - Invalid API key")
                print("📋 ACTION: Check LocoNav API key is correct")
                return "AUTH_FAILED"
                
            elif response.status_code == 404:
                print("⚠️ Endpoint not found - trying alternative...")
                # Try vehicles endpoint
                alt_url = f"{base_url}/integration/api/v1/vehicles"
                print(f"   Testing alternative: {alt_url}")
                
                alt_response = await client.get(alt_url, headers=headers)
                print(f"   Alt Status Code: {alt_response.status_code}")
                
                if alt_response.status_code == 200:
                    print("✅ Connected via vehicles endpoint!")
                    return "CONNECTION_SUCCESS"
                else:
                    print("❌ Both endpoints failed")
                    return "ENDPOINT_NOT_FOUND"
            else:
                print(f"❌ Unexpected status code: {response.status_code}")
                print(f"   Response: {response.text}")
                return "UNEXPECTED_ERROR"
                
    except httpx.TimeoutException:
        print("❌ Request timed out - Check network connectivity")
        return "TIMEOUT"
    except Exception as e:
        print(f"❌ Connection error: {e}")
        return "CONNECTION_ERROR"

async def test_vehicles_list():
    """Test getting vehicles list if connection works"""
    print(f"\n3. 🚛 TESTING VEHICLES ENDPOINT")
    
    # Force real token for test
    user_token = "PRJX5q4K5Yhn7FFWfuTx"
    base_url = "https://api.a.loconav.com"
    
    if not user_token:
        return
    
    headers = {
        "User-Authentication": user_token,
        "Content-Type": "application/json"
    }
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            # Try vehicles list with pagination
            vehicles_url = f"{base_url}/integration/api/v1/vehicles"
            params = {"page": 1, "perPage": 5}
            
            print(f"   Testing: {vehicles_url}")
            response = await client.get(vehicles_url, headers=headers, params=params)
            print(f"   Status Code: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print("✅ Successfully retrieved vehicles data!")
                
                if isinstance(data, dict) and 'values' in data:
                    vehicles = data['values']
                    print(f"   Found {len(vehicles)} vehicles")
                    
                    if vehicles:
                        sample = vehicles[0]
                        print(f"   Sample vehicle keys: {list(sample.keys())}")
                        print(f"   Sample vehicle ID: {sample.get('id', 'N/A')}")
                        
                        return "VEHICLES_SUCCESS"
                else:
                    print(f"   Unexpected data format: {type(data)}")
                    return "VEHICLES_UNEXPECTED_FORMAT"
            else:
                print(f"❌ Failed to get vehicles: {response.status_code}")
                print(f"   Response: {response.text}")
                return "VEHICLES_FAILED"
                
    except Exception as e:
        print(f"❌ Error getting vehicles: {e}")
        return "VEHICLES_ERROR"

async def main():
    print("🎯 STARTING SIMPLE LOCONAV TEST")
    print("This validates basic LocoNav API connectivity\n")
    
    connection_result = await test_loconav_simple()
    
    if connection_result == "CONNECTION_SUCCESS":
        vehicles_result = await test_vehicles_list()
    
    print("\n" + "=" * 40)
    print("🎯 TEST SUMMARY")
    
    if connection_result == "CREDENTIALS_MISSING":
        print("❌ RESULT: No LocoNav credentials configured")
        print("📋 NEXT: Get real API credentials from VPC team")
        
    elif connection_result == "CONNECTION_SUCCESS":
        print("✅ RESULT: LocoNav API connection WORKS!")
        print("🎯 IMPACT: Real truck data is available!")
        print("📋 NEXT: Fix AI service to query this data")
        
    elif connection_result == "AUTH_FAILED":
        print("❌ RESULT: Authentication failed")
        print("📋 NEXT: Verify API key with LocoNav team")
        
    else:
        print(f"❌ RESULT: Connection failed ({connection_result})")
        print("📋 NEXT: Debug network/API issues")

if __name__ == "__main__":
    asyncio.run(main())