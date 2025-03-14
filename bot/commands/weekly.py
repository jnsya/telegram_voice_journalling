import logging
from telegram import Update
from telegram.ext import ContextTypes

from utils.auth import check_authorization
from db.models import get_weekly_messages

logger = logging.getLogger(__name__)

async def weekly_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show all entries from the past week."""
    user_id = update.effective_user.id
    
    # Check if user is authorized
    if not await check_authorization(update, context):
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