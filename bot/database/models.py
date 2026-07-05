from sqlalchemy import Column, String, BigInteger, Integer, Boolean, Text, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from bot.database.connection import Base

class GroupSettings(Base):
    __tablename__ = "group_settings"

    chat_id = Column(BigInteger, primary_key=True, index=True)
    title = Column(String(255), nullable=True)
    language = Column(String(10), default="en") # "en" or "fa"
    
    # Anti-Settings (Security toggles)
    anti_spam = Column(Boolean, default=True)
    anti_flood = Column(Boolean, default=True)
    anti_raid = Column(Boolean, default=False)
    anti_bot = Column(Boolean, default=True)
    anti_link = Column(Boolean, default=True)
    anti_forward = Column(Boolean, default=False)
    anti_mention = Column(Boolean, default=False)
    anti_invite = Column(Boolean, default=False)
    anti_nsfw = Column(Boolean, default=False)
    
    # Verification Toggles
    verification_required = Column(Boolean, default=True)
    captcha_type = Column(String(20), default="math") # "math" or "text" or "button"
    
    # Welcome & Goodbye Customizable messages
    welcome_message = Column(Text, default="Welcome {user} to the group! Please solve the captcha below.")
    goodbye_message = Column(Text, default="Goodbye {user}, we will miss you!")
    welcome_enabled = Column(Boolean, default=True)
    goodbye_enabled = Column(Boolean, default=True)
    
    # Slow Mode (Seconds)
    slow_mode_delay = Column(Integer, default=0) # 0 means off
    
    # Locks (True = Locked, False = Unlocked)
    lock_text = Column(Boolean, default=False)
    lock_photos = Column(Boolean, default=False)
    lock_videos = Column(Boolean, default=False)
    lock_voice = Column(Boolean, default=False)
    lock_audio = Column(Boolean, default=False)
    lock_gif = Column(Boolean, default=False)
    lock_stickers = Column(Boolean, default=False)
    lock_documents = Column(Boolean, default=False)
    lock_polls = Column(Boolean, default=False)
    lock_games = Column(Boolean, default=False)
    lock_contacts = Column(Boolean, default=False)
    lock_locations = Column(Boolean, default=False)
    lock_links = Column(Boolean, default=False)
    lock_usernames = Column(Boolean, default=False)
    lock_forwards = Column(Boolean, default=False)
    lock_bots = Column(Boolean, default=False)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class UserStats(Base):
    __tablename__ = "user_stats"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, index=True)
    chat_id = Column(BigInteger, ForeignKey("group_settings.chat_id", ondelete="CASCADE"))
    
    warns_count = Column(Integer, default=0)
    messages_count = Column(Integer, default=0)
    
    is_muted = Column(Boolean, default=False)
    is_banned = Column(Boolean, default=False)
    mute_until = Column(DateTime, nullable=True)
    ban_until = Column(DateTime, nullable=True)
    
    last_message_time = Column(DateTime, nullable=True)

    group = relationship("GroupSettings", backref="users_stats")


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    chat_id = Column(BigInteger, index=True)
    moderator_id = Column(BigInteger, nullable=True) # ID of action taker, NULL if auto by bot
    target_id = Column(BigInteger, nullable=True) # Affected user ID
    
    action = Column(String(50)) # "ban", "kick", "mute", "unmute", "warn", "unwarn", "lock", "unlock"
    duration = Column(Integer, nullable=True) # in seconds, if temporary
    reason = Column(Text, nullable=True)
    
    timestamp = Column(DateTime, default=datetime.utcnow)
