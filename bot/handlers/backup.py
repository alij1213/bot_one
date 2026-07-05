import json
from aiogram import Router, Bot
from aiogram.types import Message, BufferedInputFile
from aiogram.filters import Command
from sqlalchemy.ext.asyncio import AsyncSession
from bot.utils.localization import get_text
from bot.database.crud import get_or_create_group

router = Router(name="backup")

@router.message(Command("backup"))
async def cmd_backup(message: Message, db_session: AsyncSession, is_admin: bool, lang: str):
    """Exports all group configurations into a JSON file."""
    if not is_admin:
        return await message.reply(get_text(lang, "admin_only"))
        
    group = await get_or_create_group(db_session, message.chat.id, message.chat.title)
    
    # Pack settings into dictionary
    backup_data = {
        "chat_id": group.chat_id,
        "language": group.language,
        "anti_spam": group.anti_spam,
        "anti_flood": group.anti_flood,
        "anti_raid": group.anti_raid,
        "anti_bot": group.anti_bot,
        "anti_link": group.anti_link,
        "anti_forward": group.anti_forward,
        "anti_mention": group.anti_mention,
        "anti_invite": group.anti_invite,
        "anti_nsfw": group.anti_nsfw,
        "verification_required": group.verification_required,
        "welcome_enabled": group.welcome_enabled,
        "goodbye_enabled": group.goodbye_enabled,
        "welcome_message": group.welcome_message,
        "goodbye_message": group.goodbye_message,
        "slow_mode_delay": group.slow_mode_delay,
        "lock_text": group.lock_text,
        "lock_photos": group.lock_photos,
        "lock_videos": group.lock_videos,
        "lock_voice": group.lock_voice,
        "lock_audio": group.lock_audio,
        "lock_gif": group.lock_gif,
        "lock_stickers": group.lock_stickers,
        "lock_documents": group.lock_documents,
        "lock_polls": group.lock_polls,
        "lock_games": group.lock_games,
        "lock_contacts": group.lock_contacts,
        "lock_locations": group.lock_locations,
        "lock_links": group.lock_links,
        "lock_usernames": group.lock_usernames,
        "lock_forwards": group.lock_forwards,
        "lock_bots": group.lock_bots
    }
    
    # Serialize to JSON
    json_bytes = json.dumps(backup_data, indent=2).encode("utf-8")
    
    backup_file = BufferedInputFile(
        file=json_bytes,
        filename=f"tg_group_backup_{message.chat.id}.json"
    )
    
    await message.reply_document(
        document=backup_file,
        caption=get_text(lang, "backup_done")
    )

@router.message(Command("restore"))
async def cmd_restore(message: Message, bot: Bot, db_session: AsyncSession, is_admin: bool, lang: str):
    """Restores group configuration settings from an uploaded JSON backup file."""
    if not is_admin:
        return await message.reply(get_text(lang, "admin_only"))
        
    if not message.reply_to_message or not message.reply_to_message.document:
        return await message.reply("Reply to a valid backup `.json` file to restore settings.", parse_mode="Markdown")
        
    doc = message.reply_to_message.document
    if not doc.file_name.endswith(".json"):
        return await message.reply(get_text(lang, "restore_error"))
        
    try:
        # Download document
        file_info = await bot.get_file(doc.file_id)
        file_bytes = await bot.download_file(file_info.file_path)
        
        # Parse JSON
        backup_data = json.loads(file_bytes.read().decode("utf-8"))
        
        # Verify schema holds chat settings keys
        if "anti_spam" not in backup_data or "verification_required" not in backup_data:
            return await message.reply(get_text(lang, "restore_error"))
            
        group = await get_or_create_group(db_session, message.chat.id, message.chat.title)
        
        # Apply configurations
        for key, value in backup_data.items():
            if key in ("chat_id", "title", "created_at", "updated_at"):
                continue # Skip unique system keys
            if hasattr(group, key):
                setattr(group, key, value)
                
        await db_session.commit()
        await message.reply(get_text(lang, "restore_done"))
    except Exception as e:
        await message.reply(f"{get_text(lang, 'restore_error')}\n\nError details: {str(e)}")
