import discord
from discord.ext import commands
from discord import app_commands
import os
import datetime

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"Logged in as {bot.user}")

# /mimic command
@bot.tree.command(name="mimic", description="Bot repeats the given text")
@app_commands.describe(text="Text to mimic", no_tracker="Hide who used the command?")
async def mimic(interaction: discord.Interaction, text: str, no_tracker: bool = False):
    if isinstance(interaction.user, discord.Member):
        member = interaction.user
        has_mimicker_role = any(role.name == "Ultimate Mimicker" for role in member.roles)

        if no_tracker and has_mimicker_role:
            await interaction.response.send_message("Mimicry was a success", ephemeral=True)
            await interaction.followup.send(text)
        else:
            await interaction.response.send_message(f"{interaction.user.display_name} said: {text}")
    else:
        await interaction.response.send_message("Error: Unable to retrieve user roles.", ephemeral=True)

# /icbp command
@bot.tree.command(name="icbp", description="Launch an intercontinental ballistic penguin")
@app_commands.checks.has_role("Penguin Launcher")
async def icbp(interaction: discord.Interaction):
    await interaction.response.send_message("Do you really want the dodo gone? (yes/no)")

# /icbm command
@bot.tree.command(name="icbm", description="Launch a nuclear bomb")
@app_commands.checks.has_role("Nuclear Bomb Launcher")
async def icbm(interaction: discord.Interaction):
    await interaction.response.send_message("@everyone INTERCONTINENTAL BALLISTIC MISSILE INBOUND COMING TOWARDS [IP_REDACTED]")

# /atomicbeam command (untouched as requested)
@bot.tree.command(name="atomicbeam", description="Evaporate someone with atomic breath")
@app_commands.checks.has_role("Royal Blood Dragon")
@app_commands.describe(victim="User to evaporate")
async def atomicbeam(interaction: discord.Interaction, victim: discord.Member):
    await victim.timeout(datetime.timedelta(hours=1), reason="Evaporated by atomic breath")
    await interaction.response.send_message(
        f"{victim.mention} was evaporated by atomic breath\nhttps://tenor.com/view/godzilla-godzilla-sp-godzilla-singular-point-godzilla-ultima-gif-21863614"
    )

# Error handling for role checks
@bot.tree.error
async def on_app_command_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    if isinstance(error, app_commands.MissingRole):
        await interaction.response.send_message(
            f"You need the '{error.missing_role}' role to use this command.",
            ephemeral=True
        )
    else:
        await interaction.response.send_message(
            "An error occurred while processing the command.",
            ephemeral=True
        )

bot.run(os.environ["TOKEN"])
