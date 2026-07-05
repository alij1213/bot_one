export interface ProjectFile {
  name: string;
  path: string;
  language: string;
  code: string;
}

export const PROJECT_FILES: ProjectFile[] = [
  {
    name: "main.py",
    path: "bot/main.py",
    language: "python",
    code: `import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.redis import RedisStorage

from bot.config import settings
from bot.database.connection import init_db
from bot.middlewares.auth import AuthAndDatabaseMiddleware
from bot.middlewares.antiflood import AntiFloodMiddleware
from bot.middlewares.i18n import InternationalizationMiddleware

# Import Routers
from bot.handlers.start import router as start_router
from bot.handlers.admin import router as admin_router
from bot.handlers.moderation import router as moderation_router
from bot.handlers.backup import router as backup_router
from bot.handlers.stats import router as stats_router

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("telegram_group_bot")

async def main():
    await init_db()
    
    storage = RedisStorage.from_url(settings.REDIS_URL) if settings.REDIS_URL else MemoryStorage()
    bot = Bot(token=settings.BOT_TOKEN)
    dp = Dispatcher(storage=storage)

    # Middlewares
    dp.update.outer_middleware(AuthAndDatabaseMiddleware())
    dp.message.middleware(AntiFloodMiddleware())
    dp.update.middleware(InternationalizationMiddleware())

    # Routers
    dp.include_router(start_router)
    dp.include_router(admin_router)
    dp.include_router(moderation_router)
    dp.include_router(backup_router)
    dp.include_router(stats_router)

    logger.info("Bot starting...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())`
  },
  {
    name: "models.py",
    path: "bot/database/models.py",
    language: "python",
    code: `from sqlalchemy import Column, String, BigInteger, Integer, Boolean, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from bot.database.connection import Base

class GroupSettings(Base):
    __tablename__ = "group_settings"

    chat_id = Column(BigInteger, primary_key=True)
    title = Column(String(255))
    language = Column(String(10), default="en")
    
    # Anti-toggles
    anti_spam = Column(Boolean, default=True)
    anti_flood = Column(Boolean, default=True)
    anti_raid = Column(Boolean, default=False)
    anti_bot = Column(Boolean, default=True)
    anti_link = Column(Boolean, default=True)
    anti_forward = Column(Boolean, default=False)
    
    # Verification
    verification_required = Column(Boolean, default=True)
    welcome_message = Column(Text, default="Welcome {user}!")
    welcome_enabled = Column(Boolean, default=True)
    
    # Locks
    lock_text = Column(Boolean, default=False)
    lock_photos = Column(Boolean, default=False)
    lock_videos = Column(Boolean, default=False)
    lock_links = Column(Boolean, default=False)
    lock_usernames = Column(Boolean, default=False)

class UserStats(Base):
    __tablename__ = "user_stats"
    id = Column(Integer, primary_key=True)
    user_id = Column(BigInteger)
    chat_id = Column(BigInteger, ForeignKey("group_settings.chat_id"))
    warns_count = Column(Integer, default=0)
    messages_count = Column(Integer, default=0)`
  },
  {
    name: "antiflood.py",
    path: "bot/middlewares/antiflood.py",
    language: "python",
    code: `import time
from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import Message
from bot.config import settings
import redis.asyncio as aioredis

class AntiFloodMiddleware(BaseMiddleware):
    def __init__(self, limit_seconds: float = 1.5):
        self.limit = limit_seconds
        self.redis = aioredis.from_url(settings.REDIS_URL) if settings.REDIS_URL else None
        self.local_cache: Dict[str, float] = {}

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        if not event.chat or event.chat.type == "private":
            return await handler(event, data)
            
        chat_id = event.chat.id
        user_id = event.from_user.id
        key = f"flood:{chat_id}:{user_id}"
        current_time = time.time()
        
        if self.redis:
            last_time = await self.redis.get(key)
            if last_time and current_time - float(last_time) < self.limit:
                await event.delete()
                return
            await self.redis.set(key, str(current_time), ex=2)
        else:
            last_time = self.local_cache.get(key, 0.0)
            if current_time - last_time < self.limit:
                await event.delete()
                return
            self.local_cache[key] = current_time
            
        return await handler(event, data)`
  },
  {
    name: "moderation.py",
    path: "bot/handlers/moderation.py",
    language: "python",
    code: `from aiogram import Router, F
from aiogram.types import Message, ChatPermissions
from aiogram.filters import Command
from bot.utils.localization import get_text

router = Router(name="moderation")

@router.message(Command("mute"))
async def cmd_mute(message: Message, is_admin: bool, lang: str):
    if not is_admin:
        return await message.reply(get_text(lang, "admin_only"))
    if not message.reply_to_message:
        return await message.reply("Reply to the user you wish to mute.")
        
    target_id = message.reply_to_message.from_user.id
    try:
        await message.chat.restrict(
            target_id,
            permissions=ChatPermissions(can_send_messages=False)
        )
        await message.reply(get_text(lang, "user_muted", user=message.reply_to_message.from_user.full_name, admin=message.from_user.full_name))
    except Exception:
        await message.reply(get_text(lang, "missing_bot_perms"))`
  },
  {
    name: "localization.py",
    path: "bot/utils/localization.py",
    language: "python",
    code: `LOCALIZED_STRINGS = {
    "en": {
        "welcome_start": "👋 Hello! I am an Enterprise-grade Group Management Bot.",
        "admin_only": "❌ This command is restricted to administrators.",
        "captcha_prompt": "🔒 Please solve this simple math puzzle: {question} = ?",
        "captcha_solved": "✅ Verification successful!",
        "user_muted": "🔇 User {user} has been muted by {admin}."
    },
    "fa": {
        "welcome_start": "👋 سلام! من ربات پیشرفته و سازمانی مدیریت گروه هستم.",
        "admin_only": "❌ این دستور فقط برای مدیران گروه مجاز است.",
        "captcha_prompt": "🔒 لطفاً پاسخ مسئله ریاضی را ارسال کنید: {question} = ؟",
        "captcha_solved": "✅ تایید هویت موفقیت‌آمیز بود!",
        "user_muted": "🔇 کاربر {user} توسط {admin} ساکت شد."
    }
}

def get_text(lang: str, key: str, **kwargs) -> str:
    template = LOCALIZED_STRINGS.get(lang, {}).get(key, key)
    return template.format(**kwargs)`
  },
  {
    name: "docker-compose.yml",
    path: "bot/docker-compose.yml",
    language: "yaml",
    code: `version: '3.8'

services:
  redis:
    image: redis:7-alpine
    container_name: tg_bot_redis
    restart: always
    ports:
      - "6379:6379"

  bot:
    build: .
    container_name: tg_group_bot
    restart: always
    depends_on:
      - redis
    env_file:
      - .env`
  }
];
