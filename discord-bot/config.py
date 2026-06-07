import os

DISCORD_BOT_TOKEN = os.environ.get("DISCORD_BOT_TOKEN", "")

# Base directory — always the folder containing this file, regardless of
# where the process is launched from (repo root, discord-bot/, Render, etc.)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Cooldown settings (seconds)
DEFAULT_USER_COOLDOWN = 5
DEFAULT_CHANNEL_COOLDOWN = 3

# Fuzzy match threshold (0-100)
FUZZY_THRESHOLD = 75

# Database file — lives in <bot_dir>/data/database.db
DATABASE_PATH = os.path.join(BASE_DIR, "data", "database.db")

# JSON data files — same folder as the scripts
TRIGGERS_PATH = os.path.join(BASE_DIR, "triggers.json")
RESPONSES_PATH = os.path.join(BASE_DIR, "responses.json")
