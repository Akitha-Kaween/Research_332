from loguru import logger

class RedisClient:
    def __init__(self):
        self.redis = None
        self.enabled = False
    
    async def connect(self):
        """Connect to Redis (optional for testing)"""
        try:
            import redis.asyncio as redis
            from app.config.settings import settings
            self.redis = await redis.from_url(
                settings.REDIS_URL,
                encoding="utf-8",
                decode_responses=True
            )
            self.enabled = True
            logger.info("Redis connected successfully")
            return self.redis
        except Exception as e:
            logger.warning(f"Redis not available: {str(e)}. Caching disabled.")
            self.enabled = False
            return None
    
    async def disconnect(self):
        """Disconnect from Redis"""
        if self.redis:
            await self.redis.close()
            logger.info("Redis disconnected")
    
    async def get(self, key: str):
        """Get value from Redis"""
        if not self.enabled:
            return None
        try:
            if not self.redis:
                await self.connect()
            return await self.redis.get(key) if self.redis else None
        except:
            return None
    
    async def set(self, key: str, value: str, ex: int = None):
        """Set value in Redis with optional expiration"""
        if not self.enabled:
            return None
        try:
            if not self.redis:
                await self.connect()
            return await self.redis.set(key, value, ex=ex) if self.redis else None
        except:
            return None
    
    async def setex(self, key: str, seconds: int, value: str):
        """Set value with expiration time"""
        if not self.enabled:
            return None
        try:
            if not self.redis:
                await self.connect()
            return await self.redis.setex(key, seconds, value) if self.redis else None
        except:
            return None
    
    async def delete(self, key: str):
        """Delete key from Redis"""
        if not self.enabled:
            return None
        try:
            if not self.redis:
                await self.connect()
            return await self.redis.delete(key) if self.redis else None
        except:
            return None

redis_client = RedisClient()

