import logging
from telegram import Update
from telegram.ext import ContextTypes

from utils.auth import check_authorization

logger = logging.getLogger(__name__)

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message when the command /start is issued."""
    # Check if user is authorized
    if not await check_authorization(update, context):
        return
    
    await update.message.reply_text(
        "Hi! I'm a voice note reflection bot. Send me a voice message and I'll transcribe it and provide reflective insights!\n\n"
        "Available commands:\n"
        "/history [n] - Show your last n entries (default 5)\n"
        "/entry MSG123 - Show a specific entry by reference ID\n"
        "/weekly - Show all entries from the past week\n"
        "/random - Show a random entry from your history\n"
        "/delete MSG123 - Delete a specific entry by reference ID\n"
        "/review_week - Get AI summary of your entries from the past week\n"
        "/review_today - Get AI summary of your entries from today"
    ) 