# Telegram Voice Transcription Bot

A Telegram bot that automatically transcribes voice messages using OpenAI's Whisper model.

## Features

- Receives voice messages from Telegram users
- Transcribes audio using OpenAI's Whisper (runs locally on your machine)
- Replies with the transcribed text
- Simple setup and configuration

## Requirements

- Python 3.8 or higher
- FFmpeg (required for audio processing)
- A Telegram account (to create a bot)

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/telegram_voice_journalling.git
cd telegram_voice_journalling
```

### 2. Create a virtual environment

```bash
# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate
```

### 3. Install dependencies

```bash
# Install required Python packages
pip install -r requirements.txt

# Install FFmpeg (required for audio processing)
# On macOS with Homebrew:
brew install ffmpeg
# On Ubuntu/Debian:
# sudo apt-get install ffmpeg
# On Windows, download from https://ffmpeg.org/download.html
```

### 4. Create a Telegram bot

1. Open Telegram and search for [@BotFather](https://t.me/BotFather)
2. Start a chat and send the command `/newbot`
3. Follow the instructions to create your bot
   - Provide a name for your bot
   - Provide a username for your bot (must end with 'bot')
4. BotFather will give you a token - copy this for the next step

### 5. Configure the bot

Create a `.env` file in the project directory:

```bash
# Create and open the .env file
touch .env
# Edit the file and add your bot token
echo "TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here" > .env
```

Replace `your_telegram_bot_token_here` with the token you received from BotFather.

## Usage

1. Make sure your virtual environment is activated
2. Run the bot:

```bash
python voice_bot.py
```

3. Open Telegram and search for your bot using its username
4. Start a chat with your bot
5. Send a voice message to your bot
6. The bot will transcribe the audio and reply with the text

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
model = whisper.load_model("tiny")

# To one of these options (in increasing order of accuracy and resource usage):
model = whisper.load_model("base")
model = whisper.load_model("small")
model = whisper.load_model("medium")
model = whisper.load_model("large")
```

## Troubleshooting

### Common Issues

1. **"No module named 'whisper'"**: Make sure you've installed all dependencies with `pip install -r requirements.txt`
2. **FFmpeg errors**: Ensure FFmpeg is installed correctly on your system
3. **Connection timeout**: Check your internet connection and verify your bot token is correct
4. **NumPy compatibility issues**: If you encounter NumPy errors, try `pip install numpy==1.26.4` to downgrade to a compatible version

## Future Extensions

Planned features for future versions:
- Server deployment options
- Integration with Obsidian for saving transcriptions as markdown files
- Summaries using Claude API
- Metadata support (timestamps, categories)

## License

[MIT License](LICENSE)

## Acknowledgements

- [OpenAI Whisper](https://github.com/openai/whisper) for the speech recognition model
- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) for the Telegram API wrapper 