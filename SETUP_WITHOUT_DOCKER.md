# Setting Up Without Docker

This guide explains how to set up and run the Telegram Voice Transcription Bot directly with Python, without using Docker.

## Requirements

- Python 3.8 or higher
- FFmpeg (required for audio processing)
- A Telegram account (to create a bot)
- An Anthropic API key for Claude ([Get API Key](https://console.anthropic.com/))

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
# Edit the file and add your bot token, user ID, and Anthropic API key
echo "TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here" > .env
echo "AUTHORIZED_USER_IDS=your_telegram_user_id_here" >> .env
echo "ANTHROPIC_API_KEY=your_anthropic_api_key_here" >> .env
```

Replace the placeholder values with your actual credentials:
- `your_telegram_bot_token_here`: The token you received from BotFather
- `your_telegram_user_id_here`: Your Telegram user ID (find it by messaging [@userinfobot](https://t.me/userinfobot))
- `your_anthropic_api_key_here`: Your Anthropic API key for Claude

### 6. Run the bot

```bash
python voice_bot.py
```

## Database Information

The bot uses a SQLite database (`messages.db`) to store message history. This file will be created automatically in the project directory when you first run the bot.

### Database Structure

The database contains a single table called `messages` with the following columns:

- `id`: Primary key, auto-incrementing
- `reference_id`: User-friendly reference ID (e.g., "MSG123")
- `user_id`: Telegram user ID
- `transcription`: Original transcribed message
- `claude_response`: Claude's response
- `created_at`: When the message was processed
- `audio_length`: Length of the audio in seconds
- `voice_file_id`: Telegram's file ID for the voice message

### Accessing the Database

You can directly access the database using SQLite tools if needed:

```bash
# Using the SQLite command line tool
sqlite3 messages.db

# Then you can run SQL queries, for example:
sqlite> SELECT reference_id, created_at, transcription FROM messages LIMIT 5;
```

### Backing Up the Database

It's a good idea to periodically back up your database:

```bash
# Simple copy backup
cp messages.db messages.db.backup

# Or use SQLite's backup command
sqlite3 messages.db ".backup messages.db.backup"
```

## Troubleshooting

### Common Issues

1. **"No module named 'faster_whisper'"**: Make sure you've installed all dependencies with `pip install -r requirements.txt`
2. **FFmpeg errors**: Ensure FFmpeg is installed correctly on your system
3. **Claude API errors**: Check your Anthropic API key and ensure you have sufficient quota
4. **Connection timeout**: Check your internet connection and verify your bot token is correct
5. **NumPy compatibility issues**: If you encounter NumPy errors, try `pip install numpy==1.26.4` to downgrade to a compatible version
6. **Database errors**: Make sure the directory where the bot is running has write permissions 