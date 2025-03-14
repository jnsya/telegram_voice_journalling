# Setting Up Without Docker

This guide explains how to set up and run the Telegram Voice Transcription Bot directly with Python, without using Docker.

## Requirements

- Python 3.8 or higher
- FFmpeg (required for audio processing)
- A Telegram account (to create a bot)

## Installation Steps

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
# Edit the file and add your bot token and user ID
echo "TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here" > .env
echo "AUTHORIZED_USER_ID=your_telegram_user_id_here" >> .env
```

Replace `your_telegram_bot_token_here` with the token you received from BotFather.

To find your Telegram user ID:
1. Send a message to [@userinfobot](https://t.me/userinfobot) on Telegram
2. The bot will reply with your user ID
3. Add this ID to your .env file as AUTHORIZED_USER_ID

### 6. Run the bot

```bash
python voice_bot.py
```

## Troubleshooting

### Common Issues

1. **"No module named 'faster_whisper'"**: Make sure you've installed all dependencies with `pip install -r requirements.txt`
2. **FFmpeg errors**: Ensure FFmpeg is installed correctly on your system
3. **Connection timeout**: Check your internet connection and verify your bot token is correct
4. **NumPy compatibility issues**: If you encounter NumPy errors, try `pip install numpy==1.26.4` to downgrade to a compatible version 