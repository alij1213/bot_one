import re
from aiogram.types import Message
from bot.database.models import GroupSettings

# Basic regex for usernames and links
USERNAME_REGEX = re.compile(r"@\w+")
LINK_REGEX = re.compile(r"(https?://\S+|www\.\S+|\w+\.[a-zA-Z]{2,6})")

def get_violated_lock(message: Message, settings: GroupSettings) -> str | None:
    """
    Checks if the message violates any of the active locks in GroupSettings.
    Returns the name of the violated lock if any, else None.
    """
    # 1. Links Lock
    if settings.lock_links:
        text = message.text or message.caption or ""
        if LINK_REGEX.search(text) or any(ent.type in ("url", "text_link") for ent in (message.entities or message.caption_entities or [])):
            return "links"
            
    # 2. Usernames Lock
    if settings.lock_usernames:
        text = message.text or message.caption or ""
        if USERNAME_REGEX.search(text) or any(ent.type == "mention" for ent in (message.entities or message.caption_entities or [])):
            return "usernames"
            
    # 3. Text Lock (Lock everything containing text)
    if settings.lock_text and message.text:
        return "text"
        
    # 4. Media Locks
    if settings.lock_photos and message.photo:
        return "photos"
        
    if settings.lock_videos and message.video:
        return "videos"
        
    if settings.lock_voice and message.voice:
        return "voice"
        
    if settings.lock_audio and message.audio:
        return "audio"
        
    if settings.lock_gif and message.animation:
        return "gif"
        
    if settings.lock_stickers and message.sticker:
        return "stickers"
        
    if settings.lock_documents and message.document:
        return "documents"
        
    # 5. Interactive and other types
    if settings.lock_polls and message.poll:
        return "polls"
        
    if settings.lock_games and message.game:
        return "games"
        
    if settings.lock_contacts and message.contact:
        return "contacts"
        
    if settings.lock_locations and message.location:
        return "locations"
        
    # 6. Forwards
    if settings.lock_forwards and (message.forward_origin or message.forward_from or message.forward_from_chat):
        return "forwards"
        
    return None
