import asyncio
import re
from datetime import datetime, timedelta
from typing import Optional
from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery, ChatPermissions, InlineKeyboardMarkup, InlineKeyboardButton, ChatMemberUpdated
from aiogram.filters import Command, ChatMemberUpdatedFilter, JOIN_TRANSITION, LEAVE_TRANSITION
from sqlalchemy.ext.asyncio import AsyncSession

from bot.config import settings
from bot.utils.localization import get_text
from bot.utils.captcha import generate_math_captcha
from bot.utils.locks_checker import get_violated_lock
from bot.database.crud import (
    get_or_create_user_stats, add_warn, reset_warns, create_audit_log, increment_message_count
)

router = Router(name="moderation")

# Help parse durations like 10m, 2h, 1d
DURATION_REGEX = re.compile(r"^(\d+)([mhdy])$")

def parse_duration(duration_str: str) -> Optional[timedelta]:
    """Parses duration string like 10m, 2h, 1d into timedelta."""
    match = DURATION_REGEX.match(duration_str.lower())
    if not match:
        return None
        
    value = int(match.group(1))
    unit = match.group(2)
    
    if unit == "m":
        return timedelta(minutes=value)
    elif unit == "h":
        return timedelta(hours=value)
    elif unit == "d":
        return timedelta(days=value)
    elif unit == "y":
        return timedelta(days=value * 365)
    return None

# ==========================================
# 1. Verification / Welcome & Goodbye Captchas
# ==========================================

@router.chat_member(ChatMemberUpdatedFilter(JOIN_TRANSITION))
async def on_user_join(event: ChatMemberUpdated, bot: Bot, db_session: AsyncSession, group_settings, lang: str):
    """Triggers captcha verification or sends customizable welcome message when a user joins."""
    if not event.new_chat_member or event.new_chat_member.user.is_bot:
        # Anti-Bot: If group_settings.anti_bot is active, ban unauthorized bots
        if event.new_chat_member and event.new_chat_member.user.is_bot and group_settings.anti_bot:
            try:
                await event.chat.ban(event.new_chat_member.user.id)
                await event.chat.delete_message(event.invite_link.id if event.invite_link else 0)
                await bot.send_message(
                    event.chat.id, 
                    get_text(lang, "bot_blocked", bot=event.new_chat_member.user.full_name)
                )
            except Exception:
                pass
        return

    new_user = event.new_chat_member.user
    chat_id = event.chat.id
    
    # 1. Custom Welcome Enabled
    if group_settings.welcome_enabled:
        # Check Captcha setting
        if group_settings.verification_required:
            question, answer, choices = generate_math_captcha()
            
            # Generate keyboard choices
            keyboard_buttons = []
            row = []
            for choice in choices:
                row.append(InlineKeyboardButton(text=str(choice), callback_data=f"verify:{new_user.id}:{choice}:{answer}"))
                if len(row) == 2:
                    keyboard_buttons.append(row)
                    row = []
            if row:
                keyboard_buttons.append(row)
                
            captcha_kb = InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)
            
            prompt_text = get_text(
                lang, "captcha_prompt", 
                user=new_user.get_mention(as_html=True), question=question
            )
            
            # Restrict new joiner until they solve captcha
            try:
                await event.chat.restrict(
                    new_user.id,
                    permissions=ChatPermissions(
                        can_send_messages=False,
                        can_send_media_messages=False,
                        can_send_other_messages=False,
                        can_add_web_page_previews=False
                    )
                )
            except Exception:
                pass
                
            sent_msg = await bot.send_message(
                chat_id, prompt_text, reply_markup=captcha_kb, parse_mode="HTML"
            )
            
            # Schedule automatic timeout check (60s)
            async def timeout_check():
                await asyncio.sleep(60)
                try:
                    # Fetch user member info to see if still restricted or left
                    member = await event.chat.get_member(new_user.id)
                    if member.status in ("restricted", "member") and not member.can_send_messages:
                        await event.chat.ban(new_user.id)
                        await bot.delete_message(chat_id, sent_msg.message_id)
                        await bot.send_message(chat_id, get_text(lang, "captcha_failed"))
                except Exception:
                    pass
                    
            asyncio.create_task(timeout_check())
            
        else:
            # Custom plain welcome message
            plain_welcome = group_settings.welcome_message.replace("{user}", new_user.full_name)
            await bot.send_message(chat_id, plain_welcome)

