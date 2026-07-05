import json
from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, BufferedInputFile
from aiogram.filters import Command
from sqlalchemy.ext.asyncio import AsyncSession
from bot.utils.localization import get_text
from bot.database.crud import get_or_create_group, update_group_setting

router = Router(name="admin")

def get_panel_keyboard(group_settings, lang: str) -> InlineKeyboardMarkup:
    """Generates the security & feature panel interactive inline keyboard toggles."""
    
    # Helper to get checkmark or cross indicator
    ind = lambda field: "🟢 ON" if getattr(group_settings, field) else "🔴 OFF"
    lock_ind = lambda field: "🔒 Locked" if getattr(group_settings, field) else "🔓 Open"
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        # Row 1: Anti-Spam & Anti-Flood
        [
            InlineKeyboardButton(text=f"Anti-Spam: {ind('anti_spam')}", callback_data="toggle:anti_spam"),
            InlineKeyboardButton(text=f"Anti-Flood: {ind('anti_flood')}", callback_data="toggle:anti_flood")
        ],
        # Row 2: Anti-Raid & Anti-Bot
        [
            InlineKeyboardButton(text=f"Anti-Raid: {ind('anti_raid')}", callback_data="toggle:anti_raid"),
            InlineKeyboardButton(text=f"Anti-Bot: {ind('anti_bot')}", callback_data="toggle:anti_bot")
        ],
        # Row 3: Verification Captcha & Welcome
        [
            InlineKeyboardButton(text=f"Captcha: {ind('verification_required')}", callback_data="toggle:verification_required"),
            InlineKeyboardButton(text=f"Welcome msg: {ind('welcome_enabled')}", callback_data="toggle:welcome_enabled")
        ],
        # Row 4: Locks Navigation
        [
            InlineKeyboardButton(text="🔒 Media & Content Locks Menu", callback_data="submenu:locks")
        ],
        # Close button
        [
            InlineKeyboardButton(text="❌ Close / بستن", callback_data="close_panel")
        ]
    ])
    return keyboard

def get_locks_keyboard(group_settings, lang: str) -> InlineKeyboardMarkup:
    """Generates sub-menu for media and content locks."""
    lock_ind = lambda field: "🔒 Lock" if getattr(group_settings, field) else "🔓 Open"
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=f"Text: {lock_ind('lock_text')}", callback_data="lock_toggle:lock_text"),
            InlineKeyboardButton(text=f"Photos: {lock_ind('lock_photos')}", callback_data="lock_toggle:lock_photos")
        ],
        [
            InlineKeyboardButton(text=f"Videos: {lock_ind('lock_videos')}", callback_data="lock_toggle:lock_videos"),
            InlineKeyboardButton(text=f"Voice: {lock_ind('lock_voice')}", callback_data="lock_toggle:lock_voice")
        ],
        [
            InlineKeyboardButton(text=f"Links: {lock_ind('lock_links')}", callback_data="lock_toggle:lock_links"),
            InlineKeyboardButton(text=f"Usernames: {lock_ind('lock_usernames')}", callback_data="lock_toggle:lock_usernames")
        ],
        [
            InlineKeyboardButton(text=f"Forwards: {lock_ind('lock_forwards')}", callback_data="lock_toggle:lock_forwards"),
            InlineKeyboardButton(text=f"Stickers: {lock_ind('lock_stickers')}", callback_data="lock_toggle:lock_stickers")
        ],
        [
            InlineKeyboardButton(text="⬅️ Back / بازگشت", callback_data="submenu:main")
        ]
    ])
    return keyboard

@router.message(Command("panel"))
async def cmd_panel(message: Message, is_admin: bool, group_settings, lang: str):
    """Opens the main configuration control panel in-group."""
    if not is_admin:
        return await message.reply(get_text(lang, "admin_only"))
        
    await message.reply(
        get_text(lang, "settings_panel"),
        reply_markup=get_panel_keyboard(group_settings, lang),
        parse_mode="HTML"
    )

