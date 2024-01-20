import os
import discord
from discord.ext import commands
from discord import Interaction

intents = discord.Intents.default()
intents.message_content = True

client = commands.Bot(intents=discord.Intents.all(), command_prefix='/')
global question_type
question_type = ""

@client.event
async def on_ready():
    await client.change_presence(activity=discord.activity.CustomActivity('/help'))
    await client.tree.sync()
    print(f'We have logged in as {client.user}')

@client.tree.command(name="ping",description="Affiche le ping du bot")
async def ping(interaction : Interaction):
    bot_latency = round(client.latency*1000)
    embed = discord.Embed(title=":ping_pong: Pong !",description=f"Latence du bot : {bot_latency}ms", color=discord.Color.red())
    await interaction.response.send_message(embed = embed)

@client.tree.command(name="help",description="Affiche l'aide")
async def help(interaction : Interaction):
    embed = discord.Embed(title=":notepad_spiral: Aide",
                          description=f"Commandes disponibles :\n"
                                            f"**/ping** : Affiche le ping du bot\n"
                                            f"**/help** : Affiche l'aide\n"
                                            f"**/capitale** : Envoie une question \"capitale\"\n",
                          color=discord.Color.purple())
    await interaction.response.send_message(embed = embed)

@client.tree.command(name="capitale",description="Envoie une question \"capitale\"")
async def capitale(interaction : Interaction):
    global question_type,_capitale,_difficulte
    _articles = "de la"
    _pays = "france"
    _capitale = "paris"
    _difficulte = "facile"
    question_type = "capitale"
    #créer un embed avec la question
    embed = discord.Embed(title=f":classical_building: __**Capitale**__ ({_difficulte})",description=f"Quelle est la capitale {_articles} **{_pays.capitalize()}** ?", color=discord.Color.green())
    await interaction.response.send_message(embed=embed)

@client.event
async def on_message(message):
    global question_type,_capitale,_difficulte
    if message.author == client.user:
        return

    if question_type == "capitale":
        if message.content.lower() == _capitale:
            await message.channel.send(embed=discord.Embed(title=f"__**Capitale**__ ({_difficulte})",description=f"{message.author.display_name} a trouvé la bonne réponse !", color=discord.Color.green()))
            await message.add_reaction("✅")
            question_type = ""
        else:
            await message.add_reaction("❌")

# On récupère notre token discord dans l'env de Railway
bot_token = os.environ.get("DISCORD_BOT_TOKEN")
bot_token = "MTE5Nzk4MzQwMjM5NDEyNDMxOA.GWJzzg.QTPZzhHbJY_Fhpj65ySH80JVYFuCFtCvWvT-NE"
# Pour lancer le bot
client.run(bot_token)
