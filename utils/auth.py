import logging
from config import AUTHORIZED_USER_IDS

logger = logging.getLogger(__name__)

def is_user_authorized(user_id):
    """Check if a user is authorized to use the bot."""
    # If no authorized users are specified, allow all users
    if not AUTHORIZED_USER_IDS:
        return True
    
    # Check if the user is in the authorized list
    is_authorized = user_id in AUTHORIZED_USER_IDS
    
    # Log unauthorized access attempts
    if not is_authorized:
        logger.warning(f"Unauthorized access attempt by user ID: {user_id}")
    
    return is_authorized

async def check_authorization(update, context):
    """Check if the user is authorized and send a message if not."""
    user_id = update.effective_user.id
    
    if not is_user_authorized(user_id):
        await update.message.reply_text(
            "Sorry, you are not authorized to use this bot."
        )
        return False
    
    return True 