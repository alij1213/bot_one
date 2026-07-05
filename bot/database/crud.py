from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from sqlalchemy.dialects.postgresql import insert as pg_insert
from datetime import datetime
from typing import Optional, List
from bot.database.models import GroupSettings, UserStats, AuditLog

async def get_or_create_group(session: AsyncSession, chat_id: int, title: Optional[str] = None) -> GroupSettings:
    """Gets existing group settings or creates a default record."""
    stmt = select(GroupSettings).where(GroupSettings.chat_id == chat_id)
    result = await session.execute(stmt)
    group = result.scalar_one_or_none()
    
    if not group:
        group = GroupSettings(chat_id=chat_id, title=title)
        session.add(group)
        await session.commit()
        await session.refresh(group)
    elif title and group.title != title:
        group.title = title
        await session.commit()
    
    return group

async def update_group_setting(session: AsyncSession, chat_id: int, field: str, value) -> None:
    """Updates a single field in GroupSettings."""
    stmt = update(GroupSettings).where(GroupSettings.chat_id == chat_id).values({field: value})
    await session.execute(stmt)
    await session.commit()

async def get_or_create_user_stats(session: AsyncSession, user_id: int, chat_id: int) -> UserStats:
    """Gets or creates user statistics for a specific group."""
    # Ensure group exists first
    await get_or_create_group(session, chat_id)
    
    stmt = select(UserStats).where(UserStats.user_id == user_id, UserStats.chat_id == chat_id)
    result = await session.execute(stmt)
    stats = result.scalar_one_or_none()
    
    if not stats:
        stats = UserStats(user_id=user_id, chat_id=chat_id)
        session.add(stats)
        await session.commit()
        await session.refresh(stats)
        
    return stats

async def increment_message_count(session: AsyncSession, user_id: int, chat_id: int) -> None:
    """Increments a user's sent messages count."""
    stats = await get_or_create_user_stats(session, user_id, chat_id)
    stats.messages_count += 1
    stats.last_message_time = datetime.utcnow()
    await session.commit()

async def add_warn(session: AsyncSession, user_id: int, chat_id: int) -> int:
    """Adds a warning to a user, returning the new count."""
    stats = await get_or_create_user_stats(session, user_id, chat_id)
    stats.warns_count += 1
    await session.commit()
    return stats.warns_count

async def reset_warns(session: AsyncSession, user_id: int, chat_id: int) -> None:
    """Resets warning count for a user to zero."""
    stats = await get_or_create_user_stats(session, user_id, chat_id)
    stats.warns_count = 0
    await session.commit()

async def create_audit_log(
    session: AsyncSession, 
    chat_id: int, 
    moderator_id: Optional[int], 
    target_id: Optional[int], 
    action: str, 
    duration: Optional[int] = None, 
    reason: Optional[str] = None
) -> AuditLog:
    """Creates a persistent action audit log."""
    log = AuditLog(
        chat_id=chat_id,
        moderator_id=moderator_id,
        target_id=target_id,
        action=action,
        duration=duration,
        reason=reason
    )
    session.add(log)
    await session.commit()
    await session.refresh(log)
    return log

async def get_stats_summary(session: AsyncSession, chat_id: int) -> dict:
    """Gets total members with stats, total warnings, and total logs."""
    users_stmt = select(UserStats).where(UserStats.chat_id == chat_id)
    users_res = await session.execute(users_stmt)
    users = users_res.scalars().all()
    
    logs_stmt = select(AuditLog).where(AuditLog.chat_id == chat_id)
    logs_res = await session.execute(logs_stmt)
    logs = logs_res.scalars().all()
    
    return {
        "tracked_members": len(users),
        "total_messages": sum(u.messages_count for u in users),
        "total_warnings_active": sum(u.warns_count for u in users),
        "banned_count": sum(1 for u in users if u.is_banned),
        "muted_count": sum(1 for u in users if u.is_muted),
        "total_actions": len(logs)
    }