@router.callback_query(F.data.startswith("verify:"))
async def process_verification(callback: CallbackQuery, lang: str):
    """Processes math puzzle captcha verification answers."""
    data_parts = callback.data.split(":")
    target_user_id = int(data_parts[1])
    chosen_answer = int(data_parts[2])
    correct_answer = int(data_parts[3])
    
    # Ensure ONLY the joining user can interact
    if callback.from_user.id != target_user_id:
        return await callback.answer("This verification is not for you! ❌", show_alert=True)
        
    if chosen_answer == correct_answer:
        # Lift restrictions
        try:
            await callback.message.chat.restrict(
                target_user_id,
                permissions=ChatPermissions(
                    can_send_messages=True,
                    can_send_media_messages=True,
                    can_send_audios=True,
                    can_send_documents=True,
                    can_send_photos=True,
                    can_send_videos=True,
                    can_send_video_notes=True,
                    can_send_voice_notes=True,
                    can_send_polls=True,
                    can_send_other_messages=True,
                    can_add_web_page_previews=True
                )
            )
        except Exception:
            pass
            
        await callback.answer(get_text(lang, "captcha_solved"))
        await callback.message.delete()
    else:
        # Ban user (kick)
        try:
            await callback.message.chat.ban(target_user_id)
            # Unban instantly to allow re-joining later (functions as simple Kick)
            await callback.message.chat.unban(target_user_id)
        except Exception:
            pass
            
        await callback.answer(get_text(lang, "captcha_failed"), show_alert=True)
        await callback.message.edit_text(get_text(lang, "captcha_failed"))

@router.chat_member(ChatMemberUpdatedFilter(LEAVE_TRANSITION))
async def on_user_leave(event: ChatMemberUpdated, bot: Bot, group_settings, lang: str):
    """Triggers customizable goodbye message when a user leaves."""
    if group_settings.goodbye_enabled and event.old_chat_member:
        user = event.old_chat_member.user
        plain_goodbye = group_settings.goodbye_message.replace("{user}", user.full_name)
        try:
            await bot.send_message(event.chat.id, plain_goodbye)
        except Exception:
            pass

# ==========================================
# 2. Moderation Core Commands
# ==========================================

@router.message(Command("mute"))
async def cmd_mute(message: Message, bot: Bot, db_session: AsyncSession, is_admin: bool, lang: str):
    """Mutes a user (restrict sending messages). Example: /mute 2h [reason]"""
    if not is_admin:
        return await message.reply(get_text(lang, "admin_only"))
        
    if not message.reply_to_message:
        return await message.reply("Reply to the user you wish to mute. Example: `/mute 1h Spamming`", parse_mode="Markdown")
        
    target_user = message.reply_to_message.from_user
    args = message.text.split(maxsplit=2)
    
    duration = None
    reason = "No reason provided"
    
    if len(args) > 1:
        time_delta = parse_duration(args[1])
        if time_delta:
            duration = time_delta
            if len(args) > 2:
                reason = args[2]
        else:
            reason = " ".join(args[1:])
            
    # Apply restriction
    until_date = None
    duration_text = "Permanent"
    if duration:
        until_date = datetime.utcnow() + duration
        duration_text = args[1]
        
    try:
        await message.chat.restrict(
            target_user.id,
            permissions=ChatPermissions(can_send_messages=False),
            until_date=until_date
        )
        
        # Log event in Audit Log
        await create_audit_log(
            db_session, message.chat.id, message.from_user.id, target_user.id,
            "mute", int(duration.total_seconds()) if duration else None, reason
        )
        
        await message.reply(
            get_text(
                lang, "user_muted", 
                user=target_user.full_name, admin=message.from_user.full_name,
                duration=duration_text, reason=reason
            ),
            parse_mode="HTML"
        )
    except Exception as e:
        await message.reply(get_text(lang, "missing_bot_perms", perms="Restrict Members"))

@router.message(Command("unmute"))
async def cmd_unmute(message: Message, db_session: AsyncSession, is_admin: bool, lang: str):
    """Unmutes a user."""
    if not is_admin:
        return await message.reply(get_text(lang, "admin_only"))
        
    if not message.reply_to_message:
        return await message.reply("Reply to the user you wish to unmute.")
        
    target_user = message.reply_to_message.from_user
    
    try:
        await message.chat.restrict(
            target_user.id,
            permissions=ChatPermissions(
                can_send_messages=True,
                can_send_media_messages=True,
                can_send_other_messages=True,
                can_add_web_page_previews=True
            )
        )
        
        await create_audit_log(
            db_session, message.chat.id, message.from_user.id, target_user.id, "unmute"
        )
        
        await message.reply(
            get_text(lang, "user_unmuted", user=target_user.full_name, admin=message.from_user.full_name),
            parse_mode="HTML"
        )
    except Exception:
        await message.reply(get_text(lang, "missing_bot_perms", perms="Restrict Members"))

