from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message, CallbackQuery
from bot.config import settings
from bot.database.connection import async_session
from bot.database.crud import get_or_create_group, get_or_create_user_stats
import logging

class AuthAndDatabaseMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        # Determine chat and user ID
        chat_id = None
        user_id = None
        chat_title = None
        
        if isinstance(event, Message):
            if event.chat:
                chat_id = event.chat.id
                chat_title = event.chat.title
            if event.from_user:
                user_id = event.from_user.id
        elif isinstance(event, CallbackQuery):
            if event.message and event.message.chat:
                chat_id = event.message.chat.id
                chat_title = event.message.chat.title
            if event.from_user:
                user_id = event.from_user.id

        # Open db session for request lifetime
        async with async_session() as session:
            data["db_session"] = session
            
            # Populate group settings and user credentials if in a group
            if chat_id:
                group = await get_or_create_group(session, chat_id, chat_title)
                data["group_settings"] = group
                
                # Check if Owner
                is_owner = (user_id == settings.BOT_OWNER_ID)
                data["is_owner"] = is_owner
                
                # Check if Admin (Telegram Cache)
                is_admin = False
                if is_owner:
                    is_admin = True
                elif chat_id and user_id:
                    # Let's bypass checks for private chats
                    if chat_id > 0: # User IDs are positive, channel/groups are negative
                        is_admin = True
                    else:
                        try:
                            # Use aiogram to fetch administrators
                            bot = data["bot"]
                            member = await bot.get_chat_member(chat_id, user_id)
                            is_admin = member.status in ("administrator", "creator")
                        except Exception as e:
                            logging.debug(f"Could not fetch chat member status: {e}")
                            is_admin = False
                            
                data["is_admin"] = is_admin
                
                # Pre-fetch user statistics
                if user_id:
                    user_stats = await get_or_create_user_stats(session, user_id, chat_id)
                    data["user_stats"] = user_stats
                    
            else:
                # Private chat default
                data["is_owner"] = (user_id == settings.BOT_OWNER_ID) if user_id else False
                data["is_admin"] = True # No admin restrictions in private chat
                
            return await handler(event, data)
