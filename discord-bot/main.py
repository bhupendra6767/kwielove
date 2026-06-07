"""
main.py — Discord bot: automatic chat responses only.
"""

import asyncio
import os
import time
import discord
from discord import app_commands
from discord.ext import commands

from config import (
    DISCORD_BOT_TOKEN,
    DEFAULT_USER_COOLDOWN,
    DEFAULT_CHANNEL_COOLDOWN,
)
from database import (
    init_db,
    set_channel_enabled,
    is_channel_enabled,
    get_enabled_channels,
    get_guild_settings,
    set_cooldown,
)
from responder import Responder

# ---------------------------------------------------------------------------
# Bot setup
# ---------------------------------------------------------------------------

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="\x00", intents=intents)  # null prefix = no prefix commands

responder = Responder()

# ---------------------------------------------------------------------------
# Cooldown tracking  {user_id: last_timestamp}  {channel_id: last_timestamp}
# ---------------------------------------------------------------------------
_user_last: dict[int, float] = {}
_channel_last: dict[int, float] = {}
_last_responses: dict[int, str] = {}  # channel_id → last bot response (anti-duplicate)


# ---------------------------------------------------------------------------
# Events
# ---------------------------------------------------------------------------

@bot.event
async def on_ready():
    await init_db()
    responder.load()
    try:
        synced = await bot.tree.sync()
        print(f"[Bot] Logged in as {bot.user} | Synced {len(synced)} slash commands")
    except Exception as e:
        print(f"[Bot] Failed to sync commands: {e}")


@bot.event
async def on_message(message: discord.Message):
    # Ignore bots
    if message.author.bot:
        return

    # Ignore slash commands
    if message.content.startswith("/"):
        return

    # Must be in a guild
    if not message.guild:
        return

    channel_id = message.channel.id
    guild_id = message.guild.id
    user_id = message.author.id

    # Check if channel is enabled
    if not await is_channel_enabled(channel_id):
        return

    # Fetch guild settings for cooldowns
    settings = await get_guild_settings(guild_id)
    user_cd = settings["user_cooldown"]
    channel_cd = settings["channel_cooldown"]

    now = time.monotonic()

    # Per-user cooldown
    if now - _user_last.get(user_id, 0) < user_cd:
        return

    # Per-channel cooldown
    if now - _channel_last.get(channel_id, 0) < channel_cd:
        return

    # Get a response
    response = responder.get_response(message.content)
    if response is None:
        return

    # Anti-duplicate: skip if same response was just sent in this channel
    if _last_responses.get(channel_id) == response:
        # Try to get a different one (up to 5 attempts)
        for _ in range(5):
            response = responder.get_response(message.content)
            if response and response != _last_responses.get(channel_id):
                break
        else:
            return

    # Update cooldown timestamps
    _user_last[user_id] = now
    _channel_last[channel_id] = now
    _last_responses[channel_id] = response

    await message.channel.send(response)


# ---------------------------------------------------------------------------
# Slash Commands
# ---------------------------------------------------------------------------

def is_admin():
    async def predicate(interaction: discord.Interaction) -> bool:
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message(
                "❌ You need **Administrator** permission to use this command.",
                ephemeral=True
            )
            return False
        return True
    return app_commands.check(predicate)


@bot.tree.command(name="enablechannel", description="Enable auto responses in the current channel.")
@is_admin()
async def enablechannel(interaction: discord.Interaction):
    await set_channel_enabled(interaction.guild_id, interaction.channel_id, True)
    await interaction.response.send_message(
        f"✅ Auto responses **enabled** in {interaction.channel.mention}",
        ephemeral=False
    )


@bot.tree.command(name="disablechannel", description="Disable auto responses in the current channel.")
@is_admin()
async def disablechannel(interaction: discord.Interaction):
    await set_channel_enabled(interaction.guild_id, interaction.channel_id, False)
    await interaction.response.send_message(
        f"🔇 Auto responses **disabled** in {interaction.channel.mention}",
        ephemeral=False
    )


@bot.tree.command(name="listchannels", description="Show all channels where auto responses are enabled.")
@is_admin()
async def listchannels(interaction: discord.Interaction):
    channel_ids = await get_enabled_channels(interaction.guild_id)
    if not channel_ids:
        await interaction.response.send_message(
            "📋 No channels have auto responses enabled yet.\nUse `/enablechannel` in a channel to enable it.",
            ephemeral=True
        )
        return

    lines = []
    for cid in channel_ids:
        ch = interaction.guild.get_channel(cid)
        if ch:
            lines.append(f"• {ch.mention}")
        else:
            lines.append(f"• `#{cid}` *(channel not found)*")

    embed = discord.Embed(
        title="📋 Channels with Auto Responses Enabled",
        description="\n".join(lines),
        color=discord.Color.green()
    )
    await interaction.response.send_message(embed=embed, ephemeral=True)


@bot.tree.command(name="setcooldown", description="Set response cooldown times (in seconds).")
@is_admin()
@app_commands.describe(
    user_seconds="Per-user cooldown in seconds (default: 5)",
    channel_seconds="Per-channel cooldown in seconds (default: 3)"
)
async def setcooldown(
    interaction: discord.Interaction,
    user_seconds: float = 5.0,
    channel_seconds: float = 3.0,
):
    if user_seconds < 0 or channel_seconds < 0:
        await interaction.response.send_message("❌ Cooldown values must be 0 or greater.", ephemeral=True)
        return
    if user_seconds > 3600 or channel_seconds > 3600:
        await interaction.response.send_message("❌ Cooldown values cannot exceed 3600 seconds (1 hour).", ephemeral=True)
        return

    await set_cooldown(interaction.guild_id, user_seconds, channel_seconds)
    await interaction.response.send_message(
        f"⏱️ Cooldowns updated!\n"
        f"• Per-user: **{user_seconds}s**\n"
        f"• Per-channel: **{channel_seconds}s**",
        ephemeral=True
    )


@bot.tree.command(name="stats", description="Show total triggers and responses loaded.")
async def stats(interaction: discord.Interaction):
    embed = discord.Embed(
        title="📊 Bot Stats",
        color=discord.Color.blurple()
    )
    embed.add_field(name="🎯 Triggers Loaded", value=f"`{responder.trigger_count:,}`", inline=True)
    embed.add_field(name="💬 Responses Loaded", value=f"`{responder.response_count:,}`", inline=True)
    embed.add_field(name="🤖 Bot", value=f"`{bot.user}`", inline=False)
    embed.set_footer(text="Auto response bot — responds naturally to chat messages")
    await interaction.response.send_message(embed=embed)


# ---------------------------------------------------------------------------
# Run
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    if not DISCORD_BOT_TOKEN:
        print("[Error] DISCORD_BOT_TOKEN is not set. Please add it to your environment secrets.")
        exit(1)
    bot.run(DISCORD_BOT_TOKEN)
