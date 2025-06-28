#!/usr/bin/env python3
"""
Test script for AI service implementation
Tests the secure Responses API integration
"""

import asyncio
import os
import sys
from pathlib import Path

# Add backend to path
backend_path = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_path))

async def test_ai_service():
    """Test AI service with simple queries"""
    try:
        from services.ai_service import ai_service
        
        print("🤖 Testing AI Service with OpenAI Responses API")
        print("=" * 50)
        
        # Test 1: Simple text query (no function calls)
        print("\n📝 Test 1: Simple Query")
        result = await ai_service.process_natural_language_query(
            "What is Watch Tower?",
            {"test": True}
        )
        print(f"Status: {result['status']}")
        print(f"Response: {result['response'][:200]}...")
        print(f"Function calls: {len(result.get('function_calls', []))}")
        
        # Test 2: Fleet status query (should trigger function call)
        print("\n🚛 Test 2: Fleet Status Query") 
        result = await ai_service.process_natural_language_query(
            "Show me the fleet status",
            {"test": True}
        )
        print(f"Status: {result['status']}")
        print(f"Response: {result['response'][:200]}...")
        print(f"Function calls: {len(result.get('function_calls', []))}")
        
        # Test 3: Truck location query
        print("\n📍 Test 3: Truck Location Query")
        result = await ai_service.process_natural_language_query(
            "Where is truck T11985LA?",
            {"test": True}
        )
        print(f"Status: {result['status']}")
        print(f"Response: {result['response'][:200]}...")
        print(f"Function calls: {len(result.get('function_calls', []))}")
        
        print("\n✅ AI Service tests completed successfully!")
        return True
        
    except Exception as e:
        print(f"\n❌ AI Service test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

async def test_function_registry():
    """Test function registry functionality"""
    try:
        from services.ai_service import ai_service
        
        print("\n🔧 Testing Function Registry")
        print("=" * 30)
        
        # Check registered functions
        functions = list(ai_service.function_registry.keys())
        print(f"Registered functions: {functions}")
        
        # Test individual function (if available)
        if 'get_fleet_status' in ai_service.function_registry:
            print("\n🧪 Testing get_fleet_status function directly")
            result = await ai_service.function_registry['get_fleet_status']()
            print(f"Function result type: {type(result)}")
            print(f"Result keys: {list(result.keys()) if isinstance(result, dict) else 'Not a dict'}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Function registry test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    """Run all tests"""
    print("🚀 Starting AI Service Tests")
    print("=" * 60)
    
    # Check environment
    if not os.getenv('OPENAI_API_KEY'):
        print("❌ OPENAI_API_KEY not found in environment")
        return False
    
    print(f"✅ OpenAI API Key: {os.getenv('OPENAI_API_KEY')[:10]}...")
    
    # Run tests
    tests = [
        ("Function Registry", test_function_registry),
        ("AI Service", test_ai_service),
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        result = await test_func()
        results.append((test_name, result))
    
    # Summary
    print("\n" + "="*60)
    print("📊 TEST SUMMARY")
    print("="*60)
    
    for test_name, passed in results:
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{test_name}: {status}")
    
    all_passed = all(result for _, result in results)
    print(f"\nOverall: {'✅ ALL TESTS PASSED' if all_passed else '❌ SOME TESTS FAILED'}")
    
    return all_passed

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)