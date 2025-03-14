import logging
from telegram import Update
from telegram.ext import ContextTypes

from utils.auth import check_authorization
from utils.text import split_text, TELEGRAM_MAX_MESSAGE_LENGTH
from db.models import get_message_by_reference

logger = logging.getLogger(__name__)

async def entry_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show a specific entry by reference ID."""
    user_id = update.effective_user.id
    
    # Check if user is authorized
    if not await check_authorization(update, context):
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
    
    # Send Claude's response first
    header = f"📝 Entry {ref_id} ({date_str}):\n\n"
    claude_message = f"{header}Claude's reflection:\n{claude_response}"
    
    if len(claude_message) <= TELEGRAM_MAX_MESSAGE_LENGTH:
        await update.message.reply_text(claude_message)
    else:
        # Split Claude's response if it's too long
        await update.message.reply_text(f"{header}Claude's reflection (part 1):")
        chunks = split_text(claude_response)
        for i, chunk in enumerate(chunks):
            await update.message.reply_text(f"Part {i+1}:\n{chunk}")
    
    # Send transcription as a separate message
    transcription_message = f"Original transcription:\n\"{transcription}\""
    
    if len(transcription_message) <= TELEGRAM_MAX_MESSAGE_LENGTH:
        await update.message.reply_text(transcription_message)
    else:
        # Split transcription if it's too long
        await update.message.reply_text("Original transcription (split due to length):")
        chunks = split_text(transcription)
        for i, chunk in enumerate(chunks):
            await update.message.reply_text(f"Part {i+1}:\n\"{chunk}\"") 