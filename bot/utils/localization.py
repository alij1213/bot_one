from typing import Dict, Any

LOCALIZED_STRINGS: Dict[str, Dict[str, str]] = {
    "en": {
        "welcome_start": "👋 Hello! I am an Enterprise-grade Group Management Bot.\n\nAdd me to a group as an Administrator, and I'll keep it safe, fast, and organized.\n\nOwner: <a href='tg://user?id={owner_id}'>Bot Owner</a>",
        "select_language": "Please select your preferred language / لطفاً زبان مورد نظر خود را انتخاب کنید:",
        "lang_changed": "✅ Language changed to English!",
        "admin_only": "❌ This command is restricted to administrators.",
        "owner_only": "❌ This command is restricted to the Bot Owner.",
        "missing_bot_perms": "❌ I do not have sufficient administrator privileges to perform this action. Required: {perms}",
        "help_text": (
            "🛡️ <b>Telegram Group Management Suite - Help Guide</b>\n\n"
            "<b>General Commands:</b>\n"
            "/start - Start the bot\n"
            "/help - Display this manual\n"
            "/stats - Show group metrics & analytics\n"
            "/language - Switch bot language\n\n"
            "<b>Administrative & Settings:</b>\n"
            "/settings - Open Web Settings dashboard link\n"
            "/panel - Main on-screen admin panel\n"
            "/backup - Export group settings file\n"
            "/restore - Restore group settings from backup file\n\n"
            "<b>Moderation Commands (Reply to user):</b>\n"
            "/mute [duration] [reason] - Mute a user (e.g., 10m, 2h, 1d)\n"
            "/unmute - Lift mute status from user\n"
            "/ban [duration] [reason] - Ban a user from the group\n"
            "/unban - Lift ban status\n"
            "/warn - Add warning (3 warns = Auto temporary Ban)\n"
            "/unwarn - Remove a warning from a user\n"
            "/purge - Delete message history up to the replied message\n"
            "/pin - Pin replied message (use 'loud' for notification)\n"
            "/unpin - Unpin currently pinned message\n\n"
            "<b>Media & Feature Locks:</b>\n"
            "/lock [feature] - Lock a specific content type\n"
            "/unlock [feature] - Unlock a specific content type\n"
            "Features: text, photos, videos, voice, audio, gif, stickers, documents, polls, games, contacts, locations, links, usernames, forwards, bots\n"
        ),
        "captcha_prompt": "🔒 <b>Security Verification</b>\n\nWelcome {user}! To prevent bots, please solve this simple math puzzle within 60 seconds:\n\n<blockquote><b>{question} = ?</b></blockquote>",
        "captcha_solved": "✅ Verification successful! Welcome to the group.",
        "captcha_failed": "❌ Incorrect captcha or time expired. You have been kicked.",
        "user_muted": "🔇 <b>User Muted</b>\n\n<b>User:</b> {user}\n<b>Admin:</b> {admin}\n<b>Duration:</b> {duration}\n<b>Reason:</b> {reason}",
        "user_unmuted": "🔊 <b>User Unmuted</b>\n\n<b>User:</b> {user}\n<b>Admin:</b> {admin}",
        "user_banned": "🚷 <b>User Banned</b>\n\n<b>User:</b> {user}\n<b>Admin:</b> {admin}\n<b>Duration:</b> {duration}\n<b>Reason:</b> {reason}",
        "user_unbanned": "✅ <b>User Unbanned</b>\n\n<b>User:</b> {user}\n<b>Admin:</b> {admin}",
        "user_kicked": "🚪 <b>User Kicked</b>\n\n<b>User:</b> {user}\n<b>Admin:</b> {admin}\n<b>Reason:</b> {reason}",
        "user_warned": "⚠️ <b>Warning Issued</b>\n\n<b>User:</b> {user}\n<b>Admin:</b> {admin}\n<b>Warnings:</b> {warns}/3\n<b>Reason:</b> {reason}",
        "user_unwarned": "🩹 <b>Warning Removed</b>\n\n<b>User:</b> {user}\n<b>Admin:</b> {admin}\n<b>Warnings:</b> {warns}/3",
        "warn_ban_trigger": "🚨 User {user} reached 3 warnings. Issuing auto temporary 24-hour Ban.",
        "purge_done": "🧹 Purged {count} messages successfully.",
        "pinned_msg": "📌 Message pinned successfully.",
        "unpinned_msg": "📌 Message unpinned successfully.",
        "settings_panel": "⚙️ <b>Group Security & Feature Panel</b>\n\nConfigure anti-spam, locks, and automatic moderation here:",
        "lock_success": "🔒 Feature <b>{feature}</b> has been locked. Members cannot send this content.",
        "unlock_success": "🔓 Feature <b>{feature}</b> has been unlocked.",
        "slowmode_updated": "⏱️ Slow mode delay has been set to <b>{delay}s</b>.",
        "stats_title": "📊 <b>Group Metrics & Analytics</b>",
        "stats_members": "• Tracked active members: {members}",
        "stats_messages": "• Total logged messages: {messages}",
        "stats_warnings": "• Active total warnings: {warnings}",
        "stats_bans": "• Total bans logged: {bans}",
        "stats_mutes": "• Total active mutes: {mutes}",
        "stats_actions": "• Total audit actions: {actions}",
        "backup_done": "📦 <b>Backup Export</b>\n\nHere is your group settings backup file. You can restore this using /restore in this or another group.",
        "restore_done": "✅ Group settings backup restored successfully!",
        "restore_error": "❌ Invalid backup file format.",
        "security_alert": "🛡️ <b>Anti-Flood / Anti-Spam Trigger</b>\n\n<b>User:</b> {user}\n<b>Action:</b> Spamming detected. User has been automatically muted for 1 hour.",
        "raid_alert": "🚨 <b>Anti-Raid Shield Activated</b>\n\nRapid join rate detected. Temporary chat locks enabled.",
        "nsfw_blocked": "🔞 <b>NSFW Image Blocked</b>\n\n<b>User:</b> {user} tried to send explicit content, message deleted.",
        "link_blocked": "🔗 <b>Link Blocked</b>\n\n<b>User:</b> {user} tried to send links. Locked in this group.",
        "bot_blocked": "🤖 <b>Anti-Bot Triggered</b>\n\nUnauthorized bot {bot} was invited and has been banned.",
        "forward_blocked": "🔄 <b>Forwarding Blocked</b>\n\n<b>User:</b> {user} tried to forward message. Locked in this group."
    },
    "fa": {
        "welcome_start": "👋 سلام! من ربات پیشرفته و سازمانی مدیریت گروه هستم.\n\nمن را به عنوان مدیر با دسترسی‌های لازم به گروه خود اضافه کنید تا امنیت، سرعت و آرامش را به گروه هدیه دهم.\n\nمالک ربات: <a href='tg://user?id={owner_id}'>مالک ربات</a>",
        "select_language": "لطفاً زبان مورد نظر خود را انتخاب کنید / Please select your preferred language:",
        "lang_changed": "✅ زبان ربات با موفقیت به فارسی تغییر یافت!",
        "admin_only": "❌ این دستور فقط برای مدیران گروه مجاز است.",
        "owner_only": "❌ این دستور فقط برای مالک اصلی ربات مجاز است.",
        "missing_bot_perms": "❌ من دسترسی‌های کافی برای انجام این کار را ندارم. دسترسی‌های مورد نیاز: {perms}",
        "help_text": (
            "🛡️ <b>راهنمای ربات مدیریت گروه سازمانی</b>\n\n"
            "<b>دستورات عمومی:</b>\n"
            "/start - شروع کار ربات\n"
            "/help - نمایش این دفترچه راهنما\n"
            "/stats - آمار و وضعیت گروه\n"
            "/language - تغییر زبان ربات\n\n"
            "<b>دستورات مدیریتی و تنظیمات:</b>\n"
            "/settings - لینک داشبورد تنظیمات تحت وب\n"
            "/panel - باز کردن پنل تنظیمات در گروه\n"
            "/backup - خروجی گرفتن از تنظیمات گروه\n"
            "/restore - بازیابی تنظیمات از فایل پشتیبان\n\n"
            "<b>دستورات تعدیل (با ریپلای روی کاربر):</b>\n"
            "/mute [مدت زمان] [علت] - سکوت کاربر (مثال: 10m, 2h, 1d)\n"
            "/unmute - حذف وضعیت سکوت کاربر\n"
            "/ban [مدت زمان] [علت] - اخراج و مسدودسازی کاربر\n"
            "/unban - لغو مسدودسازی کاربر\n"
            "/warn - ثبت اخطار (۳ اخطار = مسدودسازی خودکار ۲۴ ساعته)\n"
            "/unwarn - حذف یک اخطار از کاربر\n"
            "/purge - پاکسازی پیام‌ها تا پیام ریپلای شده\n"
            "/pin - پین کردن پیام ریپلای شده\n"
            "/unpin - حذف پیام پین شده فعلی\n\n"
            "<b>قفل‌های رسانه و ویژگی‌ها:</b>\n"
            "/lock [قفل] - قفل کردن یک نوع پیام خاص\n"
            "/unlock [قفل] - باز کردن یک نوع پیام خاص\n"
            "قفل‌های قابل استفاده: text, photos, videos, voice, audio, gif, stickers, documents, polls, games, contacts, locations, links, usernames, forwards, bots\n"
        ),
        "captcha_prompt": "🔒 <b>تایید هویت امنیتی</b>\n\nکاربر عزیز {user} به گروه خوش آمدید! برای جلوگیری از ورود ربات‌ها، لطفا مسئله ریاضی زیر را در ۶۰ ثانیه پاسخ دهید:\n\n<blockquote><b>{question} = ?</b></blockquote>",
        "captcha_solved": "✅ تایید هویت موفقیت‌آمیز بود! به گروه خوش آمدید.",
        "captcha_failed": "❌ پاسخ اشتباه یا پایان زمان معتبر. شما از گروه اخراج شدید.",
        "user_muted": "🔇 <b>کاربر ساکت شد</b>\n\n<b>کاربر:</b> {user}\n<b>مدیر:</b> {admin}\n<b>مدت زمان:</b> {duration}\n<b>علت:</b> {reason}",
        "user_unmuted": "🔊 <b>وضعیت سکوت کاربر لغو شد</b>\n\n<b>کاربر:</b> {user}\n<b>مدیر:</b> {admin}",
        "user_banned": "🚷 <b>کاربر مسدود شد (بن)</b>\n\n<b>کاربر:</b> {user}\n<b>مدیر:</b> {admin}\n<b>مدت زمان:</b> {duration}\n<b>علت:</b> {reason}",
        "user_unbanned": "✅ <b>لغو مسدودیت کاربر</b>\n\n<b>کاربر:</b> {user}\n<b>مدیر:</b> {admin}",
        "user_kicked": "🚪 <b>کاربر اخراج شد</b>\n\n<b>کاربر:</b> {user}\n<b>مدیر:</b> {admin}\n<b>علت:</b> {reason}",
        "user_warned": "⚠️ <b>اخطار ثبت شد</b>\n\n<b>کاربر:</b> {user}\n<b>مدیر:</b> {admin}\n<b>اخطارها:</b> {warns}/3\n<b>علت:</b> {reason}",
        "user_unwarned": "🩹 <b>اخطار حذف شد</b>\n\n<b>کاربر:</b> {user}\n<b>مدیر:</b> {admin}\n<b>اخطارها:</b> {warns}/3",
        "warn_ban_trigger": "🚨 کاربر {user} به حد نصاب ۳ اخطار رسید. مسدودسازی خودکار ۲۴ ساعته اعمال شد.",
        "purge_done": "🧹 تعداد {count} پیام با موفقیت پاکسازی شد.",
        "pinned_msg": "📌 پیام با موفقیت پین شد.",
        "unpinned_msg": "📌 پیام با موفقیت آن‌پین شد.",
        "settings_panel": "⚙️ <b>پنل امنیت و تنظیمات گروه</b>\n\nتنظیمات ضد اسپم، قفل‌ها و تعدیل خودکار را اینجا مدیریت کنید:",
        "lock_success": "🔒 ویژگی <b>{feature}</b> قفل شد. اعضا دیگر نمی‌توانند این نوع محتوا را ارسال کنند.",
        "unlock_success": "🔓 ویژگی <b>{feature}</b> باز شد.",
        "slowmode_updated": "⏱️ تاخیر کندباش (Slow Mode) به <b>{delay} ثانیه</b> تغییر یافت.",
        "stats_title": "📊 <b>آمار و سنجه‌های گروه</b>",
        "stats_members": "• کاربران فعال رهگیری‌شده: {members}",
        "stats_messages": "• کل پیام‌های ثبت‌شده: {messages}",
        "stats_warnings": "• تعداد کل اخطارهای فعال: {warnings}",
        "stats_bans": "• کل اخراج و مسدودیت‌ها: {bans}",
        "stats_mutes": "• کل وضعیت‌های سکوت فعال: {mutes}",
        "stats_actions": "• کل عملیات بازرسی: {actions}",
        "backup_done": "📦 <b>خروجی پشتیبان</b>\n\nاین فایل پشتیبان تنظیمات گروه شماست. می‌توانید آن را با دستور /restore در همین گروه یا گروه دیگر بازیابی کنید.",
        "restore_done": "✅ تنظیمات گروه با موفقیت از فایل پشتیبان بازیابی شد!",
        "restore_error": "❌ قالب فایل پشتیبان نامعتبر است.",
        "security_alert": "🛡️ <b>هشدار ضد اسپم / ضد فلود</b>\n\n<b>کاربر:</b> {user}\n<b>علت:</b> ارسال سریع پیام (اسپم). کاربر به مدت ۱ ساعت ساکت شد.",
        "raid_alert": "🚨 <b>شیلد ضد رید فعال شد</b>\n\nعضویت سریع و انبوه کاربران ردیابی شد. قفل موقت چت فعال گردید.",
        "nsfw_blocked": "🔞 <b>تصویر مستهجن مسدود شد</b>\n\n<b>کاربر:</b> {user} قصد ارسال محتوای غیراخلاقی داشت، پیام وی حذف شد.",
        "link_blocked": "🔗 <b>ارسال لینک مسدود شد</b>\n\n<b>کاربر:</b> {user} پیام حاوی لینک ارسال کرد که در این گروه قفل است.",
        "bot_blocked": "🤖 <b>ضد ربات فعال شد</b>\n\nربات غیرمجاز {bot} وارد شد و مسدود گردید.",
        "forward_blocked": "🔄 <b>فوروارد پیام مسدود شد</b>\n\n<b>کاربر:</b> {user} پیامی فوروارد کرد که در این گروه قفل است."
    }
}

def get_text(lang: str, key: str, **kwargs) -> str:
    """Returns localized string with optional formatting."""
    lang_dict = LOCALIZED_STRINGS.get(lang, LOCALIZED_STRINGS["en"])
    template = lang_dict.get(key, LOCALIZED_STRINGS["en"].get(key, key))
    try:
        return template.format(**kwargs)
    except Exception:
        return template
