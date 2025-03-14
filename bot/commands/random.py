import logging
from telegram import Update
from telegram.ext import ContextTypes

from utils.auth import check_authorization
from db.models import get_random_message

logger = logging.getLogger(__name__)

async def random_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show a random entry from the user's history."""
    user_id = update.effective_user.id
    
    # Check if user is authorized
    if not await check_authorization(update, context):
        return
    
    message = get_random_message(user_id)
    
    if not message:
        await update.message.reply_text("You don't have any entries yet.")
        return
    
    ref_id, transcription, claude_response, created_at = message
    
    # Format the date
    date_str = created_at.split('.')[0] if '.' in created_at else created_at
    
    response = f"📝 Random Entry {ref_id} ({date_str}):\n\n"
    response += f"Original transcription:\n\"{transcription}\"\n\n"
    response += f"Claude's reflection:\n{claude_response}"
    
    await update.message.reply_text(response) 