import os
import asyncio
import discord
from discord import app_commands
from dotenv import load_dotenv

load_dotenv()

class IlieBot(discord.Client):
    def __init__(self):
        intents = discord.Intents.default()
        intents.guilds = True
        intents.guild_messages = True
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

client = IlieBot()

TARGET_ROLE_NAME = "Membru"

@client.event
async def on_ready():
    print(f"🔒 Ilie ruleaza acum cu BLOCARE RAPIDA pe roluri! 🐍👑")

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
        role = discord.utils.get(interaction.guild.roles, name=TARGET_ROLE_NAME)
        everyone_role = interaction.guild.default_role
        
        tasks = []

        if role:
            perms = discord.Permissions(role.permissions.value)
            perms.update(send_messages=False)
            tasks.append(role.edit(permissions=perms, reason="IlieBot Lockdown Executed"))
            
        everyone_perms = discord.Permissions(everyone_role.permissions.value)
        everyone_perms.update(send_messages=False)
        tasks.append(everyone_role.edit(permissions=everyone_perms, reason="IlieBot Lockdown Executed"))
        
        await asyncio.gather(*tasks)
        
        await interaction.followup.send(
            f"🚨🚨 **Lockdown total executat!** Rolul '{TARGET_ROLE_NAME}' si '@everyone' au fost dezactivate global!\n"
            f"*Notă: Utilizatorii pot vorbi în continuare în canalele cu permisiuni specifice (Channel Overwrites) setate explicit pe 'True'.*"
        )
    except discord.Forbidden:
        await interaction.followup.send("Nu am permisiuni suficiente! Asigură-te că rolul botului este deasupra rolurilor modificate.")
    except Exception as e:
        print(f"Eroare lockdown roluri: {e}")
        await interaction.followup.send("Nu am putut modifica rolurile globale.")

@client.tree.command(name="unlockdown", description="Porneste permisiunea de scris inapoi pe ambele roluri!")
@app_commands.default_permissions(administrator=True)
async def unlockdown(interaction: discord.Interaction):
    await interaction.response.defer()
    try:
        role = discord.utils.get(interaction.guild.roles, name=TARGET_ROLE_NAME)
        everyone_role = interaction.guild.default_role
        
        tasks = []

        if role:
            perms = discord.Permissions(role.permissions.value)
            perms.update(send_messages=True)
            tasks.append(role.edit(permissions=perms, reason="IlieBot Unlockdown Executed"))
            
        everyone_perms = discord.Permissions(everyone_role.permissions.value)
        everyone_perms.update(send_messages=True)
        tasks.append(everyone_role.edit(permissions=everyone_perms, reason="IlieBot Unlockdown Executed"))
        
        await asyncio.gather(*tasks)
        
        await interaction.followup.send(f"🔓 **Misiune indeplinita! Ambele roluri pot scrie din nou global!** 🔓")
    except discord.Forbidden:
        await interaction.followup.send("Eroare de permisiune! Verifică ierarhia rolurilor din server.")
    except Exception as e:
        print(f"Eroare unlockdown roluri: {e}")
        await interaction.followup.send("Am esuat deblocarea rolurilor globale.")

client.run(os.getenv("DISCORD_TOKEN"))
