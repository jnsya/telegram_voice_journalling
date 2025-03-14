import os
import sqlite3
from pathlib import Path
from faster_whisper import WhisperModel
from telegram import Update
from telegram.ext import Application, MessageHandler, CommandHandler, filters, ContextTypes
from dotenv import load_dotenv
import time
import logging
import anthropic
from datetime import datetime, timedelta

# Configure logging at the top of your file
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Get authorized user IDs from environment variables
# Format in .env file: AUTHORIZED_USER_IDS=123456789,987654321
authorized_ids_str = os.getenv("AUTHORIZED_USER_IDS", "")
AUTHORIZED_USER_IDS = [int(id_str) for id_str in authorized_ids_str.split(",") if id_str.strip().isdigit()]
logger.info(f"Authorized users: {AUTHORIZED_USER_IDS if AUTHORIZED_USER_IDS else 'No restrictions (all users allowed)'}")

# Initialize Whisper model (options are: tiny, base, small, medium, large)
model = WhisperModel("tiny", device="cpu", compute_type="int8")

# Initialize Claude client
claude_client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# Create directory for temporary voice note storage
VOICE_NOTES_DIR = Path("voice_notes")
VOICE_NOTES_DIR.mkdir(exist_ok=True)

# Database setup
DB_PATH = 'messages.db'

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

