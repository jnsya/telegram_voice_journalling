import logging
import anthropic
from config import ANTHROPIC_API_KEY, CLAUDE_MODEL, CLAUDE_MAX_TOKENS, CLAUDE_TEMPERATURE, CLAUDE_REVIEW_MAX_TOKENS

logger = logging.getLogger(__name__)

# Initialize Claude client
client = None

# Claude has a context window limit, so we need to limit the transcription length
# Claude 3 Haiku has a 200K context window, but we'll be conservative
MAX_TRANSCRIPTION_LENGTH = 32000  # Characters, not tokens

def get_client():
    """Get the Claude client, initializing it if necessary."""
    global client
    if client is None:
        client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
        logger.info("Claude client initialized")
    return client

def truncate_transcription(transcription):
    """Truncate transcription if it's too long for Claude."""
    if len(transcription) <= MAX_TRANSCRIPTION_LENGTH:
        return transcription
    
    # If it's too long, truncate and add a note
    truncated = transcription[:MAX_TRANSCRIPTION_LENGTH]
    truncated += f"\n\n[Note: Transcription was truncated from {len(transcription)} characters due to length limits]"
    
    logger.warning(f"Transcription truncated from {len(transcription)} to {len(truncated)} characters")
    return truncated

async def get_reflection(transcription):
    """Get reflective insights from Claude based on the transcription."""
    try:
        client = get_client()
        
        # Truncate transcription if necessary
        safe_transcription = truncate_transcription(transcription)
        
        prompt = f"""You are a reflective journaling assistant. I'll share a transcribed voice note.
Please:
1. Provide a concise & empathetic summary (2-3 sentences), as if you're a therapist mirroring a client's words
2. Identify a potential blindspot or assumption - something that the user might not have considered
3. Offer one thoughtful question for further reflection

You should respond as if you're talking directly to the user.
You should be empathetic and understanding.
You should be with the user in their world, but also help them see new perspectives.

Here's the transcribed voice note:
{safe_transcription}"""

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
        return f"I transcribed your message, but couldn't generate reflections (Claude API error).\n\nTranscription:\n{transcription[:500]}... [truncated]"

async def get_review_summary(messages, time_period):
    """Generate a summary of multiple entries using Claude."""
    if not messages:
        return f"You don't have any entries from {time_period}."
    
    # Extract transcriptions from messages
    transcriptions = []
    for _, transcription, _, _ in messages:
        # Limit each transcription to a reasonable length
        if len(transcription) > 5000:  # Arbitrary limit per transcription
            transcription = transcription[:5000] + "... [truncated]"
        transcriptions.append(transcription)
    
    all_transcriptions = "\n\n".join([f"Entry {i+1}: {text}" for i, text in enumerate(transcriptions)])
    
    # Ensure the combined transcriptions aren't too long
    if len(all_transcriptions) > MAX_TRANSCRIPTION_LENGTH:
        logger.warning(f"Combined transcriptions too long ({len(all_transcriptions)} chars). Truncating.")
        all_transcriptions = all_transcriptions[:MAX_TRANSCRIPTION_LENGTH] + "\n\n[Some entries truncated due to length limits]"
    
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