import logging
from telegram import Update
from telegram.ext import ContextTypes

from utils.auth import check_authorization
from db.models import get_weekly_messages
from services.claude_service import get_review_summary

logger = logging.getLogger(__name__)

async def review_week_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Generate a review of the past week's entries."""
    user_id = update.effective_user.id
    
    # Check if user is authorized
    if not await check_authorization(update, context):
        return
    
    # Send initial status
    status_message = await update.message.reply_text("Generating your weekly review...")
    
    # Get messages from the past week
    messages = get_weekly_messages(user_id)
    
    if not messages:
        await status_message.edit_text("You don't have any entries from the past week.")
        return
    
    # Generate review using Claude
    review = await get_review_summary(messages, "the past week")
    
    # Add reference IDs at the end
    ref_ids = [ref_id for ref_id, _, _, _ in messages]
    ref_ids_text = ", ".join(ref_ids)
    review += f"\n\nEntries included: {ref_ids_text}"
    
    await status_message.edit_text(review) 