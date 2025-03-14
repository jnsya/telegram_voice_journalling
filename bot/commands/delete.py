import logging
from telegram import Update
from telegram.ext import ContextTypes

from utils.auth import check_authorization
from db.models import get_message_by_reference, delete_message

logger = logging.getLogger(__name__)

async def delete_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Delete a specific entry by reference ID."""
    user_id = update.effective_user.id
    
    # Check if user is authorized
    if not await check_authorization(update, context):
        return
    
    # Check if reference ID is provided
    if not context.args:
        await update.message.reply_text("Please provide a reference ID, e.g., /delete MSG123")
        return
    
    reference_id = context.args[0].upper()
    
    # First check if the entry exists
    message = get_message_by_reference(user_id, reference_id)
    if not message:
        await update.message.reply_text(f"Entry {reference_id} not found.")
        return
    
    # Delete the entry
    deleted = delete_message(user_id, reference_id)
    
    if deleted:
        await update.message.reply_text(f"Entry {reference_id} has been deleted.")
    else:
        await update.message.reply_text(f"Failed to delete entry {reference_id}.") 