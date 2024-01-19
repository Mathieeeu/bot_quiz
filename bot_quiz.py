import os
import discord
from discord import app_commands as apc

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

tree = apc.CommandTree(client)

@tree.command(
    name="hello",
    description="Say hello to the bot",
)
async def hello(interaction):
    await interaction.response.send_message("Hello!")

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!hello'):
        await message.channel.send(message.content)
        
# On récupère notre token discord dans l'env de Railway
bot_token = os.environ.get("DISCORD_BOT_TOKEN")

# Pour lancer le bot
client.run(bot_token)
