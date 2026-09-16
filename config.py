import os
from dotenv import load_dotenv
from typing import Optional, List

load_dotenv()

class Config:
    """Bot configuration loaded from environment variables."""
    
    # Discord Token
    DISCORD_TOKEN: str = os.environ.get("DISCORD_TOKEN", "")
    
    # Lavalink Configuration
    LAVALINK_HOST: str = os.environ.get("LAVALINK_HOST", "localhost")
    LAVALINK_PORT: int = int(os.environ.get("LAVALINK_PORT", 2333))
    LAVALINK_PASSWORD: str = os.environ.get("LAVALINK_PASSWORD", "youshallnotpass")
    
    # Owner Configuration
    OWNER_IDS: List[int] = [int(id) for id in os.environ.get("OWNER_IDS", "").split(",") if id]
    
    # AI API Key
    AI_API_KEY: str = os.environ.get("AI_API_KEY", "")
    
    # Database Path
    DB_PATH: str = os.environ.get("DB_PATH", "./nexus.db")
    
    # Bot Prefix
    PREFIX: str = "$"
    
    # Theme Colors
    class Color:
        MAIN = 0x2B2D31
        SUCCESS = 0x57F287
        ERROR = 0xED4245
        ACCENT = 0x5865F2
        WARNING = 0xFAA61A
        INFO = 0x00AFF4
    
    # Emojis
    class Emoji:
        SUCCESS = "✅"
        ERROR = "❌"
        WARNING = "⚠️"
        INFO = "ℹ️"
        LOADING = "⏳"
        MUSIC = "🎵"
        MUSIC_PLAY = "▶️"
        MUSIC_PAUSE = "⏸️"
        MUSIC_SKIP = "⏭️"
        MUSIC_LOOP = "🔁"
        MUSIC_STOP = "⏹️"
        MUSIC_PREV = "⏮️"
        VOLUME_UP = "🔊"
        VOLUME_DOWN = "🔉"
        QUEUE = "📋"
        ECONOMY = "💰"
        LEVEL = "📈"
        GIVEAWAY = "🎉"
        TICKET = "🎫"
        ROLES = "🎭"
        WELCOME = "👋"
        MODERATION = "🛡️"
        AUTOMOD = "🚨"
        VOICE = "🔊"
        SOCIAL = "👥"
        AI = "🤖"
        STAR = "⭐"
        
config = Config()