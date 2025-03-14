import sqlite3
import logging
from config import DB_PATH

logger = logging.getLogger(__name__)

def init_db():
    """Initialize the SQLite database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        reference_id TEXT UNIQUE,
        user_id INTEGER,
        transcription TEXT,
        claude_response TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        audio_length FLOAT,
        voice_file_id TEXT
    )
    ''')
    conn.commit()
    conn.close()
    logger.info("Database initialized")

def get_connection():
    """Get a database connection."""
    return sqlite3.connect(DB_PATH) 