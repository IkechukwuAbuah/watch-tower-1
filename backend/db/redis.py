"""
Redis connection management for Watch Tower
"""

import redis.asyncio as redis
from redis.asyncio import ConnectionPool
from typing import Optional
import logging
from core.config import settings

logger = logging.getLogger(__name__)

# Global connection pool
_redis_pool: Optional[ConnectionPool] = None


async def get_redis_pool() -> ConnectionPool:
    """Get or create Redis connection pool"""
    global _redis_pool
    
    if _redis_pool is None:
        _redis_pool = redis.ConnectionPool.from_url(
            settings.redis_url,
            max_connections=settings.redis_pool_size,
            decode_responses=settings.redis_decode_responses,
            socket_timeout=settings.redis_socket_timeout,
            socket_connect_timeout=settings.redis_socket_connect_timeout,
        )
        logger.info(f"Created Redis connection pool with {settings.redis_pool_size} connections")
    
    return _redis_pool


async def get_redis_client() -> redis.Redis:
    """Get Redis client instance"""
    pool = await get_redis_pool()
    return redis.Redis(connection_pool=pool)


async def close_redis_pool():
    """Close Redis connection pool"""
    global _redis_pool
    
    if _redis_pool:
        await _redis_pool.disconnect()
        _redis_pool = None
        logger.info("Closed Redis connection pool")


async def health_check() -> bool:
    """Check Redis connectivity"""
    try:
        client = await get_redis_client()
        await client.ping()
        return True
    except Exception as e:
        logger.error(f"Redis health check failed: {e}")
        return False