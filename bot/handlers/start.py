from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command, CommandStart
from sqlalchemy.ext.asyncio import AsyncSession
from bot.config import settings
from bot.utils.localization import get_text
from bot.database.crud import update_group_setting

router = Router(name="start")

@router.message(CommandStart())
async def cmd_start(message: Message, lang: str):
    """Handles the /start command."""
    # Language selection keyboard
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🇺🇸 English", callback_data="set_lang:en"),
            InlineKeyboardButton(text="🇮🇷 فارسی", callback_data="set_lang:fa")
        ]
    ])
    
    welcome_text = get_text(lang, "welcome_start", owner_id=settings.BOT_OWNER_ID)
    select_prompt = get_text(lang, "select_language")
    
    await message.reply(
        f"{welcome_text}\n\n{select_prompt}",
        reply_markup=keyboard,
        parse_mode="HTML"
    )

@router.message(Command("help"))
async def cmd_help(message: Message, lang: str):
    """Handles the /help command."""
    help_text = get_text(lang, "help_text")
    await message.reply(help_text, parse_mode="HTML")

@router.message(Command("language"))
async def cmd_language(message: Message, lang: str, is_admin: bool):
    """Enforces language choice screen for admins."""
    if not is_admin:
        await message.reply(get_text(lang, "admin_only"))
        return
        
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🇺🇸 English", callback_data="set_lang:en"),
            InlineKeyboardButton(text="🇮🇷 فارسی", callback_data="set_lang:fa")
        ]
    ])
    await message.reply(get_text(lang, "select_language"), reply_markup=keyboard)

@router.callback_query(F.data.startswith("set_lang:"))
async def select_lang_callback(callback: CallbackQuery, db_session: AsyncSession, is_admin: bool):
    """Processes language selection inline buttons."""
    # Ensure sender is admin or owner
    if not is_admin:
        await callback.answer(get_text("en", "admin_only"), show_alert=True)
        return
        
    chosen_lang = callback.data.split(":")[1]
    
    if callback.message and callback.message.chat:
        # Save to database
        await update_group_setting(db_session, callback.message.chat.id, "language", chosen_lang)
        
    # Get localized reply
    feedback_text = get_text(chosen_lang, "lang_changed")
    await callback.answer(feedback_text)
    
    # Update on-screen text to show confirmation
    welcome_text = get_text(chosen_lang, "welcome_start", owner_id=settings.BOT_OWNER_ID)
    await callback.message.edit_text(
        f"{welcome_text}\n\n{feedback_text}",
        parse_mode="HTML"
    )
