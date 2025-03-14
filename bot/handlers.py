import logging
from telegram.ext import Application, CommandHandler, MessageHandler, filters

from bot.commands.start import start_command
from bot.commands.history import history_command
from bot.voice_processing import process_voice

logger = logging.getLogger(__name__)

def setup_handlers(application: Application):
    """Set up all command and message handlers."""
    # Add command handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("history", history_command))
    
    # Add message handlers
    application.add_handler(MessageHandler(filters.VOICE, process_voice))
    
    logger.info("Command and message handlers set up")
    
    return application 