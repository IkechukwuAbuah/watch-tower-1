#!/usr/bin/env python3
"""
Test .env file loading to ensure proper configuration
"""

import os
from dotenv import load_dotenv

def test_env_loading():
    print("🔧 TESTING .ENV FILE LOADING")
    print("=" * 50)
    
    # Load from root directory
    load_dotenv()
    
    print("\n1. 🔑 LOCONAV VARIABLES:")
    loconav_vars = {k: v for k, v in os.environ.items() if 'LOCONAV' in k}
    for key, value in loconav_vars.items():
        print(f"   {key} = {value}")
    
    print("\n2. 🤖 OPENAI VARIABLES:")
    openai_vars = {k: v for k, v in os.environ.items() if 'OPENAI' in k}
    for key, value in openai_vars.items():
        print(f"   {key} = {value}")
    
    print("\n3. 💬 SLACK VARIABLES:")
    slack_vars = {k: v for k, v in os.environ.items() if 'SLACK' in k}
    for key, value in slack_vars.items():
        print(f"   {key} = {value[:20]}..." if len(value) > 20 else f"   {key} = {value}")
    
    print("\n4. ✅ VALIDATION:")
    
    # Check for real LocoNav token
    loconav_token = os.getenv("LOCONAV_USER_TOKEN")
    if loconav_token and loconav_token != "your_loconav_auth_token_here":
        print("   ✅ LocoNav token: REAL")
    else:
        print("   ❌ LocoNav token: PLACEHOLDER")
    
    # Check for OpenAI key
    openai_key = os.getenv("OPENAI_API_KEY")
    if openai_key and openai_key != "sk-your_openai_api_key_here":
        print("   ✅ OpenAI key: CONFIGURED")
    else:
        print("   ❌ OpenAI key: PLACEHOLDER")
    
    # Check for Slack token
    slack_token = os.getenv("SLACK_BOT_TOKEN")
    if slack_token and slack_token.startswith("xoxb-") and len(slack_token) > 20:
        print("   ✅ Slack token: CONFIGURED")
    else:
        print("   ❌ Slack token: MISSING")

if __name__ == "__main__":
    test_env_loading()