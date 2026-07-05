# 🛡️ Telegram Group Management Bot Suite (aiogram 3.x)

An enterprise-grade, high-performance, modular Telegram Group Management Bot engineered with **Python 3.12+**, **aiogram 3.x**, **SQLAlchemy 2.0**, and **Redis** for state caching and advanced anti-flood rate limiting.

---

## 🌟 Key Features

1. **Enterprise Security & Shielding:**
   - **Anti-Flood & Rate Limiting:** Dynamic message tracking backed by Redis (or in-memory cache fallback) to prevent flooding.
   - **Anti-Spam & Media Locks:** Lock specific types of content (e.g., links, stickers, voice notes, forwards, documents) for standard members.
   - **Anti-Bot & Anti-Raid Shield:** Auto-bans unauthorized bot entries and manages fast-paced group joins.
2. **Localization (English & Persian):**
   - Seamless out-of-the-box support for **English** and **Persian (فارسی)**.
   - Language configuration settings are stored in the group database and apply dynamically per chat.
3. **Advanced Verification System:**
   - Math/Algebraic captcha verification for joining members.
4. **Interactive In-Group Panel:**
   - Elegant, paginated on-screen inline keyboards to manage security thresholds, toggles, and features.
5. **Real-Time Group Analytics:**
   - Advanced group metrics showing total active members, logged messages, warnings issued, active bans, and audit events.
6. **Data Backups:**
   - Command `/backup` lets group administrators export all configurations to a JSON file.
   - Command `/restore` allows instant configuration restoration by replying to a backup file.

---

## 📂 Project Architecture

```
bot/
├── database/
│   ├── __init__.py
│   ├── connection.py   # Async Engine, base models and initialization
│   ├── models.py       # SQLAlchemy models: GroupSettings, UserStats, AuditLog
│   └── crud.py         # DB write/read operations (async)
├── handlers/
│   ├── __init__.py
│   ├── start.py        # /start, /help, /language commands
│   ├── admin.py        # /panel, Group Metadata titles/descriptions
│   ├── moderation.py   # /mute, /ban, /warn, verification, anti-spam filters
│   ├── backup.py       # /backup and /restore managers
│   └── stats.py        # /stats analytics
├── middlewares/
│   ├── __init__.py
│   ├── auth.py         # Database session & authorization injection
│   ├── antiflood.py    # Rate-limiting, anti-spam and Redis key storage
│   └── i18n.py         # Dynamic multi-language resolution
├── utils/
│   ├── __init__.py
│   ├── captcha.py      # Random mathematical questions builder
│   ├── localization.py # Language lookup dictionary maps (EN & FA)
│   └── locks_checker.py# Scans messages for locked flags
├── Dockerfile          # Multi-stage image build instructions
├── docker-compose.yml  # Orchestrates Bot + Redis services
├── requirements.txt    # Stable external pip requirements
└── main.py             # Global bootloader entrypoint
```

---

## 🚀 Quick Start & Installation

### Option A: Running with Docker (Recommended)

1. **Clone & Navigate:**
   ```bash
   cd bot
   ```
2. **Configure Environment:**
   Copy `.env.example` to `.env` and fill in your details:
   ```bash
   cp .env.example .env
   ```
   Edit `.env`:
   ```env
   BOT_TOKEN=YOUR_TELEGRAM_BOT_TOKEN
   BOT_OWNER_ID=YOUR_NUMERIC_TELEGRAM_USER_ID
   DATABASE_URL=sqlite+aiosqlite:///bot.db
   REDIS_URL=redis://redis:6379/0
   ```
3. **Spin up using Docker Compose:**
   ```bash
   docker-compose up -d --build
   ```

### Option B: Local Development (Bare-Metal)

1. **Setup Python Environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
2. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Configure Environment:**
   Create a `.env` file in the `bot` root with your variables.
4. **Run the Bot:**
   ```bash
   python main.py
   ```

---

## 🗄️ Database Migrations: SQLite ➡️ PostgreSQL

The application uses SQLAlchemy's robust database abstraction layer. Upgrading to a production PostgreSQL cluster takes exactly **one step**:

Update your `DATABASE_URL` in `.env` or your host context:
```env
DATABASE_URL=postgresql+asyncpg://postgres_user:postgres_password@localhost:5432/telegram_bot
```
*No other code changes are required! SQLAlchemy automatically compiles the SQL dialects dynamically for your target server.*

---

## 🕹️ Supported Commands

- `/start` - Launches the bot and prompts language preference selection.
- `/help` - Lists the bot administrator manual.
- `/language` - Changes the group's default language.
- `/panel` - Interactive visual inline settings panel (Admin only).
- `/mute [duration] [reason]` - Mute a member (e.g. `/mute 2h Flood`).
- `/unmute` - Remove mute status.
- `/ban [duration] [reason]` - Permanently or temporarily ban a member.
- `/unban` - Remove ban status.
- `/warn [reason]` - Issue warning (Auto temporary 24h ban at 3 warnings).
- `/unwarn` - Remove warnings.
- `/purge` - Delete message history up to current replied message.
- `/pin [loud]` - Pin a message (optionally loud).
- `/unpin` - Unpins the pinned message.
- `/backup` - Export entire group schema settings to JSON file.
- `/restore` - Import group settings (replying to JSON file).
- `/stats` - Displays group statistics.
