import logging
import anthropic
from config import ANTHROPIC_API_KEY, CLAUDE_MODEL, CLAUDE_MAX_TOKENS, CLAUDE_TEMPERATURE, CLAUDE_REVIEW_MAX_TOKENS

logger = logging.getLogger(__name__)

# Initialize Claude client
client = None

def get_client():
    """Get the Claude client, initializing it if necessary."""
    global client
    if client is None:
        client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
        logger.info("Claude client initialized")
    return client

async def get_reflection(transcription):
    """Get reflective insights from Claude based on the transcription."""
    try:
        client = get_client()
        
        prompt = f"""You are a reflective journaling assistant. I'll share a transcribed voice note.
Please:
1. Provide a concise & empathetic summary (2-3 sentences), as if you're a therapist mirroring a client's words
2. Identify a potential blindspot or assumption - something that the user might not have considered
3. Offer one thoughtful question for further reflection

You should respond as if you're talking directly to the user.
You should be empathetic and understanding.
You should be with the user in their world, but also help them see new perspectives.

Here's the transcribed voice note:
{transcription}"""

        message = client.messages.create(
            model=CLAUDE_MODEL,
            max_tokens=CLAUDE_MAX_TOKENS,
            temperature=CLAUDE_TEMPERATURE,
            system="You are a helpful, empathetic journaling assistant that provides thoughtful reflections.",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        return message.content[0].text
    except Exception as e:
        logger.error(f"Error getting Claude response: {str(e)}")
        return f"I transcribed your message, but couldn't generate reflections (Claude API error).\n\nTranscription:\n{transcription}"

async def get_review_summary(messages, time_period):
    """Generate a summary of multiple entries using Claude."""
    if not messages:
        return f"You don't have any entries from {time_period}."
    
    # Extract transcriptions from messages
    transcriptions = []
    for _, transcription, _, _ in messages:
        transcriptions.append(transcription)
    
    all_transcriptions = "\n\n".join([f"Entry {i+1}: {text}" for i, text in enumerate(transcriptions)])
    
    try:
        client = get_client()
        
        prompt = f"""You are a reflective journaling assistant. I'll share multiple voice note transcriptions from {time_period}.
Please provide:
1. A concise summary of the main themes and topics (3-4 sentences)
2. Identify 2-3 patterns, insights, or connections between entries. This can be as simple as noticing a pattern, or identifying a blindspot or key assumption the user is making.
3. Offer one or two thoughtful questions for further reflection based on these entries

Here are the transcribed voice notes from {time_period}:
{all_transcriptions}"""

        message = client.messages.create(
            model=CLAUDE_MODEL,
            max_tokens=CLAUDE_REVIEW_MAX_TOKENS,
            temperature=CLAUDE_TEMPERATURE,
            system="You are a helpful, empathetic journaling assistant that provides thoughtful reflections on multiple journal entries.",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        return f"📝 Review of your entries from {time_period}:\n\n{message.content[0].text}"
    except Exception as e:
        logger.error(f"Error getting Claude review response: {str(e)}")
        return f"I found {len(messages)} entries from {time_period}, but couldn't generate a review (Claude API error)." 