@router.callback_query(F.data == "submenu:locks")
async def show_locks_menu(callback: CallbackQuery, is_admin: bool, group_settings, lang: str):
    if not is_admin:
        return await callback.answer(get_text(lang, "admin_only"), show_alert=True)
        
    await callback.message.edit_reply_markup(reply_markup=get_locks_keyboard(group_settings, lang))
    await callback.answer()

@router.callback_query(F.data == "submenu:main")
async def show_main_menu(callback: CallbackQuery, is_admin: bool, group_settings, lang: str):
    if not is_admin:
        return await callback.answer(get_text(lang, "admin_only"), show_alert=True)
        
    await callback.message.edit_reply_markup(reply_markup=get_panel_keyboard(group_settings, lang))
    await callback.answer()

@router.callback_query(F.data == "close_panel")
async def close_panel_callback(callback: CallbackQuery, is_admin: bool):
    if not is_admin:
        return await callback.answer(get_text("en", "admin_only"), show_alert=True)
    await callback.message.delete()
    await callback.answer()

@router.callback_query(F.data.startswith("toggle:"))
async def toggle_setting_callback(callback: CallbackQuery, db_session: AsyncSession, is_admin: bool, group_settings, lang: str):
    """Toggles regular boolean configuration settings."""
    if not is_admin:
        return await callback.answer(get_text(lang, "admin_only"), show_alert=True)
        
    field = callback.data.split(":")[1]
    current_val = getattr(group_settings, field)
    new_val = not current_val
    
    # Save to db
    await update_group_setting(db_session, callback.message.chat.id, field, new_val)
    setattr(group_settings, field, new_val) # update reference
    
    # Refresh keyboard
    await callback.message.edit_reply_markup(reply_markup=get_panel_keyboard(group_settings, lang))
    await callback.answer(f"Updated setting: {field.replace('_', ' ').capitalize()}")

@router.callback_query(F.data.startswith("lock_toggle:"))
async def toggle_locks_callback(callback: CallbackQuery, db_session: AsyncSession, is_admin: bool, group_settings, lang: str):
    """Toggles locks configuration settings."""
    if not is_admin:
        return await callback.answer(get_text(lang, "admin_only"), show_alert=True)
        
    field = callback.data.split(":")[1]
    current_val = getattr(group_settings, field)
    new_val = not current_val
    
    # Save to db
    await update_group_setting(db_session, callback.message.chat.id, field, new_val)
    setattr(group_settings, field, new_val) # update reference
    
    # Refresh keyboard
    await callback.message.edit_reply_markup(reply_markup=get_locks_keyboard(group_settings, lang))
    await callback.answer(f"Updated lock: {field.replace('lock_', '').capitalize()}")

# ==========================================
# Group Meta Modification Commands
# ==========================================

@router.message(Command("title"))
async def cmd_change_title(message: Message, bot: Bot, is_admin: bool, lang: str):
    """Changes the Telegram group's title."""
    if not is_admin:
        return await message.reply(get_text(lang, "admin_only"))
        
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        return await message.reply("Usage: `/title New Group Title`", parse_mode="Markdown")
        
    new_title = args[1]
    try:
        await message.chat.set_title(new_title)
        await message.reply(f"✅ Title changed to: <b>{new_title}</b>", parse_mode="HTML")
    except Exception:
        await message.reply(get_text(lang, "missing_bot_perms", perms="Change Chat Info"))

@router.message(Command("description"))
async def cmd_change_description(message: Message, is_admin: bool, lang: str):
    """Changes the Telegram group's description."""
    if not is_admin:
        return await message.reply(get_text(lang, "admin_only"))
        
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        return await message.reply("Usage: `/description New description here`", parse_mode="Markdown")
        
    new_desc = args[1]
    try:
        await message.chat.set_description(new_desc)
        await message.reply("✅ Description updated successfully!")
    except Exception:
        await message.reply(get_text(lang, "missing_bot_perms", perms="Change Chat Info"))
