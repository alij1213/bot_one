from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from sqlalchemy.ext.asyncio import AsyncSession
from bot.utils.localization import get_text
from bot.database.crud import get_stats_summary

router = Router(name="stats")

@router.message(Command("stats"))
async def cmd_stats(message: Message, db_session: AsyncSession, is_admin: bool, lang: str):
    """Displays real-time analytics and stats for the group."""
    if not is_admin:
        return await message.reply(get_text(lang, "admin_only"))
        
    stats = await get_stats_summary(db_session, message.chat.id)
    
    title = get_text(lang, "stats_title")
    members_text = get_text(lang, "stats_members", members=stats["tracked_members"])
    messages_text = get_text(lang, "stats_messages", messages=stats["total_messages"])
    warnings_text = get_text(lang, "stats_warnings", warnings=stats["total_warnings_active"])
    bans_text = get_text(lang, "stats_bans", bans=stats["banned_count"])
    mutes_text = get_text(lang, "stats_mutes", mutes=stats["muted_count"])
    actions_text = get_text(lang, "stats_actions", actions=stats["total_actions"])
    
    report = (
        f"{title}\n\n"
        f"{members_text}\n"
        f"{messages_text}\n"
        f"{warnings_text}\n"
        f"{bans_text}\n"
        f"{mutes_text}\n"
        f"{actions_text}"
    )
    
    await message.reply(report, parse_mode="HTML")
