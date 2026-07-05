import time
from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import Message
from bot.config import settings
from bot.database.connection import async_session
from bot.database.crud import get_or_create_group, create_audit_log, update_group_setting
import redis.asyncio as aioredis
import logging

class AntiFloodMiddleware(BaseMiddleware):
    def __init__(self, limit_seconds: float = 1.5):
        self.limit = limit_seconds
        self.redis: aioredis.Redis | None = None
        self.local_cache: Dict[str, float] = {}
        
        # Try establishing connection to Redis if configured
        if settings.REDIS_URL:
            try:
                self.redis = aioredis.from_url(settings.REDIS_URL)
            except Exception as e:
                logging.error(f"Failed to connect to Redis for AntiFlood: {e}. Falling back to memory storage.")

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        # Ignore private chats and channel posts
        if not event.chat or event.chat.type == "private":
            return await handler(event, data)
            
        chat_id = event.chat.id
        user_id = event.from_user.id
        
        # Check if anti-flood is enabled for this group (pre-fetched or lazy loaded)
        db_session = data.get("db_session")
        if db_session:
            group = await get_or_create_group(db_session, chat_id, event.chat.title)
            if not group.anti_flood:
                return await handler(event, data)
        else:
            # Safe fallback if session is missing
            group = None

        key = f"flood:{chat_id}:{user_id}"
        current_time = time.time()
        
        # 1. Use Redis rate limiting if available
        if self.redis:
            try:
                last_time_str = await self.redis.get(key)
                if last_time_str:
                    last_time = float(last_time_str)
                    if current_time - last_time < self.limit:
                        # User is flooding. Delete message and restrict if threshold is crossed.
                        trigger_key = f"flood_trig:{chat_id}:{user_id}"
                        triggers = await self.redis.incr(trigger_key)
                        await self.redis.expire(trigger_key, 10)
                        
                        try:
                            await event.delete()
                        except Exception:
                            pass
                            
                        if triggers >= 4: # Severe spam trigger
                            # Restrict user
                            await event.chat.mute(user_id, until_date=int(time.time() + 3600))
                            if db_session:
                                await create_audit_log(
                                    db_session, chat_id, None, user_id, 
                                    "mute", 3600, "Anti-Flood automatic lock (Severe Spam)"
                                )
                            return
                        return # Silence message handling
                await self.redis.set(key, str(current_time), ex=int(self.limit) + 1)
            except Exception as e:
                logging.error(f"Redis operation failed during antiflood: {e}")
                
        # 2. Local memory fallback
        else:
            last_time = self.local_cache.get(key, 0.0)
            if current_time - last_time < self.limit:
                try:
                    await event.delete()
                except Exception:
                    pass
                return # Block execution
            self.local_cache[key] = current_time
            # Keep cache clean
            if len(self.local_cache) > 10000:
                self.local_cache.clear()
                
        return await handler(event, data)
