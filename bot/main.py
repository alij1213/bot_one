import asyncio
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

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("telegram_group_bot")

async def main():
    logger.info("Initializing Telegram Group Management Suite...")
    
    # 1. Initialize SQLite/PostgreSQL Database Schema
    try:
        await init_db()
        logger.info("Database schemas initialized successfully.")
    except Exception as e:
        logger.error(f"Critical: Database initialization failed: {e}")
        sys.exit(1)

    # 2. Setup FSM and Cache Storage (Redis or Memory)
    if settings.REDIS_URL:
        try:
            storage = RedisStorage.from_url(settings.REDIS_URL)
            logger.info("Connected to Redis cache storage successfully.")
        except Exception as e:
            logger.warning(f"Failed to connect to Redis: {e}. Falling back to MemoryStorage.")
            storage = MemoryStorage()
    else:
        logger.info("No Redis URL supplied. Initializing MemoryStorage.")
        storage = MemoryStorage()

    # 3. Instantiate Bot and Dispatcher
    bot = Bot(token=settings.BOT_TOKEN)
    dp = Dispatcher(storage=storage)

    # 4. Register Middlewares (Order of execution: outer to inner)
    dp.update.outer_middleware(AuthAndDatabaseMiddleware())
    dp.message.middleware(AntiFloodMiddleware())
    dp.update.middleware(InternationalizationMiddleware())

    # 5. Register Handlers Routers
    dp.include_router(start_router)
    dp.include_router(admin_router)
    dp.include_router(moderation_router)
    dp.include_router(backup_router)
    dp.include_router(stats_router)

    # Start polling
    logger.info("Bot is starting polling cycle. Ready!")
    try:
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    except Exception as e:
        logger.error(f"Execution failed or interrupted: {e}")
    finally:
        await bot.session.close()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot stopped successfully.")
