import sqlite3
import random
from datetime import datetime, timedelta
import logging
from db.database import get_connection

logger = logging.getLogger(__name__)

def store_message(user_id, transcription, claude_response, audio_length=None, voice_file_id=None):
    """Store a message in the database."""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Generate a reference ID (e.g., MSG123)
    cursor.execute("SELECT COUNT(*) FROM messages")
    count = cursor.fetchone()[0]
    reference_id = f"MSG{count+1}"
    
    cursor.execute('''
    INSERT INTO messages (reference_id, user_id, transcription, claude_response, audio_length, voice_file_id)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', (reference_id, user_id, transcription, claude_response, audio_length, voice_file_id))
    
    conn.commit()
    conn.close()
    
    return reference_id

def get_recent_messages(user_id, limit=5):
    """Get recent messages for a user."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
    SELECT reference_id, transcription, claude_response, created_at
    FROM messages
    WHERE user_id = ?
    ORDER BY created_at DESC
    LIMIT ?
    ''', (user_id, limit))
    
    messages = cursor.fetchall()
    conn.close()
    
    return messages

def get_message_by_reference(user_id, reference_id):
    """Get a specific message by its reference ID."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
    SELECT reference_id, transcription, claude_response, created_at
    FROM messages
    WHERE user_id = ? AND reference_id = ?
    ''', (user_id, reference_id))
    
    message = cursor.fetchone()
    conn.close()
    
    return message

def get_random_message(user_id):
    """Get a random message for a user."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
    SELECT reference_id, transcription, claude_response, created_at
    FROM messages
    WHERE user_id = ?
    ''', (user_id,))
    
    messages = cursor.fetchall()
    conn.close()
    
    if not messages:
        return None
    
    return random.choice(messages)

def delete_message(user_id, reference_id):
    """Delete a specific message by its reference ID."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
    DELETE FROM messages
    WHERE user_id = ? AND reference_id = ?
    ''', (user_id, reference_id))
    
    deleted = cursor.rowcount > 0
    conn.commit()
    conn.close()
    
    return deleted

def get_weekly_messages(user_id):
    """Get all messages from the past week for a user."""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Calculate date 7 days ago
    one_week_ago = datetime.now() - timedelta(days=7)
    one_week_ago_str = one_week_ago.strftime('%Y-%m-%d %H:%M:%S')
    
    cursor.execute('''
    SELECT reference_id, transcription, claude_response, created_at
    FROM messages
    WHERE user_id = ? AND created_at >= ?
    ORDER BY created_at DESC
    ''', (user_id, one_week_ago_str))
    
    messages = cursor.fetchall()
    conn.close()
    
    return messages

def get_today_messages(user_id):
    """Get all messages from today for a user."""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Calculate start of today
    today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    today_start_str = today_start.strftime('%Y-%m-%d %H:%M:%S')
    
    cursor.execute('''
    SELECT reference_id, transcription, claude_response, created_at
    FROM messages
    WHERE user_id = ? AND created_at >= ?
    ORDER BY created_at DESC
    ''', (user_id, today_start_str))
    
    messages = cursor.fetchall()
    conn.close()
    
    return messages 