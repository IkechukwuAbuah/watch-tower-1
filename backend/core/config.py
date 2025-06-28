"""
Configuration settings for Watch Tower
"""

from pydantic_settings import BaseSettings
from typing import Optional
import os


class Settings(BaseSettings):
    # App
    app_name: str = "Watch Tower"
    environment: str = "development"
    debug: bool = True
    
    # Database
    database_url: str
    database_pool_size: int = 20
    database_max_overflow: int = 40
    
    # Redis
    redis_url: str = "redis://localhost:6379/0"
    redis_pool_size: int = 10
    redis_decode_responses: bool = False  # Keep False for binary data
    redis_socket_timeout: int = 5
    redis_socket_connect_timeout: int = 5
    
    # Event Streaming
    event_stream_prefix: str = "watch_tower:events"
    event_consumer_group: str = "watch_tower_consumers"
    event_batch_size: int = 100
    event_block_ms: int = 1000  # How long to block waiting for events
    
    # LocoNav - CORRECTED IMPLEMENTATION
    loconav_user_token: Optional[str] = None
    loconav_base_url: str = "https://api.a.loconav.com"
    loconav_timeout: int = 30
    
    # Google Sheets
    google_sheets_credentials_json: Optional[str] = None
    google_sheets_master_spreadsheet_id: Optional[str] = None
    
    # OpenAI
    openai_api_key: Optional[str] = None
    openai_model: str = "gpt-4o-mini"
    openai_temperature: float = 0.7
    openai_max_tokens: int = 2000
    
    # Slack
    slack_bot_token: Optional[str] = None
    slack_app_token: Optional[str] = None
    slack_signing_secret: Optional[str] = None
    slack_alerts_channel: str = "#fleet-alerts"
    
    # Celery
    celery_broker_url: str = "redis://localhost:6379/1"
    celery_result_backend: str = "redis://localhost:6379/2"
    celery_timezone: str = "Africa/Lagos"
    
    # Security
    secret_key: str = "your-secret-key-change-this"
    api_key_header: str = "X-API-Key"
    
    # Lagos specifics
    lagos_timezone: str = "Africa/Lagos"
    lagos_lat: float = 6.5244
    lagos_lng: float = 3.3792
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Create global settings instance
settings = Settings()