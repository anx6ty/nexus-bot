import aiosqlite
import logging
from typing import Any, List, Optional, Dict
from pathlib import Path

logger = logging.getLogger(__name__)

class Database:
    """SQLite database wrapper for Nexus bot."""
    
    def __init__(self, db_path: str = "./nexus.db"):
        self.db_path = db_path
        self.connection: Optional[aiosqlite.Connection] = None
    
    async def connect(self) -> None:
        """Connect to the database and initialize tables."""
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
        self.connection = await aiosqlite.connect(self.db_path)
        await self.connection.execute("PRAGMA journal_mode = WAL")
        await self.initialize_tables()
        logger.info(f"Connected to database at {self.db_path}")
    
    async def disconnect(self) -> None:
        """Disconnect from the database."""
        if self.connection:
            await self.connection.close()
            logger.info("Disconnected from database")
    
    async def initialize_tables(self) -> None:
        """Initialize all database tables."""
        await self.connection.executescript("""
            CREATE TABLE IF NOT EXISTS guild_config (
                guild_id INTEGER PRIMARY KEY,
                prefix TEXT DEFAULT '$',
                mod_log_channel INTEGER,
                mute_role INTEGER,
                dm_on_punish BOOLEAN DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            
            CREATE TABLE IF NOT EXISTS automod_config (
                guild_id INTEGER PRIMARY KEY,
                anti_nuke BOOLEAN DEFAULT 0,
                anti_link BOOLEAN DEFAULT 0,
                anti_invite BOOLEAN DEFAULT 0,
                anti_raid BOOLEAN DEFAULT 0,
                anti_spam BOOLEAN DEFAULT 0,
                anti_mention BOOLEAN DEFAULT 0,
                anti_caps BOOLEAN DEFAULT 0,
                anti_emoji BOOLEAN DEFAULT 0,
                anti_repeat BOOLEAN DEFAULT 0,
                anti_zalgo BOOLEAN DEFAULT 0,
                anti_phishing BOOLEAN DEFAULT 0,
                anti_scam BOOLEAN DEFAULT 0,
                anti_token_grab BOOLEAN DEFAULT 0,
                anti_ghost_ping BOOLEAN DEFAULT 0,
                anti_nsfw BOOLEAN DEFAULT 0,
                anti_toxic BOOLEAN DEFAULT 0,
                anti_alt BOOLEAN DEFAULT 0,
                anti_vpn BOOLEAN DEFAULT 0,
                anti_webhook_spam BOOLEAN DEFAULT 0,
                anti_everyone BOOLEAN DEFAULT 0,
                automod_log_channel INTEGER,
                action_type TEXT DEFAULT 'mute',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            
            CREATE TABLE IF NOT EXISTS music_config (
                guild_id INTEGER PRIMARY KEY,
                default_volume INTEGER DEFAULT 70,
                dj_role INTEGER,
                max_queue INTEGER DEFAULT 500,
                max_song_length INTEGER DEFAULT 600,
                autoplay BOOLEAN DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            
            CREATE TABLE IF NOT EXISTS user_economy (
                user_id INTEGER PRIMARY KEY,
                guild_id INTEGER,
                balance INTEGER DEFAULT 0,
                bank INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(user_id, guild_id)
            );
            
            CREATE TABLE IF NOT EXISTS user_levels (
                user_id INTEGER,
                guild_id INTEGER,
                xp INTEGER DEFAULT 0,
                level INTEGER DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (user_id, guild_id)
            );
            
            CREATE TABLE IF NOT EXISTS warnings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                guild_id INTEGER,
                moderator_id INTEGER,
                reason TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            
            CREATE TABLE IF NOT EXISTS mutes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                guild_id INTEGER,
                moderator_id INTEGER,
                reason TEXT,
                expires_at TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            
            CREATE TABLE IF NOT EXISTS bans (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                guild_id INTEGER,
                moderator_id INTEGER,
                reason TEXT,
                expires_at TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            
            CREATE TABLE IF NOT EXISTS giveaways (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                guild_id INTEGER,
                message_id INTEGER,
                channel_id INTEGER,
                host_id INTEGER,
                prize TEXT,
                winners INTEGER DEFAULT 1,
                ends_at TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            
            CREATE TABLE IF NOT EXISTS giveaway_entries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                giveaway_id INTEGER,
                user_id INTEGER,
                entered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (giveaway_id) REFERENCES giveaways(id)
            );
            
            CREATE TABLE IF NOT EXISTS tickets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                guild_id INTEGER,
                channel_id INTEGER,
                user_id INTEGER,
                status TEXT DEFAULT 'open',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            
            CREATE TABLE IF NOT EXISTS tags (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                guild_id INTEGER,
                name TEXT,
                content TEXT,
                creator_id INTEGER,
                uses INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(guild_id, name)
            );
            
            CREATE TABLE IF NOT EXISTS reminders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                guild_id INTEGER,
                message TEXT,
                remind_at TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            
            CREATE TABLE IF NOT EXISTS todos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                task TEXT,
                completed BOOLEAN DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            
            CREATE TABLE IF NOT EXISTS quotes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                guild_id INTEGER,
                author TEXT,
                content TEXT,
                creator_id INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            
            CREATE TABLE IF NOT EXISTS birthdays (
                user_id INTEGER PRIMARY KEY,
                guild_id INTEGER,
                month INTEGER,
                day INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            
            CREATE TABLE IF NOT EXISTS suggestions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                guild_id INTEGER,
                user_id INTEGER,
                content TEXT,
                status TEXT DEFAULT 'pending',
                message_id INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            
            CREATE TABLE IF NOT EXISTS reaction_roles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                guild_id INTEGER,
                message_id INTEGER,
                emoji TEXT,
                role_id INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            
            CREATE TABLE IF NOT EXISTS autoresponder (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                guild_id INTEGER,
                trigger TEXT,
                response TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        await self.connection.commit()
        logger.info("Database tables initialized")
    
    async def execute(self, query: str, params: tuple = ()) -> None:
        """Execute a single query."""
        try:
            await self.connection.execute(query, params)
            await self.connection.commit()
        except Exception as e:
            logger.error(f"Database execute error: {e}")
            raise
    
    async def fetch(self, query: str, params: tuple = ()) -> List[tuple]:
        """Fetch multiple rows."""
        try:
            cursor = await self.connection.execute(query, params)
            return await cursor.fetchall()
        except Exception as e:
            logger.error(f"Database fetch error: {e}")
            return []
    
    async def fetchone(self, query: str, params: tuple = ()) -> Optional[tuple]:
        """Fetch a single row."""
        try:
            cursor = await self.connection.execute(query, params)
            return await cursor.fetchone()
        except Exception as e:
            logger.error(f"Database fetchone error: {e}")
            return None
    
    async def executemany(self, query: str, params: List[tuple]) -> None:
        """Execute multiple queries at once."""
        try:
            await self.connection.executemany(query, params)
            await self.connection.commit()
        except Exception as e:
            logger.error(f"Database executemany error: {e}")
            raise