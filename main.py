#!/usr/bin/env python3
import logging
from telegram.ext import Application

from config import TELEGRAM_BOT_TOKEN
from db.database import init_db
from bot.handlers import setup_handlers
from utils.logging import setup_logging
from pathlib import Path

def main():
    """Initialize and start the Telegram bot."""
    # Setup logging
    setup_logging()
    logger = logging.getLogger(__name__)
    logger.info("Starting Telegram Voice Journaling Bot")
    
    # Create necessary directories
    Path("voice_notes").mkdir(exist_ok=True)
    
    # Initialize database
    init_db()
    logger.info("Database initialized")
    
    # Create the Application
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    
    # Setup command and message handlers
    setup_handlers(application)
    logger.info("Handlers registered")
    
    # Start the Bot
    logger.info("Bot started, polling for updates...")
    application.run_polling()

if __name__ == "__main__":
    main() 