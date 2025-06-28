#!/usr/bin/env python3
"""
Simple Slack notification test
"""

import asyncio
import os
from slack_bolt.async_app import AsyncApp
from dotenv import load_dotenv

# Load environment variables - force reload
load_dotenv(override=True)
# Try loading from specific path too
load_dotenv(".env", override=True)

async def test_slack_basic():
    """Test basic Slack functionality"""
    
    slack_token = os.getenv("SLACK_BOT_TOKEN")
    slack_channel = os.getenv("SLACK_ALERTS_CHANNEL", "#fleet-alerts")
    
    print("🧪 Testing Watch Tower Slack Integration...")
    print(f"Bot Token: {slack_token[:20]}... (hidden)" if slack_token else "❌ No token")
    print(f"Channel: {slack_channel}")
    print(f"Debug - Full token: {slack_token}")
    
    if not slack_token or "your-bot-token" in slack_token or len(slack_token) < 20:
        print("❌ Please configure SLACK_BOT_TOKEN in your .env file")
        return
    
    try:
        # Create Slack app
        app = AsyncApp(token=slack_token)
        
        # Test 1: Basic message
        print("\n📢 Test 1: Sending basic message...")
        response1 = await app.client.chat_postMessage(
            channel=slack_channel,
            text="🚛 Watch Tower Bot is now online! Fleet monitoring system ready."
        )
        
        if response1["ok"]:
            print("✅ Basic message sent successfully!")
        else:
            print(f"❌ Basic message failed: {response1}")
        
        # Test 2: Rich formatted alert
        print("\n🚨 Test 2: Sending formatted fleet alert...")
        blocks = [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": "🚨 Fleet Alert - Test"
                }
            },
            {
                "type": "section",
                "fields": [
                    {
                        "type": "mrkdwn",
                        "text": "*Truck:*\nT12345LA"
                    },
                    {
                        "type": "mrkdwn",
                        "text": "*Alert Type:*\nConnectivity Test"
                    },
                    {
                        "type": "mrkdwn",
                        "text": "*Severity:*\nMedium"
                    },
                    {
                        "type": "mrkdwn",
                        "text": "*Location:*\nLagos Island"
                    }
                ]
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "*Details:*\nThis is a test alert from Watch Tower fleet management system."
                }
            }
        ]
        
        response2 = await app.client.chat_postMessage(
            channel=slack_channel,
            blocks=blocks
        )
        
        if response2["ok"]:
            print("✅ Formatted alert sent successfully!")
        else:
            print(f"❌ Formatted alert failed: {response2}")
        
        # Test 3: Trip notification
        print("\n🚛 Test 3: Sending trip notification...")
        trip_blocks = [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": "🚛 Trip Started"
                }
            },
            {
                "type": "section",
                "fields": [
                    {
                        "type": "mrkdwn",
                        "text": "*Trip ID:*\nVPC20241228T001"
                    },
                    {
                        "type": "mrkdwn",
                        "text": "*Truck:*\nT28737LA"
                    }
                ]
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "*Route:*\nESSLIBRA Terminal → ECLAT Terminal"
                }
            }
        ]
        
        response3 = await app.client.chat_postMessage(
            channel=slack_channel,
            blocks=trip_blocks
        )
        
        if response3["ok"]:
            print("✅ Trip notification sent successfully!")
        else:
            print(f"❌ Trip notification failed: {response3}")
        
        print("\n🎉 Slack testing completed!")
        print(f"Check your {slack_channel} channel for the test messages")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_slack_basic())