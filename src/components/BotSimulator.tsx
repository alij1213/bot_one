import { useState, useEffect } from "react";
import { Send, User, Bot as BotIcon, Shield, RefreshCw, Layers, CheckCircle2, AlertTriangle, Check, X } from "lucide-react";

interface Message {
  sender: "user" | "bot";
  text: string;
  markup?: {
    type: "lang" | "panel" | "captcha" | "locks";
    buttons: Array<{ text: string; action: string; active?: boolean }>;
  };
  timestamp: string;
}

export function BotSimulator() {
  const [lang, setLang] = useState<"en" | "fa">("en");
  const [messages, setMessages] = useState<Message[]>([]);
  const [isJoined, setIsJoined] = useState(true);
  const [captchaAnswer, setCaptchaAnswer] = useState<number>(12);
  const [captchaSolved, setCaptchaSolved] = useState<boolean | null>(null);

  // Group config state for the interactive admin panel
  const [panelConfig, setPanelConfig] = useState({
    antiSpam: true,
    antiFlood: true,
    antiRaid: false,
    antiBot: true,
    verification: true,
    welcome: true,
    // Locks
    lockText: false,
    lockPhotos: false,
    lockVideos: false,
    lockLinks: true,
    lockUsernames: false,
  });

  // Load initial welcome message
  useEffect(() => {
    handleTriggerStart();
  }, [lang]);

  const handleTriggerStart = () => {
    const time = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    const greet = lang === "en" 
      ? "👋 Hello! I am an Enterprise-grade Group Management Bot.\n\nAdd me to a group as an Administrator, and I'll keep it safe, fast, and organized.\n\nOwner: Bot Owner (ID: 554323211)"
      : "👋 سلام! من ربات پیشرفته و سازمانی مدیریت گروه هستم.\n\nمن را به عنوان مدیر با دسترسی‌های لازم به گروه خود اضافه کنید تا امنیت، سرعت و آرامش را به گروه هدیه دهم.\n\nمالک ربات: مالک اصلی (شناسه: 554323211)";

    setMessages([
      {
        sender: "user",
        text: "/start",
        timestamp: time,
      },
      {
        sender: "bot",
        text: greet,
        timestamp: time,
        markup: {
          type: "lang",
          buttons: [
            { text: "🇺🇸 English", action: "set_lang:en", active: lang === "en" },
            { text: "🇮🇷 فارسی", action: "set_lang:fa", active: lang === "fa" },
          ]
        }
      }
    ]);
  };

  const handleTriggerHelp = () => {
    const time = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    const helpEn = `🛡️ <b>Telegram Group Management Suite - Help Guide</b>

<b>General Commands:</b>
/start - Start the bot
/help - Display this manual
/stats - Show group metrics & analytics
/language - Switch bot language

<b>Administrative & Settings:</b>
/settings - Open Web Settings dashboard link
/panel - Main on-screen admin panel
/backup - Export group settings file
/restore - Restore group settings from backup file

<b>Moderation Commands (Reply to user):</b>
/mute [duration] [reason] - Mute a user (e.g., 10m, 2h, 1d)
/unmute - Lift mute status from user
/ban [duration] [reason] - Ban a user from the group
/unban - Lift ban status
/warn - Add warning (3 warns = Auto temporary Ban)`;

    const helpFa = `🛡️ <b>راهنمای ربات مدیریت گروه سازمانی</b>

<b>دستورات عمومی:</b>
/start - شروع کار ربات
/help - نمایش این دفترچه راهنما
/stats - آمار و وضعیت گروه
/language - تغییر زبان ربات

<b>دستورات مدیریتی و تنظیمات:</b>
/settings - لینک داشبورد تنظیمات تحت وب
/panel - باز کردن پنل تنظیمات در گروه
/backup - خروجی گرفتن از تنظیمات گروه
/restore - بازیابی تنظیمات از فایل پشتیبان

<b>دستورات تعدیل (با ریپلای روی کاربر):</b>
/mute [مدت زمان] [علت] - سکوت کاربر (مثال: 10m, 2h, 1d)
/unmute - حذف وضعیت سکوت کاربر
/ban [مدت زمان] [علت] - اخراج و مسدودسازی کاربر
/unban - لغو مسدودسازی کاربر
/warn - ثبت اخطار (۳ اخطار = مسدودسازی خودکار ۲۴ ساعته)`;

    setMessages(prev => [
      ...prev,
      { sender: "user", text: "/help", timestamp: time },
      { sender: "bot", text: lang === "en" ? helpEn : helpFa, timestamp: time }
    ]);
  };

  const handleTriggerPanel = (type: "main" | "locks" = "main") => {
    const time = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    const text = lang === "en" 
      ? "⚙️ <b>Group Security & Feature Panel</b>\n\nConfigure anti-spam, locks, and automatic moderation here:"
      : "⚙️ <b>پنل امنیت و تنظیمات گروه</b>\n\nتنظیمات ضد اسپم، قفل‌ها و تعدیل خودکار را اینجا مدیریت کنید:";

    if (type === "main") {
      setMessages(prev => [
        ...prev,
        { sender: "user", text: "/panel", timestamp: time },
        {
          sender: "bot",
          text: text,
          timestamp: time,
          markup: {
            type: "panel",
            buttons: [
              { text: `Anti-Spam: ${panelConfig.antiSpam ? "🟢 ON" : "🔴 OFF"}`, action: "toggle:antiSpam" },
              { text: `Anti-Flood: ${panelConfig.antiFlood ? "🟢 ON" : "🔴 OFF"}`, action: "toggle:antiFlood" },
              { text: `Anti-Raid: ${panelConfig.antiRaid ? "🟢 ON" : "🔴 OFF"}`, action: "toggle:antiRaid" },
              { text: `Anti-Bot: ${panelConfig.antiBot ? "🟢 ON" : "🔴 OFF"}`, action: "toggle:antiBot" },
              { text: `Captcha Verification: ${panelConfig.verification ? "🟢 ON" : "🔴 OFF"}`, action: "toggle:verification" },
              { text: `Welcome Message: ${panelConfig.welcome ? "🟢 ON" : "🔴 OFF"}`, action: "toggle:welcome" },
              { text: "🔒 Media & Content Locks Menu", action: "submenu:locks" },
            ]
          }
        }
      ]);
    } else {
      setMessages(prev => [
        ...prev,
        {
          sender: "bot",
          text: lang === "en" ? "🔒 <b>Media & Content Locks</b>" : "🔒 <b>قفل‌های رسانه و محتوا</b>",
          timestamp: time,
          markup: {
            type: "locks",
            buttons: [
              { text: `Text Lock: ${panelConfig.lockText ? "🔒 Locked" : "🔓 Open"}`, action: "lock_toggle:lockText" },
              { text: `Photos Lock: ${panelConfig.lockPhotos ? "🔒 Locked" : "🔓 Open"}`, action: "lock_toggle:lockPhotos" },
              { text: `Videos Lock: ${panelConfig.lockVideos ? "🔒 Locked" : "🔓 Open"}`, action: "lock_toggle:lockVideos" },
              { text: `Links Lock: ${panelConfig.lockLinks ? "🔒 Locked" : "🔓 Open"}`, action: "lock_toggle:lockLinks" },
              { text: `Usernames Lock: ${panelConfig.lockUsernames ? "🔒 Locked" : "🔓 Open"}`, action: "lock_toggle:lockUsernames" },
              { text: "⬅️ Back to Main Menu", action: "submenu:main" },
            ]
          }
        }
      ]);
    }
  };

  const handleTriggerStats = () => {
    const time = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    const statsEn = `📊 <b>Group Metrics & Analytics</b>

• Tracked active members: 142
• Total logged messages: 14,831
• Active total warnings: 4
• Total bans logged: 12
• Total active mutes: 2
• Total audit actions: 28`;

    const statsFa = `📊 <b>آمار و سنجه‌های گروه</b>

• کاربران فعال رهگیری‌شده: 142
• کل پیام‌های ثبت‌شده: 14,831
• تعداد کل اخطارهای فعال: 4
• کل اخراج و مسدودیت‌ها: 12
• کل وضعیت‌های سکوت فعال: 2
• کل عملیات بازرسی: 28`;

    setMessages(prev => [
      ...prev,
      { sender: "user", text: "/stats", timestamp: time },
      { sender: "bot", text: lang === "en" ? statsEn : statsFa, timestamp: time }
    ]);
  };

  const handleTriggerJoin = () => {
    const time = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    setCaptchaSolved(null);
    setIsJoined(false);

    const text = lang === "en" 
      ? "🔒 <b>Security Verification</b>\n\nWelcome Alex! To prevent automated bots, please solve this simple math puzzle within 60 seconds:\n\n<blockquote><b>7 + 5 = ?</b></blockquote>"
      : "🔒 <b>تایید هویت امنیتی</b>\n\nکاربر عزیز الکس به گروه خوش آمدید! برای جلوگیری از ورود ربات‌ها، لطفا مسئله ریاضی زیر را در ۶۰ ثانیه پاسخ دهید:\n\n<blockquote><b>7 + 5 = ؟</b></blockquote>";

    setMessages(prev => [
      ...prev,
      { sender: "user", text: "👤 <i>Alex joined the group</i>", timestamp: time },
      {
        sender: "bot",
        text: text,
        timestamp: time,
        markup: {
          type: "captcha",
          buttons: [
            { text: "10", action: "solve:10" },
            { text: "12 (Correct)", action: "solve:12" },
            { text: "14", action: "solve:14" },
            { text: "15", action: "solve:15" },
          ]
        }
      }
    ]);
  };

  // Process clicking buttons in the mock inline keyboards
  const handleAction = (action: string) => {
    const time = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

    if (action.startsWith("set_lang:")) {
      const selected = action.split(":")[1] as "en" | "fa";
      setLang(selected);
    } 
    
    else if (action.startsWith("solve:")) {
      const answer = parseInt(action.split(":")[1]);
      if (answer === 12) {
        setCaptchaSolved(true);
        setIsJoined(true);
        setMessages(prev => [
          ...prev,
          {
            sender: "bot",
            text: lang === "en" ? "✅ <b>Verification successful!</b> Welcome to the group." : "✅ <b>تایید هویت موفقیت‌آمیز بود!</b> به گروه خوش آمدید.",
            timestamp: time
          }
        ]);
      } else {
        setCaptchaSolved(false);
        setMessages(prev => [
          ...prev,
          {
            sender: "bot",
            text: lang === "en" ? "❌ <b>Incorrect captcha.</b> Alex has been kicked." : "❌ <b>پاسخ اشتباه.</b> کاربر از گروه اخراج شد.",
            timestamp: time
          }
        ]);
      }
    } 
    
    else if (action.startsWith("toggle:")) {
      const field = action.split(":")[1] as keyof typeof panelConfig;
      setPanelConfig(prev => {
        const updated = { ...prev, [field]: !prev[field] };
        const fieldStr = String(field);
        
        // Push update notification message
        setMessages(chat => [
          ...chat,
          {
            sender: "bot",
            text: lang === "en" 
              ? `⚙️ Updated parameter: <b>${fieldStr}</b> set to <b>${updated[field] ? "ON" : "OFF"}</b>`
              : `⚙️ پارامتر به‌روزرسانی شد: <b>${fieldStr}</b> روی حالت <b>${updated[field] ? "روشن" : "خاموش"}</b> قرار گرفت`,
            timestamp: time
          }
        ]);
        return updated;
      });
    }

    else if (action.startsWith("lock_toggle:")) {
      const field = action.split(":")[1] as keyof typeof panelConfig;
      setPanelConfig(prev => {
        const updated = { ...prev, [field]: !prev[field] };
        const fieldStr = String(field);
        setMessages(chat => [
          ...chat,
          {
            sender: "bot",
            text: lang === "en"
              ? `🔒 Lock state updated for <b>${fieldStr}</b>: <b>${updated[field] ? "LOCKED" : "OPEN"}</b>`
              : `🔒 وضعیت قفل به‌روزرسانی شد <b>${fieldStr}</b>: <b>${updated[field] ? "قفل" : "باز"}</b>`,
            timestamp: time
          }
        ]);
        return updated;
      });
    }

    else if (action === "submenu:locks") {
      handleTriggerPanel("locks");
    }

    else if (action === "submenu:main") {
      handleTriggerPanel("main");
    }
  };

  return (
    <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 bg-slate-900 border border-slate-800 rounded-3xl overflow-hidden shadow-2xl p-6">
      {/* Bot Sidebar Triggers */}
      <div className="lg:col-span-4 flex flex-col justify-between bg-slate-950 p-5 rounded-2xl border border-slate-800/60">
        <div>
          <div className="flex items-center gap-2 mb-4">
            <Layers className="h-5 w-5 text-cyan-400" />
            <h3 className="text-sm font-semibold uppercase tracking-wider text-slate-300">Command Simulator</h3>
          </div>
          <p className="text-xs text-slate-400 mb-6 leading-relaxed">
            Select standard command buttons below to preview the Telegram user commands and bot replies in real-time.
          </p>

          <div className="space-y-3">
            <button
              onClick={handleTriggerStart}
              className="flex items-center justify-between w-full bg-slate-900 hover:bg-cyan-500/10 hover:border-cyan-500/30 text-left px-4 py-3 rounded-xl border border-slate-800 text-xs text-slate-300 font-mono transition-all group"
            >
              <span>/start</span>
              <span className="text-[10px] text-slate-500 group-hover:text-cyan-400">Boot & Lang</span>
            </button>

            <button
              onClick={handleTriggerHelp}
              className="flex items-center justify-between w-full bg-slate-900 hover:bg-cyan-500/10 hover:border-cyan-500/30 text-left px-4 py-3 rounded-xl border border-slate-800 text-xs text-slate-300 font-mono transition-all group"
            >
              <span>/help</span>
              <span className="text-[10px] text-slate-500 group-hover:text-cyan-400">User Manual</span>
            </button>

            <button
              onClick={() => handleTriggerPanel("main")}
              className="flex items-center justify-between w-full bg-slate-900 hover:bg-cyan-500/10 hover:border-cyan-500/30 text-left px-4 py-3 rounded-xl border border-slate-800 text-xs text-slate-300 font-mono transition-all group"
            >
              <span>/panel</span>
              <span className="text-[10px] text-slate-500 group-hover:text-cyan-400">Admin Panel</span>
            </button>

            <button
              onClick={handleTriggerStats}
              className="flex items-center justify-between w-full bg-slate-900 hover:bg-cyan-500/10 hover:border-cyan-500/30 text-left px-4 py-3 rounded-xl border border-slate-800 text-xs text-slate-300 font-mono transition-all group"
            >
              <span>/stats</span>
              <span className="text-[10px] text-slate-500 group-hover:text-cyan-400">Metrics</span>
            </button>

            <button
              onClick={handleTriggerJoin}
              className="flex items-center justify-between w-full bg-slate-900 hover:bg-emerald-500/10 hover:border-emerald-500/30 text-left px-4 py-3 rounded-xl border border-slate-800 text-xs text-slate-300 font-mono transition-all group"
            >
              <span>👤 Simulate New Join</span>
              <span className="text-[10px] text-slate-500 group-hover:text-emerald-400">Math Captcha</span>
            </button>
          </div>
        </div>

        <div className="pt-6 border-t border-slate-800/80 mt-6">
          <div className="flex items-center justify-between">
            <span className="text-xs text-slate-400">Language Context</span>
            <div className="flex bg-slate-900 p-0.5 rounded-lg border border-slate-800">
              <button
                onClick={() => setLang("en")}
                className={`px-3 py-1 text-xs rounded-md transition-all ${
                  lang === "en" ? "bg-cyan-500 text-slate-950 font-semibold" : "text-slate-400 hover:text-slate-200"
                }`}
              >
                EN
              </button>
              <button
                onClick={() => setLang("fa")}
                className={`px-3 py-1 text-xs rounded-md transition-all ${
                  lang === "fa" ? "bg-cyan-500 text-slate-950 font-semibold" : "text-slate-400 hover:text-slate-200"
                }`}
              >
                FA
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Live Telegram UI Simulator */}
      <div className="lg:col-span-8 bg-slate-950 rounded-2xl border border-slate-800 overflow-hidden flex flex-col h-[520px]">
        {/* Telegram Header */}
        <div className="bg-slate-900/80 px-4 py-3 border-b border-slate-800 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="h-9 w-9 bg-cyan-500/20 rounded-full flex items-center justify-center border border-cyan-500/30">
              <Shield className="h-4 w-4 text-cyan-400" />
            </div>
            <div>
              <h4 className="text-xs font-semibold text-slate-100">Enterprise Shield Bot</h4>
              <p className="text-[10px] text-emerald-400 flex items-center gap-1">
                <span className="h-1.5 w-1.5 bg-emerald-400 rounded-full animate-pulse" />
                bot runs on SQLite & Redis
              </p>
            </div>
          </div>

          <span className="text-[10px] bg-slate-800 text-slate-400 px-2.5 py-1 rounded-full font-mono">
            Chat ID: -1001928421
          </span>
        </div>

        {/* Telegram Messages Logs Box */}
        <div className="flex-1 overflow-y-auto p-4 space-y-4 flex flex-col justify-end">
          {messages.map((msg, index) => (
            <div
              key={index}
              className={`flex flex-col max-w-[85%] ${
                msg.sender === "user" ? "self-end items-end" : "self-start items-start"
              }`}
            >
              {/* Sender Tag */}
              <span className="text-[10px] text-slate-500 mb-1 flex items-center gap-1">
                {msg.sender === "user" ? (
                  <>
                    <User className="h-3 w-3" /> User Admin
                  </>
                ) : (
                  <>
                    <BotIcon className="h-3 w-3 text-cyan-400" /> Shield Bot
                  </>
                )}
                • {msg.timestamp}
              </span>

              {/* Message bubble */}
              <div
                className={`p-3.5 rounded-2xl text-xs leading-relaxed whitespace-pre-wrap shadow-md ${
                  msg.sender === "user"
                    ? "bg-cyan-500 text-slate-950 rounded-tr-none font-mono"
                    : "bg-slate-900 text-slate-200 border border-slate-800 rounded-tl-none"
                }`}
                dangerouslySetInnerHTML={{ __html: msg.text }}
              />

              {/* Keyboard markup */}
              {msg.markup && (
                <div className="grid grid-cols-2 gap-1.5 mt-2 w-full max-w-sm">
                  {msg.markup.buttons.map((btn, btnIdx) => (
                    <button
                      key={btnIdx}
                      onClick={() => handleAction(btn.action)}
                      className={`text-[11px] py-2 px-2.5 rounded-lg text-center transition-all border font-medium ${
                        btn.active
                          ? "bg-cyan-500 text-slate-950 border-cyan-400 font-semibold shadow-lg"
                          : "bg-slate-900/90 text-slate-300 border-slate-800 hover:bg-slate-800 hover:text-slate-100"
                      } ${btn.action === "submenu:locks" || btn.action === "submenu:main" ? "col-span-2" : ""}`}
                    >
                      {btn.text}
                    </button>
                  ))}
                </div>
              )}
            </div>
          ))}
        </div>

        {/* Fake Telegram Input bar */}
        <div className="p-3 border-t border-slate-800/80 bg-slate-900/50 flex items-center gap-3">
          <input
            type="text"
            disabled
            placeholder="Interaction simulated via commands on the left sidebar..."
            className="flex-1 bg-slate-950 border border-slate-800/80 text-xs text-slate-500 rounded-xl px-4 py-2.5 focus:outline-none"
          />
          <button className="h-9 w-9 bg-slate-800 text-slate-600 rounded-xl flex items-center justify-center cursor-not-allowed">
            <Send className="h-4 w-4" />
          </button>
        </div>
      </div>
    </div>
  );
}
