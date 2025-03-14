import logging
from telegram import Update
from telegram.ext import ContextTypes

from utils.auth import check_authorization
from db.models import get_recent_messages

logger = logging.getLogger(__name__)

async def history_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show recent message history."""
    user_id = update.effective_user.id
    
    # Check if user is authorized
    if not await check_authorization(update, context):
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