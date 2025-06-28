#!/usr/bin/env python3
"""
Test script to check if Responses API is available in upgraded OpenAI SDK
"""

import asyncio
import os
import sys
from pathlib import Path

# Add backend to path
backend_path = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_path))

async def test_responses_api_availability():
    """Test if Responses API is available"""
    try:
        print("🔍 Testing Responses API Availability")
        print("=" * 45)
        
        from openai import AsyncOpenAI
        import openai
        
        print(f"✅ OpenAI SDK Version: {openai.__version__}")
        
        client = AsyncOpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        
        # Check if responses attribute exists
        if hasattr(client, 'responses'):
            print("✅ client.responses attribute found")
            
            # Try a simple call
            print("\n📞 Testing Simple Responses API Call")
            try:
                response = await client.responses.create(
                    model="gpt-4o-mini",
                    input="Hello, respond with 'Responses API working'"
                )
                
                print(f"✅ Response ID: {response.id}")
                
                if hasattr(response, 'output_text'):
                    print(f"✅ Output text: {response.output_text}")
                elif hasattr(response, 'output'):
                    print(f"✅ Output: {response.output}")
                else:
                    print(f"⚠️ Response format: {dir(response)}")
                
                return True
                
            except Exception as e:
                print(f"❌ Responses API call failed: {e}")
                print(f"Error type: {type(e)}")
                return False
                
        else:
            print("❌ client.responses attribute not found")
            print(f"Available attributes: {[attr for attr in dir(client) if not attr.startswith('_')]}")
            return False
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

async def test_function_calling_format():
    """Test function calling format with new SDK"""
    try:
        print("\n🔧 Testing Function Calling Format")
        print("=" * 40)
        
        from openai import AsyncOpenAI
        
        client = AsyncOpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        
        # Test with Chat Completions first
        print("📞 Testing Chat Completions function calling")
        
        tools = [{
            "type": "function",
            "function": {
                "name": "test_function",
                "description": "A test function",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "message": {"type": "string"}
                    },
                    "required": ["message"]
                }
            }
        }]
        
        response = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": "Call the test function with message 'hello'"}
            ],
            tools=tools,
            tool_choice="auto"
        )
        
        message = response.choices[0].message
        if message.tool_calls:
            print(f"✅ Function call detected: {message.tool_calls[0].function.name}")
            print(f"✅ Arguments: {message.tool_calls[0].function.arguments}")
        else:
            print("⚠️ No function call made")
        
        return True
        
    except Exception as e:
        print(f"❌ Function calling test failed: {e}")
        return False

async def main():
    """Run all tests"""
    print("🚀 Testing Upgraded OpenAI SDK")
    print("=" * 50)
    
    if not os.getenv('OPENAI_API_KEY'):
        print("❌ OPENAI_API_KEY not found")
        return False
    
    tests = [
        ("Responses API Availability", test_responses_api_availability),
        ("Function Calling Format", test_function_calling_format),
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n{'='*5} {test_name} {'='*5}")
        result = await test_func()
        results.append((test_name, result))
    
    # Summary
    print("\n" + "="*50)
    print("📊 TEST SUMMARY")
    print("="*50)
    
    for test_name, passed in results:
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{test_name}: {status}")
    
    all_passed = all(result for _, result in results)
    print(f"\nOverall: {'✅ ALL TESTS PASSED' if all_passed else '❌ SOME TESTS FAILED'}")
    
    return all_passed

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)