import os
from pathlib import Path
from faster_whisper import WhisperModel
from telegram import Update
from telegram.ext import Application, MessageHandler, CommandHandler, filters, ContextTypes
from dotenv import load_dotenv
import time
import logging
import anthropic

# Configure logging at the top of your file
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Get authorized user ID from environment variables
AUTHORIZED_USER_ID = int(os.getenv("AUTHORIZED_USER_ID", "0"))

# Initialize Whisper model (options are: tiny, base, small, medium, large)
model = WhisperModel("tiny", device="cpu", compute_type="int8")

# Initialize Claude client
claude_client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# Create directory for temporary voice note storage
VOICE_NOTES_DIR = Path("voice_notes")
VOICE_NOTES_DIR.mkdir(exist_ok=True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message when the command /start is issued."""
    user_id = update.effective_user.id
    
    if AUTHORIZED_USER_ID != 0 and user_id != AUTHORIZED_USER_ID:
        await update.message.reply_text(
            "Sorry, you are not authorized to use this bot."
        )
        logger.warning(f"Unauthorized access attempt by user ID: {user_id}")
        return
    
    await update.message.reply_text(
        "Hi! I'm a voice note reflection bot. Send me a voice message and I'll transcribe it and provide reflective insights!"
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
    if AUTHORIZED_USER_ID != 0 and user_id != AUTHORIZED_USER_ID:
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

        # Send Claude's response back to user
        await status_message.edit_text(f"{claude_response}\n\n---\nOriginal transcription: \"{transcription}\"")
        logger.info(f"Total processing time: {claude_end - start_time:.2f} seconds")

        # Clean up - delete the temporary file
        os.remove(file_path)

    except Exception as e:
        await status_message.edit_text(f"Sorry, an error occurred: {str(e)}")
        logger.error(f"Error processing voice note: {str(e)}")

def main():
    """Start the bot."""
    # Create the Application
    application = Application.builder().token(os.getenv("TELEGRAM_BOT_TOKEN")).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.VOICE, process_voice))

    # Start the Bot
    application.run_polling()

if __name__ == "__main__":
    main() 