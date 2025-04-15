import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
import os
# // Python 是什麼 78  語言
from typing import Optional

load_dotenv()

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
intents.guilds = True

bot = commands.Bot(command_prefix='/', intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name="with 2FA codes"))
    try: 
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands")
    except:
        print(f'Error syncing commands')

@bot.tree.command(name="2fa-admin", description="This is the command where you can get your Guild's public 2FA codes")
@app_commands.default_permissions(administrator=True)
# Use str for entering a string. NOT discord.text duhh
async def tfa_admin(interaction: discord.Interaction, name: str):
    await interaction.response.defer(ephemeral=True)
    
    await interaction.followup.send(name)

@bot.tree.command(name="2fa", description="This allows your a member of this guild to access a set of 2FA keys that the Admins allows.")
@app_commands.default_permissions()
async def tfa_users(interaction: discord.Interaction, name: str):
    await interaction.response.defer(ephemeral=True)
    await interaction.followup.send(name)


@bot.tree.command(name="2fa-create", description="This is where you the admin can create 2FA codes for your guild")
@app_commands.default_permissions(administrator=True)
async def create_2fa(interaction: discord.Interaction, name: str, code: str, admin_only: bool):
    # Use ephemeral=True to point out that only the sender haves the message.
    await interaction.response.defer(ephemeral=True)

    await interaction.followup.send(f'Name: {name}, Code: {code}, AdminOnly: {admin_only}')

@bot.tree.command(name="setlog", description="Setup logs for Admins")
@app_commands.default_permissions(administrator=True)
async def setlog(interaction: discord.Interaction, channel: Optional[discord.TextChannel] = None):
    await interaction.response.defer(ephemeral=True)
    await interaction.followup.send(f'{channel | "N/A"}')


bot.run(os.getenv("TOKEN"))