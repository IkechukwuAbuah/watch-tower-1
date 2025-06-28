#!/usr/bin/env python3
"""
Test Slack notifications for Watch Tower
"""

import asyncio
import os
import sys
from datetime import datetime

# Add backend to path
sys.path.append('/Users/x/Downloads/watch-tower-experiments/watch-tower-1/backend')

async def test_slack_notifications():
    """Test different types of Slack notifications"""
    
    # Set minimal env vars
    os.environ['DATABASE_URL'] = 'postgresql://localhost/test'
    
    try:
        from services.slack_service import SlackService
        from core.config import settings
        
        print("🧪 Testing Slack Integration...")
        print(f"Bot Token configured: {'Yes' if settings.slack_bot_token else 'No'}")
        print(f"Alert Channel: {settings.slack_alerts_channel}")
        
        if not settings.slack_bot_token or settings.slack_bot_token == "xoxb-your-bot-token":
            print("❌ Please configure SLACK_BOT_TOKEN in your .env file")
            return
        
        slack_service = SlackService()
        
        # Test 1: Basic Alert
        print("\n📢 Test 1: Sending basic fleet alert...")
        alert_result = await slack_service.send_alert({
            "severity": "medium",
            "title": "Test Fleet Alert",
            "alert_type": "connectivity",
            "description": "This is a test alert from Watch Tower",
            "truck_number": "T12345LA",
            "location": "Lagos Island"
        })
        
        if alert_result:
            print("✅ Alert sent successfully!")
        else:
            print("❌ Alert failed to send")
        
        # Test 2: Trip Notification
        print("\n🚛 Test 2: Sending trip notification...")
        trip_result = await slack_service.send_trip_notification({
            "trip_id": "VPC20241228T001",
            "truck_number": "T28737LA",
            "origin": "ESSLIBRA Terminal",
            "destination": "ECLAT Terminal"
        }, "started")
        
        if trip_result:
            print("✅ Trip notification sent successfully!")
        else:
            print("❌ Trip notification failed to send")
        
        # Test 3: Daily Summary
        print("\n📊 Test 3: Sending daily summary...")
        summary_result = await slack_service.send_daily_summary({
            "date": datetime.now().strftime("%Y-%m-%d"),
            "active_trucks": 42,
            "completed_trips": 18,
            "total_distance_km": 1247.8,
            "alerts_count": 3
        })
        
        if summary_result:
            print("✅ Daily summary sent successfully!")
        else:
            print("❌ Daily summary failed to send")
        
        print("\n🎉 Slack testing completed!")
        print(f"Check your #{settings.slack_alerts_channel.replace('#', '')} channel for messages")
        
    except Exception as e:
        print(f"❌ Error testing Slack: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_slack_notifications())