@router.message(Command("ban"))
async def cmd_ban(message: Message, db_session: AsyncSession, is_admin: bool, lang: str):
    """Bans a user from the group. Example: /ban 3d Spamming"""
    if not is_admin:
        return await message.reply(get_text(lang, "admin_only"))
        
    if not message.reply_to_message:
        return await message.reply("Reply to the user you wish to ban.")
        
    target_user = message.reply_to_message.from_user
    args = message.text.split(maxsplit=2)
    
    duration = None
    reason = "No reason provided"
    
    if len(args) > 1:
        time_delta = parse_duration(args[1])
        if time_delta:
            duration = time_delta
            if len(args) > 2:
                reason = args[2]
        else:
            reason = " ".join(args[1:])
            
    until_date = None
    duration_text = "Permanent"
    if duration:
        until_date = datetime.utcnow() + duration
        duration_text = args[1]
        
    try:
        await message.chat.ban(target_user.id, until_date=until_date)
        
        await create_audit_log(
            db_session, message.chat.id, message.from_user.id, target_user.id,
            "ban", int(duration.total_seconds()) if duration else None, reason
        )
        
        await message.reply(
            get_text(
                lang, "user_banned", 
                user=target_user.full_name, admin=message.from_user.full_name,
                duration=duration_text, reason=reason
            ),
            parse_mode="HTML"
        )
    except Exception:
        await message.reply(get_text(lang, "missing_bot_perms", perms="Ban Members"))

@router.message(Command("unban"))
async def cmd_unban(message: Message, db_session: AsyncSession, is_admin: bool, lang: str):
    """Unbans a user."""
    if not is_admin:
        return await message.reply(get_text(lang, "admin_only"))
        
    if not message.reply_to_message:
        return await message.reply("Reply to the user you wish to unban.")
        
    target_user = message.reply_to_message.from_user
    
    try:
        await message.chat.unban(target_user.id, only_if_banned=True)
        
        await create_audit_log(db_session, message.chat.id, message.from_user.id, target_user.id, "unban")
        
        await message.reply(
            get_text(lang, "user_unbanned", user=target_user.full_name, admin=message.from_user.full_name),
            parse_mode="HTML"
        )
    except Exception:
        await message.reply(get_text(lang, "missing_bot_perms", perms="Ban Members"))

# ==========================================
# 3. Warn / Auto Punishment System
# ==========================================

@router.message(Command("warn"))
async def cmd_warn(message: Message, db_session: AsyncSession, is_admin: bool, lang: str):
    """Issues a warning to a user. On 3 warnings, issues a temporary 24-hour Ban."""
    if not is_admin:
        return await message.reply(get_text(lang, "admin_only"))
        
    if not message.reply_to_message:
        return await message.reply("Reply to the user you wish to warn.")
        
    target_user = message.reply_to_message.from_user
    args = message.text.split(maxsplit=1)
    reason = args[1] if len(args) > 1 else "No reason provided"
    
    # Check if target is an admin
    member = await message.chat.get_member(target_user.id)
    if member.status in ("administrator", "creator"):
        return await message.reply("❌ Cannot warn group administrators!")
        
    new_warns = await add_warn(db_session, target_user.id, message.chat.id)
    await create_audit_log(db_session, message.chat.id, message.from_user.id, target_user.id, "warn", reason=reason)
    
    if new_warns >= 3:
        # Trigger auto 24-hour ban punishment
        try:
            ban_duration = timedelta(days=1)
            until_date = datetime.utcnow() + ban_duration
            
            await message.chat.ban(target_user.id, until_date=until_date)
            await reset_warns(db_session, target_user.id, message.chat.id)
            
            await create_audit_log(
                db_session, message.chat.id, None, target_user.id, 
                "ban", int(ban_duration.total_seconds()), "Auto-Punishment (Reached 3 Warnings)"
            )
            
            await message.reply(get_text(lang, "warn_ban_trigger", user=target_user.full_name))
        except Exception:
            await message.reply(get_text(lang, "missing_bot_perms", perms="Ban Members"))
    else:
        await message.reply(
            get_text(
                lang, "user_warned", 
                user=target_user.full_name, admin=message.from_user.full_name,
                warns=new_warns, reason=reason
            ),
            parse_mode="HTML"
        )

