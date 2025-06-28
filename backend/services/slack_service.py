"""
Slack notification service for Watch Tower
"""

import logging
from typing import Dict, Any, Optional
from slack_bolt.async_app import AsyncApp
from core.config import settings

logger = logging.getLogger(__name__)


class SlackService:
    """Service for sending Slack notifications"""
    
    def __init__(self):
        self.app = AsyncApp(token=settings.SLACK_BOT_TOKEN)
        self.channel = settings.SLACK_ALERTS_CHANNEL
        
    async def send_alert(self, alert_data: Dict[str, Any]) -> bool:
        """Send alert notification to Slack"""
        try:
            severity_emoji = {
                "critical": "🚨",
                "high": "⚠️", 
                "medium": "🟡",
                "low": "ℹ️"
            }
            
            emoji = severity_emoji.get(alert_data.get("severity", "low"), "ℹ️")
            truck_number = alert_data.get("truck_number", "Unknown")
            alert_type = alert_data.get("alert_type", "General")
            title = alert_data.get("title", "Fleet Alert")
            description = alert_data.get("description", "")
            
            blocks = [
                {
                    "type": "header",
                    "text": {
                        "type": "plain_text",
                        "text": f"{emoji} {title}"
                    }
                },
                {
                    "type": "section",
                    "fields": [
                        {
                            "type": "mrkdwn",
                            "text": f"*Truck:*\n{truck_number}"
                        },
                        {
                            "type": "mrkdwn", 
                            "text": f"*Alert Type:*\n{alert_type}"
                        },
                        {
                            "type": "mrkdwn",
                            "text": f"*Severity:*\n{alert_data.get('severity', 'low').title()}"
                        }
                    ]
                }
            ]
            
            if description:
                blocks.append({
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"*Details:*\n{description}"
                    }
                })
            
            # Add truck location if available
            if alert_data.get("location"):
                blocks.append({
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"*Location:*\n{alert_data['location']}"
                    }
                })
            
            await self.app.client.chat_postMessage(
                channel=self.channel,
                blocks=blocks
            )
            
            logger.info(
                f"Sent {alert_data.get('severity')} alert to Slack for truck {truck_number}",
                extra={"alert_type": alert_type}
            )
            return True
            
        except Exception as e:
            logger.error(f"Failed to send Slack alert: {e}")
            return False
    
    async def send_trip_notification(self, trip_data: Dict[str, Any], event_type: str) -> bool:
        """Send trip-related notifications"""
        try:
            truck_number = trip_data.get("truck_number", "Unknown")
            trip_id = trip_data.get("vpc_id", trip_data.get("trip_id", "Unknown"))
            
            event_emojis = {
                "started": "🚛",
                "completed": "✅", 
                "delayed": "⏰",
                "cancelled": "❌"
            }
            
            emoji = event_emojis.get(event_type, "📋")
            
            blocks = [
                {
                    "type": "header",
                    "text": {
                        "type": "plain_text",
                        "text": f"{emoji} Trip {event_type.title()}"
                    }
                },
                {
                    "type": "section",
                    "fields": [
                        {
                            "type": "mrkdwn",
                            "text": f"*Trip ID:*\n{trip_id}"
                        },
                        {
                            "type": "mrkdwn",
                            "text": f"*Truck:*\n{truck_number}"
                        }
                    ]
                }
            ]
            
            if trip_data.get("origin") and trip_data.get("destination"):
                blocks.append({
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"*Route:*\n{trip_data['origin']} → {trip_data['destination']}"
                    }
                })
            
            await self.app.client.chat_postMessage(
                channel=self.channel,
                blocks=blocks
            )
            
            logger.info(f"Sent trip {event_type} notification for {trip_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send trip notification: {e}")
            return False
    
    async def send_daily_summary(self, summary_data: Dict[str, Any]) -> bool:
        """Send daily fleet summary"""
        try:
            date = summary_data.get("date", "Today")
            active_trucks = summary_data.get("active_trucks", 0)
            completed_trips = summary_data.get("completed_trips", 0)
            total_distance = summary_data.get("total_distance_km", 0)
            
            blocks = [
                {
                    "type": "header",
                    "text": {
                        "type": "plain_text",
                        "text": f"📊 Daily Fleet Summary - {date}"
                    }
                },
                {
                    "type": "section",
                    "fields": [
                        {
                            "type": "mrkdwn",
                            "text": f"*Active Trucks:*\n{active_trucks}"
                        },
                        {
                            "type": "mrkdwn",
                            "text": f"*Completed Trips:*\n{completed_trips}"
                        },
                        {
                            "type": "mrkdwn",
                            "text": f"*Total Distance:*\n{total_distance:.1f} km"
                        }
                    ]
                }
            ]
            
            if summary_data.get("alerts_count", 0) > 0:
                blocks.append({
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"*Alerts Today:* {summary_data['alerts_count']}"
                    }
                })
            
            await self.app.client.chat_postMessage(
                channel=self.channel,
                blocks=blocks
            )
            
            logger.info(f"Sent daily summary for {date}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send daily summary: {e}")
            return False


# Global instance
slack_service = SlackService()