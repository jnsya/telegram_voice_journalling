# Telegram Voice Transcription Bot

A Telegram bot that automatically transcribes voice messages using OpenAI's Whisper model.

## Features

- Receives voice messages from Telegram users
- Transcribes audio using OpenAI's Whisper (runs locally)
- Replies with the transcribed text
- Simple authentication to restrict usage to authorized users
- Simple setup and configuration using Docker

## Requirements

- Docker installed on your system ([Install Docker](https://docs.docker.com/get-docker/))
- A Telegram account (to create a bot)

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
touch .env
# Edit the file and add your bot token and user ID
echo "TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here" > .env
echo "AUTHORIZED_USER_ID=your_telegram_user_id_here" >> .env
```

Replace `your_telegram_bot_token_here` with the token you received from BotFather.

To find your Telegram user ID:
1. Send a message to [@userinfobot](https://t.me/userinfobot) on Telegram
2. The bot will reply with your user ID
3. Add this ID to your .env file as AUTHORIZED_USER_ID

This will restrict the bot to only respond to your messages.

### 4. Build and run with Docker

```bash
# Build the Docker image
docker build -t telegram-voice-bot .

# Run the container
docker run --env-file .env telegram-voice-bot

# Mount your local code directory to see changes without rebuilding:
docker run --env-file .env -v $(pwd):/app telegram-voice-bot
```

That's it! Your bot is now running and ready to transcribe voice messages.

## Usage

1. Open Telegram and search for your bot using its username
2. Start a chat with your bot
3. Send a voice message to your bot
4. The bot will transcribe the audio and reply with the text


## How It Works

1. The bot listens for incoming voice messages
2. When a voice message is received, it downloads the audio file
3. The audio is processed using OpenAI's Whisper model (running locally)
4. The transcribed text is sent back to the user
5. The temporary audio file is deleted

## Customization

### Changing the Whisper Model

The bot uses the "tiny" Whisper model by default. You can change this to a larger model for better accuracy (at the cost of more resources):

```python
# In voice_bot.py, change:
model = WhisperModel("tiny", device="cpu", compute_type="int8")

# To one of these options (in increasing order of accuracy and resource usage):
model = WhisperModel("base", device="cpu", compute_type="int8")
model = WhisperModel("small", device="cpu", compute_type="int8")
model = WhisperModel("medium", device="cpu", compute_type="int8")
model = WhisperModel("large", device="cpu", compute_type="int8")
```

## Troubleshooting

### Common Issues

1. **Docker not installed**: Make sure Docker is installed and running on your system
2. **Authentication issues**: Verify your Telegram bot token and user ID in the .env file
3. **Permission errors**: On Linux, you might need to run Docker with sudo
4. **Connection timeout**: Check your internet connection

## Alternative Setup (without Docker)

If you prefer not to use Docker, see the [detailed setup instructions](SETUP_WITHOUT_DOCKER.md) for running the bot directly with Python.

## Future Extensions

Planned features for future versions:
- Integration with Obsidian for saving transcriptions as markdown files
- Summaries using Claude API
- Metadata support (timestamps, categories)

## License

[MIT License](LICENSE)

## Acknowledgements

- [OpenAI Whisper](https://github.com/openai/whisper) for the speech recognition model
- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) for the Telegram API wrapper 