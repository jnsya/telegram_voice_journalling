# Telegram Voice Journal - Product Brief

## Current Functionality
- Telegram bot that receives voice notes
- Transcribes voice notes using Whisper API
- Returns transcription to the user
- Send transcriptions to Claude API for insights with prompt: "Return a short summary of this, and then add some reflection (like a blindspot you think the user has) and question for further reflection"
- Return Claude's insights to user instead of raw transcription
- SQLite database stores all messages

## New Features to Implement

### Core Functionality
- Implement SQLite database to store:
  - User messages (voice note transcriptions)
  - Claude responses
  - Numeric ID for each entry (visible to user)
  - Timestamps

### User Commands
- `/reviewthisweek` - Analyzes all entries from the current week, sends to Claude with prompt: "Here are some journal messages from a user. Please summarise them, noting any connections between the messages, and give some reflection back"
- `/reviewtoday` - Same as above but only for today's entries
- `/start` - Welcome message explaining how to use the bot and its features
- `/help` - Comprehensive list of commands and usage instructions

### Additional Features to Consider (Future)
- Error handling for API failures
- `/random` - Retrieve a random past entry for reflection
- `/continued [ID]` - Continue a previous journal entry's theme
- `/search [keyword]` - Find entries containing specific words
- `/delete [ID]` - Allow users to remove specific entries
- Auto-detected emotional tone analysis
- Simple tagging capability for organizing entries

## Technical Requirements
- SQLite database implementation
- Claude API integration
- Proper error handling and recovery
- User data privacy considerations