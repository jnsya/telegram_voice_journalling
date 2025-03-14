import logging
from telegram.ext import Application, CommandHandler, MessageHandler, filters

from bot.commands.start import start_command
from bot.commands.history import history_command
from bot.commands.entry import entry_command
from bot.commands.weekly import weekly_command
from bot.commands.random import random_command
from bot.commands.delete import delete_command
from bot.commands.review_week import review_week_command
from bot.commands.review_today import review_today_command
from bot.voice_processing import process_voice

logger = logging.getLogger(__name__)

def setup_handlers(application: Application):
    """Set up all command and message handlers."""
    # Add command handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("history", history_command))
    application.add_handler(CommandHandler("entry", entry_command))
    application.add_handler(CommandHandler("weekly", weekly_command))
    application.add_handler(CommandHandler("random", random_command))
    application.add_handler(CommandHandler("delete", delete_command))
    application.add_handler(CommandHandler("review_week", review_week_command))
    application.add_handler(CommandHandler("review_today", review_today_command))
    
    # Add message handlers
    application.add_handler(MessageHandler(filters.VOICE, process_voice))
    
    logger.info("Command and message handlers set up")
    
    return application 