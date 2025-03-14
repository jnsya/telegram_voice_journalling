# Telegram AI Voice Journalling Bot

A Telegram bot that automatically transcribes voice messages using OpenAI's Whisper model and provides reflective insights using Claude AI.

## Features

- Receives voice messages from Telegram users
- Transcribes audio using OpenAI's Whisper (runs locally)
- Generates reflective insights using Claude AI:
  - Concise summary of your voice note
  - Identification of potential blindspots
  - Thoughtful questions for further reflection
- Stores message history in a local database
- Provides commands to review, retrieve, and manage past entries
- Replies with both the AI-generated insights and original transcription
- Simple authentication to restrict usage to authorized users
- Simple setup and configuration using Docker

## Requirements

- Docker installed on your system ([Install Docker](https://docs.docker.com/get-docker/))
- A Telegram account (to create a bot)
- An Anthropic API key for Claude ([Get API Key](https://console.anthropic.com/))

## Quick Setup

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/telegram_voice_journalling.git
cd telegram_voice_journalling
```

### 2. Create a Telegram bot

1. Open Telegram and search for [@BotFather](https://t.me/BotFather)
2. Start a chat and send the command `/newbot`
3. Follow the instructions to create your bot
   - Provide a name for your bot
   - Provide a username for your bot (must end with 'bot')
4. BotFather will give you a token - copy this for the next step

### 3. Configure the bot

Create a `.env` file in the project directory:

```bash
# Create and open the .env file
cp .env.example .env
```

Replace the placeholder values with your actual credentials:
- `your_telegram_bot_token_here`: The token you received from BotFather
- `your_telegram_user_id_here`: Your Telegram user ID (find it by messaging [@userinfobot](https://t.me/userinfobot))
- `your_anthropic_api_key_here`: Your Anthropic API key for Claude

This will restrict the bot to only respond to your messages.

### 4. Build and run with Docker

```bash
# Build the Docker image
docker build -t telegram-voice-bot .

# Run the container
docker run --env-file .env -v $(pwd)/messages.db:/app/messages.db telegram-voice-bot

# Mount your local code directory to see changes without rebuilding:
docker run --env-file .env -v $(pwd):/app telegram-voice-bot
```

Note: The `-v $(pwd)/messages.db:/app/messages.db` option ensures that your message database persists between container restarts.

That's it! Your bot is now running and ready to transcribe voice messages and provide reflective insights.

## Usage

### Basic Usage

1. Open Telegram and search for your bot using its username
2. Start a chat with your bot
3. Send a voice message to your bot
4. The bot will:
   - Transcribe your audio
   - Generate reflective insights using Claude
   - Reply with both the insights and original transcription
   - Store the message in its database with a reference ID

### Commands

The bot supports the following commands:

- `/start` - Introduction and list of available commands
- `/history [n]` - Show your last n entries (default 5)
- `/entry MSG123` - Show a specific entry by reference ID
- `/weekly` - Show all entries from the past week
- `/random` - Show a random entry from your history
- `/delete MSG123` - Delete a specific entry by reference ID
- `/review_week` - Get AI summary of your entries from the past week
- `/review_today` - Get AI summary of your entries from today

## How It Works

1. The bot listens for incoming voice messages
2. When a voice message is received, it downloads the audio file
3. The audio is processed using OpenAI's Whisper model (running locally)
4. The transcription is sent to Claude AI with a prompt for reflective analysis
5. Claude generates a summary, identifies potential blindspots, and offers a question
6. The bot stores both the transcription and Claude's response in a SQLite database
7. The bot sends Claude's response along with the original transcription back to the user
8. The temporary audio file is deleted

The bot also provides review functionality:
- `/review_week` analyzes all your entries from the past week, identifying patterns and themes
- `/review_today` summarizes your entries from the current day, offering consolidated insights

## Database

The bot uses a SQLite database to store message history. The database includes:

- Reference ID (e.g., MSG123) for easy retrieval
- User ID to associate messages with specific users
- Original transcription
- Claude's response
- Timestamp
- Audio metadata (length, file ID)

This allows you to review past entries and potentially analyze patterns in your voice notes over time.

## Customization

### Changing the Whisper Model

The bot uses the "tiny" Whisper model by default. You can change this in `config.py`:

```python
# Whisper model configuration
WHISPER_MODEL = "tiny"  # Options: tiny, base, small, medium, large
```

### Changing the Claude Model

The bot uses Claude 3 Haiku by default. You can change this in `config.py`:

```python
# Claude model configuration
CLAUDE_MODEL = "claude-3-haiku-20240307"
```

## Troubleshooting

### Common Issues

1. **Docker not installed**: Make sure Docker is installed and running on your system
2. **Authentication issues**: Verify your Telegram bot token and user ID in the .env file
3. **Claude API errors**: Check your Anthropic API key and ensure you have sufficient quota
4. **Permission errors**: On Linux, you might need to run Docker with sudo
5. **Connection timeout**: Check your internet connection
6. **Database issues**: Ensure the database file is writable by the container

## Alternative Setup (without Docker)

If you prefer not to use Docker, see the [detailed setup instructions](SETUP_WITHOUT_DOCKER.md) for running the bot directly with Python.

## Future Extensions

Planned features for future versions:
- Integration with Obsidian for saving transcriptions as markdown files
- Weekly summaries of all your entries
- Topic clustering and trend analysis
- Custom prompts for different types of reflections

## License

[MIT License](LICENSE)

## Acknowledgements

- [OpenAI Whisper](https://github.com/openai/whisper) for the speech recognition model
- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) for the Telegram API wrapper
- [Anthropic Claude](https://www.anthropic.com/claude) for the AI-powered reflections 