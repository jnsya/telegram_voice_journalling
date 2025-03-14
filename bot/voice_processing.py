import os
import time
import logging
from pathlib import Path
from telegram import Update
from telegram.ext import ContextTypes

from config import VOICE_NOTES_DIR
from utils.auth import check_authorization
from services.whisper_service import transcribe_audio
from services.claude_service import get_reflection
from db.models import store_message

logger = logging.getLogger(__name__)

# Create directory for temporary voice note storage
Path(VOICE_NOTES_DIR).mkdir(exist_ok=True)

async def process_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Process received voice notes."""
    user_id = update.effective_user.id
    
    # Check if user is authorized
    if not await check_authorization(update, context):
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
        file_path = Path(VOICE_NOTES_DIR) / f"voice_{update.message.message_id}.ogg"
        
        # Download the voice note
        await status_message.edit_text("Downloading voice note...")
        await voice_note.download_to_drive(file_path)
        download_time = time.time()
        logger.info(f"Downloading took: {download_time - file_info_time:.2f} seconds")

        # Transcribe the audio
        await status_message.edit_text("Transcribing...")
        transcribe_start = time.time()
        transcription = transcribe_audio(file_path)
        transcribe_end = time.time()
        logger.info(f"Transcription took: {transcribe_end - transcribe_start:.2f} seconds")

        # Get reflective insights from Claude
        await status_message.edit_text("Generating reflective insights...")
        claude_start = time.time()
        claude_response = await get_reflection(transcription)
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