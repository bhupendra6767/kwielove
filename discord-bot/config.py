import os

DISCORD_BOT_TOKEN = os.environ.get("DISCORD_BOT_TOKEN", "")

# Cooldown settings (seconds)
DEFAULT_USER_COOLDOWN = 5
DEFAULT_CHANNEL_COOLDOWN = 3

# Fuzzy match threshold (0-100)
FUZZY_THRESHOLD = 75

# Database file
DATABASE_PATH = "discord-bot/database.db"

# JSON data files
TRIGGERS_PATH = "discord-bot/triggers.json"
RESPONSES_PATH = "discord-bot/responses.json"