def store_message(user_id, transcription, claude_response, audio_length=None, voice_file_id=None):
    """Store a message in the database."""
    conn = sqlite3.connect(DB_PATH)
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
    conn = sqlite3.connect(DB_PATH)
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
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
    SELECT reference_id, transcription, claude_response, created_at
    FROM messages
    WHERE user_id = ? AND reference_id = ?
    ''', (user_id, reference_id))
    
    message = cursor.fetchone()
    conn.close()
    
    return message

def get_weekly_messages(user_id):
    """Get all messages from the past week for a user."""
    conn = sqlite3.connect(DB_PATH)
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

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message when the command /start is issued."""
    user_id = update.effective_user.id
    
    # Check if user is authorized
    if AUTHORIZED_USER_IDS and user_id not in AUTHORIZED_USER_IDS:
        await update.message.reply_text(
            "Sorry, you are not authorized to use this bot."
        )
        logger.warning(f"Unauthorized access attempt by user ID: {user_id}")
        return
    
    await update.message.reply_text(
        "Hi! I'm a voice note reflection bot. Send me a voice message and I'll transcribe it and provide reflective insights!\n\n"
        "Available commands:\n"
        "/history [n] - Show your last n entries (default 5)\n"
        "/entry MSG123 - Show a specific entry by reference ID\n"
        "/weekly - Show all entries from the past week"
    )

async def get_claude_response(transcription):
    """Get reflective insights from Claude based on the transcription."""
    try:
        prompt = f"""You are a reflective journaling assistant. I'll share a transcribed voice note.
Please:
1. Provide a concise summary (2-3 sentences)
2. Identify a potential blindspot or assumption
3. Offer one thoughtful question for further reflection

Here's the transcribed voice note:
{transcription}"""

        message = claude_client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=1000,
            temperature=0.7,
            system="You are a helpful, empathetic journaling assistant that provides thoughtful reflections.",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        return message.content[0].text
    except Exception as e:
        logger.error(f"Error getting Claude response: {str(e)}")
        return f"I transcribed your message, but couldn't generate reflections (Claude API error).\n\nTranscription:\n{transcription}"

async def process_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Process received voice notes."""
    user_id = update.effective_user.id
    
    # Check if user is authorized
    if AUTHORIZED_USER_IDS and user_id not in AUTHORIZED_USER_IDS:
        await update.message.reply_text(
            "Sorry, you are not authorized to use this bot."
        )
        logger.warning(f"Unauthorized access attempt by user ID: {user_id}")
        return
    
    # Send initial status
    status_message = await update.message.reply_text("Receiving your voice note...")
    start_time = time.time()

    try:
        # Get voice note file
        voice_note = await update.message.voice.get_file()
        voice_file_id = update.message.voice.file_id
        audio_length = update.message.voice.duration
        file_info_time = time.time()
        logger.info(f"Getting file info took: {file_info_time - start_time:.2f} seconds")
        
        # Generate unique filename
        file_path = VOICE_NOTES_DIR / f"voice_{update.message.message_id}.ogg"
        
        # Download the voice note
        await status_message.edit_text("Downloading voice note...")
        await voice_note.download_to_drive(file_path)
        download_time = time.time()
        logger.info(f"Downloading took: {download_time - file_info_time:.2f} seconds")

        # Transcribe the audio
        await status_message.edit_text("Transcribing...")
        transcribe_start = time.time()
        segments, info = model.transcribe(str(file_path))
        transcription = " ".join([segment.text for segment in segments])
        transcribe_end = time.time()
        logger.info(f"Transcription took: {transcribe_end - transcribe_start:.2f} seconds")

        # Get reflective insights from Claude
        await status_message.edit_text("Generating reflective insights...")
        claude_start = time.time()
        claude_response = await get_claude_response(transcription)
        claude_end = time.time()
        logger.info(f"Claude API took: {claude_end - claude_start:.2f} seconds")

        # Store message in database
        reference_id = store_message(
            user_id=user_id,
            transcription=transcription,
            claude_response=claude_response,
            audio_length=audio_length,
            voice_file_id=voice_file_id
        )
        
        # Send Claude's response back to user
        await status_message.edit_text(
            f"{claude_response}\n\n"
            f"---\n"
            f"Original transcription: \"{transcription}\"\n\n"
            f"Reference ID: {reference_id}"
        )
        logger.info(f"Total processing time: {claude_end - start_time:.2f} seconds")

        # Clean up - delete the temporary file
        os.remove(file_path)

    except Exception as e:
        await status_message.edit_text(f"Sorry, an error occurred: {str(e)}")
        logger.error(f"Error processing voice note: {str(e)}")

async def history_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show recent message history."""
    user_id = update.effective_user.id
    
    # Check if user is authorized
    if AUTHORIZED_USER_IDS and user_id not in AUTHORIZED_USER_IDS:
        await update.message.reply_text(
            "Sorry, you are not authorized to use this bot."
        )
        logger.warning(f"Unauthorized access attempt by user ID: {user_id}")
        return
    
    # Get limit parameter if provided
    limit = 5
    if context.args and context.args[0].isdigit():
        limit = min(int(context.args[0]), 20)  # Cap at 20 to avoid huge messages
    
    messages = get_recent_messages(user_id, limit)
    
    if not messages:
        await update.message.reply_text("You don't have any message history yet.")
        return
    
    response = f"Your {len(messages)} most recent entries:\n\n"
    
    for ref_id, transcription, claude_response, created_at in messages:
        # Format the date
        date_str = created_at.split('.')[0] if '.' in created_at else created_at
        
        # Truncate transcription if too long
        short_transcription = transcription[:50] + "..." if len(transcription) > 50 else transcription
        
        response += f"📝 {ref_id} ({date_str}): \"{short_transcription}\"\n\n"
    
    response += "Use /entry MSG123 to view a specific entry."
    
    await update.message.reply_text(response)

async def entry_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show a specific entry by reference ID."""
    user_id = update.effective_user.id
    
    # Check if user is authorized
    if AUTHORIZED_USER_IDS and user_id not in AUTHORIZED_USER_IDS:
        await update.message.reply_text(
            "Sorry, you are not authorized to use this bot."
        )
        logger.warning(f"Unauthorized access attempt by user ID: {user_id}")
        return
    
    # Check if reference ID is provided
    if not context.args:
        await update.message.reply_text("Please provide a reference ID, e.g., /entry MSG123")
        return
    
    reference_id = context.args[0].upper()
    message = get_message_by_reference(user_id, reference_id)
    
    if not message:
        await update.message.reply_text(f"Entry {reference_id} not found.")
        return
    
    ref_id, transcription, claude_response, created_at = message
    
    # Format the date
    date_str = created_at.split('.')[0] if '.' in created_at else created_at
    
    response = f"📝 Entry {ref_id} ({date_str}):\n\n"
    response += f"Original transcription:\n\"{transcription}\"\n\n"
    response += f"Claude's reflection:\n{claude_response}"
    
    await update.message.reply_text(response)

async def weekly_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show all entries from the past week."""
    user_id = update.effective_user.id
    
    # Check if user is authorized
    if AUTHORIZED_USER_IDS and user_id not in AUTHORIZED_USER_IDS:
        await update.message.reply_text(
            "Sorry, you are not authorized to use this bot."
        )
        logger.warning(f"Unauthorized access attempt by user ID: {user_id}")
        return
    
    messages = get_weekly_messages(user_id)
    
    if not messages:
        await update.message.reply_text("You don't have any entries from the past week.")
        return
    
    response = f"Your entries from the past week ({len(messages)}):\n\n"
    
    for ref_id, transcription, claude_response, created_at in messages:
        # Format the date
        date_str = created_at.split('.')[0] if '.' in created_at else created_at
        
        # Truncate transcription if too long
        short_transcription = transcription[:50] + "..." if len(transcription) > 50 else transcription
        
        response += f"📝 {ref_id} ({date_str}): \"{short_transcription}\"\n\n"
    
    response += "Use /entry MSG123 to view a specific entry."
    
    await update.message.reply_text(response)

def main():
    """Start the bot."""
    # Initialize database
    init_db()
    
    # Create the Application
    application = Application.builder().token(os.getenv("TELEGRAM_BOT_TOKEN")).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("history", history_command))
    application.add_handler(CommandHandler("entry", entry_command))
    application.add_handler(CommandHandler("weekly", weekly_command))
    application.add_handler(MessageHandler(filters.VOICE, process_voice))

    # Start the Bot
    application.run_polling()

if __name__ == "__main__":
    main() 