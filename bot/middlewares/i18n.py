from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from bot.database.models import GroupSettings

class InternationalizationMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        # Default language is English
        lang = "en"
        
        # If group settings is loaded, use group's configured language
        group_settings: GroupSettings = data.get("group_settings")
        if group_settings:
            lang = group_settings.language
            
        data["lang"] = lang
        return await handler(event, data)
