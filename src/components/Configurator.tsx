import { useState } from "react";
import { Key, User, Database, Globe, Copy, Check, Info } from "lucide-react";

export function Configurator() {
  const [token, setToken] = useState("718294028:AAH92v-X91L_kP1l_0oR9m9w_1");
  const [ownerId, setOwnerId] = useState("554323211");
  const [dbType, setDbType] = useState<"sqlite" | "postgres">("sqlite");
  const [postgresUrl, setPostgresUrl] = useState("postgresql+asyncpg://postgres:secure_pass@localhost:5432/tg_bot");
  const [redisEnabled, setRedisEnabled] = useState(true);
  const [copied, setCopied] = useState(false);

  const envContent = `# ==========================================
# 🛡️ TELEGRAM GROUP BOT CUSTOM ENVIRONMENT
# Generated on: ${new Date().toLocaleDateString()}
# ==========================================

# Telegram Bot Token (Get it from @BotFather)
BOT_TOKEN=${token}

# Bot Owner's numeric Telegram User ID
BOT_OWNER_ID=${ownerId}

# Database Connection URL
${
  dbType === "sqlite"
    ? "DATABASE_URL=sqlite+aiosqlite:///bot.db"
    : `DATABASE_URL=${postgresUrl}`
}

# Redis Connection URL (For rate limits, anti-flood, caching)
${redisEnabled ? "REDIS_URL=redis://localhost:6379/0" : "# REDIS_URL= (Fallback to local memory)"}

# Admin Logs Channel ID (Optional)
# LOGS_CHANNEL_ID=-1001234567890
`;

  const handleCopy = () => {
    navigator.clipboard.writeText(envContent);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div id="env-configurator" className="bg-slate-900 border border-slate-800 rounded-3xl p-6 lg:p-8 shadow-2xl">
      <div className="flex items-center gap-2 mb-4">
        <Key className="h-5 w-5 text-cyan-400" />
        <h3 className="text-lg font-bold text-slate-100">Environment Configurator</h3>
      </div>
      <p className="text-xs text-slate-400 mb-6 leading-relaxed">
        Replace the default parameters below with your actual Telegram bot token and credentials to automatically compose your secure <code className="bg-slate-950 px-1 py-0.5 rounded text-cyan-400">.env</code> configuration.
      </p>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
        {/* Form Controls */}
        <div className="lg:col-span-5 space-y-5">
          {/* Bot Token */}
          <div className="space-y-1.5">
            <label className="text-xs font-semibold text-slate-300 flex items-center gap-1">
              <span>Bot Token</span>
              <span className="text-red-500">*</span>
            </label>
            <div className="relative">
              <Key className="absolute left-3 top-3 h-4 w-4 text-slate-500" />
              <input
                type="text"
                value={token}
                onChange={(e) => setToken(e.target.value)}
                placeholder="123456789:ABCdefGh..."
                className="w-full bg-slate-950 border border-slate-800 text-xs text-slate-300 rounded-xl pl-9 pr-4 py-3 focus:outline-none focus:border-cyan-500 font-mono transition-colors"
              />
            </div>
          </div>

          {/* Owner ID */}
          <div className="space-y-1.5">
            <label className="text-xs font-semibold text-slate-300 flex items-center gap-1">
              <span>Bot Owner User ID</span>
              <span className="text-red-500">*</span>
            </label>
            <div className="relative">
              <User className="absolute left-3 top-3 h-4 w-4 text-slate-500" />
              <input
                type="number"
                value={ownerId}
                onChange={(e) => setOwnerId(e.target.value)}
                placeholder="YOUR_TELEGRAM_USER_ID"
                className="w-full bg-slate-950 border border-slate-800 text-xs text-slate-300 rounded-xl pl-9 pr-4 py-3 focus:outline-none focus:border-cyan-500 font-mono transition-colors"
              />
            </div>
          </div>

          {/* Database Selector */}
          <div className="space-y-1.5">
            <label className="text-xs font-semibold text-slate-300 flex items-center gap-1">
              <Database className="h-4 w-4 text-slate-500" />
              <span>Database Provider</span>
            </label>
            <div className="grid grid-cols-2 gap-3">
              <button
                type="button"
                onClick={() => setDbType("sqlite")}
                className={`py-2 px-3 text-xs font-semibold rounded-xl border transition-all ${
                  dbType === "sqlite"
                    ? "bg-cyan-500/10 border-cyan-500 text-cyan-400"
                    : "bg-slate-950 border-slate-800 text-slate-400 hover:text-slate-200"
                }`}
              >
                SQLite (Local file)
              </button>
              <button
                type="button"
                onClick={() => setDbType("postgres")}
                className={`py-2 px-3 text-xs font-semibold rounded-xl border transition-all ${
                  dbType === "postgres"
                    ? "bg-cyan-500/10 border-cyan-500 text-cyan-400"
                    : "bg-slate-950 border-slate-800 text-slate-400 hover:text-slate-200"
                }`}
              >
                PostgreSQL
              </button>
            </div>
          </div>

          {/* Postgres URL (Conditional) */}
          {dbType === "postgres" && (
            <div className="space-y-1.5 animate-fadeIn">
              <label className="text-xs font-semibold text-slate-400">Postgres Connection URL</label>
              <input
                type="text"
                value={postgresUrl}
                onChange={(e) => setPostgresUrl(e.target.value)}
                className="w-full bg-slate-950 border border-slate-800 text-xs text-slate-300 rounded-xl px-4 py-3 focus:outline-none focus:border-cyan-500 font-mono"
              />
            </div>
          )}

          {/* Redis Toggle */}
          <div className="flex items-center justify-between p-3.5 bg-slate-950 rounded-xl border border-slate-800/80">
            <div>
              <h4 className="text-xs font-semibold text-slate-200">Enable Redis Caching</h4>
              <p className="text-[10px] text-slate-500 mt-0.5">Used for anti-flood rate limits.</p>
            </div>
            <label className="relative inline-flex items-center cursor-pointer">
              <input
                type="checkbox"
                checked={redisEnabled}
                onChange={(e) => setRedisEnabled(e.target.checked)}
                className="sr-only peer"
              />
              <div className="w-9 h-5 bg-slate-800 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-0.5 after:left-[2px] after:bg-slate-400 after:border-slate-300 after:border after:rounded-full after:h-4 after:w-4 after:transition-all peer-checked:bg-cyan-500 peer-checked:after:bg-slate-950 peer-checked:after:border-transparent"></div>
            </label>
          </div>
        </div>

        {/* Generated output .env */}
        <div className="lg:col-span-7 flex flex-col bg-slate-950 border border-slate-800 rounded-2xl h-[330px] overflow-hidden">
          <div className="px-5 py-3.5 bg-slate-900 border-b border-slate-800/80 flex items-center justify-between">
            <span className="text-[10px] font-mono text-slate-500">.env File Output</span>
            <button
              onClick={handleCopy}
              className="flex items-center gap-1 text-[10px] text-slate-400 hover:text-cyan-400 transition-colors"
            >
              {copied ? (
                <>
                  <Check className="h-3.5 w-3.5 text-emerald-400" />
                  <span className="text-emerald-400">Copied Configuration!</span>
                </>
              ) : (
                <>
                  <Copy className="h-3.5 w-3.5" />
                  <span>Copy Config</span>
                </>
              )}
            </button>
          </div>
          <div className="flex-1 p-5 overflow-auto font-mono text-[10px] sm:text-xs text-slate-300 leading-relaxed select-all">
            <pre>{envContent}</pre>
          </div>
        </div>
      </div>
    </div>
  );
}
