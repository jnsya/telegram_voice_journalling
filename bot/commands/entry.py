import logging
from telegram import Update
from telegram.ext import ContextTypes

from utils.auth import check_authorization
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
    
    response = f"📝 Entry {ref_id} ({date_str}):\n\n"
    response += f"Original transcription:\n\"{transcription}\"\n\n"
    response += f"Claude's reflection:\n{claude_response}"
    
    await update.message.reply_text(response) 