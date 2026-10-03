import os
import asyncio
import discord
from discord import app_commands
from dotenv import load_dotenv
from flask import Flask
from threading import Thread

load_dotenv()

app = Flask('')

@app.route('/')
def home():
    return "Ilie Bot is running flawlessly in the cloud 24/7!"

def run_web_server():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run_web_server)
    t.start()

class IlieBot(discord.Client):
    def __init__(self):
        intents = discord.Intents.default()
        intents.guilds = True
        intents.guild_messages = True
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

client = IlieBot()

EXCLUDED_CHANNELS = ["regulament", "reguli", "anunturi", "announcements", "welcome"]

@client.event
async def on_ready():
    print(f"🔒 {client.user} s-a trezit si e ONLINE in Python! 🐍🔥")

@client.event
async def on_message(message: discord.Message):
    if message.author.bot:
        return
    if message.content == "!sync" and message.author.id == 1237335057513971763:
        print("Sincronizare comenzi slash...")
        await client.tree.sync()
        await message.channel.send("Comenzile slash au fost aliniate global!")

@client.tree.command(name="lockdown", description="Opreste permisiunea de scris pe rolul Membru si @everyone global!")
@app_commands.default_permissions(administrator=True)
async def lockdown(interaction: discord.Interaction):
    await interaction.response.defer()
    try:
        role = discord.utils.get(interaction.guild.roles, name="Membru")
        everyone_role = interaction.guild.default_role
        tasks = []
        if role:
            perms = discord.Permissions(role.permissions.value)
            perms.update(send_messages=False)
            tasks.append(role.edit(permissions=perms, reason="IlieBot Lockdown Executed"))
        everyone_perms = discord.Permissions(everyone_role.permissions.value)
        everyone_permissions.update(send_messages=False)
        tasks.append(everyone_role.edit(permissions=everyone_permissions, reason="IlieBot Lockdown Executed"))
        await asyncio.gather(*tasks)
        await interaction.followup.send("🚨🚨 **Lockdown total executat global!** 🚨🚨")
    except discord.Forbidden:
        await interaction.followup.send("Nu am permisiuni suficiente!")
    except Exception as e:
        print(f"Eroare lockdown: {e}")
        await interaction.followup.send("Nu am putut modifica rolurile.")

@client.tree.command(name="unlockdown", description="Porneste permisiunea de scris inapoi pe ambele roluri!")
@app_commands.default_permissions(administrator=True)
async def unlockdown(interaction: discord.Interaction):
    await interaction.response.defer()
    try:
        role = discord.utils.get(interaction.guild.roles, name="Membru")
        everyone_role = interaction.guild.default_role
        tasks = []
        if role:
            perms = discord.Permissions(role.permissions.value)
            perms.update(send_messages=True)
            tasks.append(role.edit(permissions=perms, reason="IlieBot Unlockdown Executed"))
        everyone_perms = discord.Permissions(everyone_role.permissions.value)
        everyone_perms.update(send_messages=True)
        tasks.append(everyone_role.edit(permissions=everyone_permissions, reason="IlieBot Unlockdown Executed"))
        await asyncio.gather(*tasks)
        await interaction.followup.send("🔓 **Misiune indeplinita! Ambele roluri pot scrie din nou global!** 🔓")
    except discord.Forbidden:
        await interaction.followup.send("Eroare de permisiune!")
    except Exception as e:
        print(f"Eroare unlockdown: {e}")
        await interaction.followup.send("Am esuat deblocarea rolurilor.")

keep_alive()
client.run(os.getenv("DISCORD_TOKEN"))
