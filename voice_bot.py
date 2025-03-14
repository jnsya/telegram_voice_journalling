import os
from pathlib import Path
from faster_whisper import WhisperModel
from telegram import Update
from telegram.ext import Application, MessageHandler, CommandHandler, filters, ContextTypes
from dotenv import load_dotenv
import time
import logging

# Configure logging at the top of your file
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Initialize Whisper model (options are: tiny, base, small, medium, large)
model = WhisperModel("tiny", device="cpu", compute_type="int8")

# Create directory for temporary voice note storage
VOICE_NOTES_DIR = Path("voice_notes")
VOICE_NOTES_DIR.mkdir(exist_ok=True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message when the command /start is issued."""
    await update.message.reply_text(
        "Hi! I'm a voice note transcription bot. Send me a voice message and I'll transcribe it for you!"
    )

async def process_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Process received voice notes."""
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

        # Send transcription back to user
        await status_message.edit_text(f"Transcription:\n\n{transcription}")
        print(f"Total processing time: {transcribe_end - start_time:.2f} seconds")

        # Clean up - delete the temporary file
        os.remove(file_path)

    except Exception as e:
        await status_message.edit_text(f"Sorry, an error occurred: {str(e)}")

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