@router.message(Command("unwarn"))
async def cmd_unwarn(message: Message, db_session: AsyncSession, is_admin: bool, lang: str):
    """Removes a warning from a user."""
    if not is_admin:
        return await message.reply(get_text(lang, "admin_only"))
        
    if not message.reply_to_message:
        return await message.reply("Reply to the user you wish to unwarn.")
        
    target_user = message.reply_to_message.from_user
    
    stats = await get_or_create_user_stats(db_session, target_user.id, message.chat.id)
    if stats.warns_count > 0:
        stats.warns_count -= 1
        await db_session.commit()
        await create_audit_log(db_session, message.chat.id, message.from_user.id, target_user.id, "unwarn")
        
    await message.reply(
        get_text(
            lang, "user_unwarned", 
            user=target_user.full_name, admin=message.from_user.full_name, warns=stats.warns_count
        ),
        parse_mode="HTML"
    )

# ==========================================
# 4. Message Pinning and Purge
# ==========================================

@router.message(Command("pin"))
async def cmd_pin(message: Message, is_admin: bool, lang: str):
    """Pins a message. Reply with `/pin loud` to notify all members, otherwise silent."""
    if not is_admin:
        return await message.reply(get_text(lang, "admin_only"))
        
    if not message.reply_to_message:
        return await message.reply("Reply to the message you wish to pin.")
        
    disable_notification = True
    if "loud" in message.text.lower():
        disable_notification = False
        
    try:
        await message.reply_to_message.pin(disable_notification=disable_notification)
        await message.reply(get_text(lang, "pinned_msg"))
    except Exception:
        await message.reply(get_text(lang, "missing_bot_perms", perms="Pin Messages"))

@router.message(Command("unpin"))
async def cmd_unpin(message: Message, is_admin: bool, lang: str):
    """Unpins the current pinned message."""
    if not is_admin:
        return await message.reply(get_text(lang, "admin_only"))
        
    try:
        await message.chat.unpin_message()
        await message.reply(get_text(lang, "unpinned_msg"))
    except Exception:
        await message.reply(get_text(lang, "missing_bot_perms", perms="Pin Messages"))

@router.message(Command("purge"))
async def cmd_purge(message: Message, bot: Bot, is_admin: bool, lang: str):
    """Deletes all messages between the replied message and this command."""
    if not is_admin:
        return await message.reply(get_text(lang, "admin_only"))
        
    if not message.reply_to_message:
        return await message.reply("Reply to the message from which you want to start purging.")
        
    start_id = message.reply_to_message.message_id
    end_id = message.message_id
    
    chat_id = message.chat.id
    msg_ids = list(range(start_id, end_id + 1))
    
    # Telegram allows bulk deleting up to 100 messages at once
    chunks = [msg_ids[i:i + 100] for i in range(0, len(msg_ids), 100)]
    
    count = 0
    for chunk in chunks:
        try:
            await bot.delete_messages(chat_id, chunk)
            count += len(chunk)
        except Exception:
            # Delete one by one if bulk delete fails (e.g. messages older than 48h)
            for msg_id in chunk:
                try:
                    await bot.delete_message(chat_id, msg_id)
                    count += 1
                except Exception:
                    pass
                    
    # Send temporary completion message
    temp = await bot.send_message(chat_id, get_text(lang, "purge_done", count=count))
    await asyncio.sleep(4)
    try:
        await temp.delete()
    except Exception:
        pass

# ==========================================
# 5. Media & Feature Locks Enforcement
# ==========================================

@router.message()
async def check_locks_and_increment_stats(message: Message, db_session: AsyncSession, group_settings, is_admin: bool, lang: str):
    """Checks for active lock violations and locks content accordingly, logs activity stats."""
    # Private chats ignore locks
    if not message.chat or message.chat.type == "private":
        return
        
    # Increment user message count statistics
    if message.from_user:
        await increment_message_count(db_session, message.from_user.id, message.chat.id)
        
    # Administrators and Owners bypass locks completely
    if is_admin:
        return
        
    # Lock violation parser
    violation = get_violated_lock(message, group_settings)
    
    if violation:
        try:
            # Delete message
            await message.delete()
            
            # Send dynamic block warning matching locked media type
            user_mention = message.from_user.get_mention(as_html=True) if message.from_user else "Member"
            block_msg = await message.answer(
                get_text(lang, f"{violation[:-1] if violation.endswith('s') and violation != 'text' else violation}_blocked", user=user_mention, bot=""),
                parse_mode="HTML"
            )
            
            # Auto cleanup block warning
            await asyncio.sleep(5)
            await block_msg.delete()
        except Exception:
            pass
