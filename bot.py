import os
import asyncio
import discord
from discord import app_commands
from dotenv import load_dotenv
from flask import Flask, jsonify
from flask_cors import CORS
from threading import Thread

load_dotenv()

app = Flask('')
CORS(app)

bot_loop = None

@app.route('/')
def home():
    return "Ilie Bot API is running flawlessly in the cloud 24/7!"

@app.route('/api/lockdown', methods=['POST'])
def api_lockdown():
    if bot_loop and client.is_ready():
        asyncio.run_coroutine_threadsafe(trigger_global_lockdown(True), bot_loop)
        return jsonify({"status": "success", "message": "Lockdown triggered successfully via API!"}), 200
    return jsonify({"status": "error", "message": "Bot is not ready or offline!"}), 500

@app.route('/api/unlockdown', methods=['POST'])
def api_unlockdown():
    if bot_loop and client.is_ready():
        asyncio.run_coroutine_threadsafe(trigger_global_lockdown(False), bot_loop)
        return jsonify({"status": "success", "message": "Unlockdown triggered successfully via API!"}), 200
    return jsonify({"status": "error", "message": "Bot is not ready or offline!"}), 500

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

async def trigger_global_lockdown(lock: bool):
    try:
        for guild in client.guilds:
            role = discord.utils.get(guild.roles, name="Membru")
            everyone_role = guild.default_role
            tasks = []
            
            if role:
                perms = discord.Permissions(role.permissions.value)
                perms.update(send_messages=not lock)
                tasks.append(role.edit(permissions=perms, reason="IlieBot API Control Executed"))
                
            everyone_perms = discord.Permissions(everyone_role.permissions.value)
            everyone_permissions.update(send_messages=not lock)
            tasks.append(everyone_role.edit(permissions=everyone_permissions, reason="IlieBot API Control Executed"))
            
            await asyncio.gather(*tasks)
            print(f"Executat de la distanta: Lockdown={lock} pe serverul {guild.name}")
    except Exception as e:
        print(f"Eroare executie API Discord: {e}")

@client.event
async def on_ready():
    global bot_loop
    bot_loop = asyncio.get_running_loop()
    print(f"🔒 {client.user} s-a trezit si e ONLINE in Cloud! 🐍🔥")

keep_alive()
client.run(os.getenv("DISCORD_TOKEN"))
