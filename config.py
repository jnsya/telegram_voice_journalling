import os
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Bot configuration
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# User authorization
authorized_ids_str = os.getenv("AUTHORIZED_USER_IDS", "")
AUTHORIZED_USER_IDS = [int(id_str) for id_str in authorized_ids_str.split(",") if id_str.strip().isdigit()]

# API Keys
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

# Whisper model configuration
WHISPER_MODEL = "tiny"  # Options: tiny, base, small, medium, large
WHISPER_DEVICE = "cpu"
WHISPER_COMPUTE_TYPE = "int8"

# Claude model configuration
CLAUDE_MODEL = "claude-3-haiku-20240307"
CLAUDE_MAX_TOKENS = 1000
CLAUDE_TEMPERATURE = 0.7
CLAUDE_REVIEW_MAX_TOKENS = 1500

# Database configuration
DB_PATH = 'messages.db'

# Voice notes storage
VOICE_NOTES_DIR = "voice_notes"

# Logging
def get_logger(name):
    """Get a logger with the specified name."""
    logger = logging.getLogger(name)
    return logger 