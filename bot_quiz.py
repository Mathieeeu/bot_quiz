import os
import discord
from discord.ext import commands
import sqlite3
import time
import random

intents = discord.Intents.default()
intents.message_content = True

client = commands.Bot(command_prefix='!', intents=intents)
condition = ""
question_type = ""
boucle = False
channel = None
precedent = ""

def connexion_db(sqlite_select_Query):
    try :
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(BASE_DIR, "db_bot_quiz.db")
        conn = sqlite3.connect(db_path)
    except sqlite3.Error as e:
        print(e)
    c = conn.cursor()
    #execution de la requéte
    c.execute(sqlite_select_Query)
    row=c.fetchone() #ne renvoie qu'un seul résultat
    conn.close()
    return row

def simp(text):
    text = text.lower()
    text = text.replace("é","e")
    text = text.replace("è","e")
    text = text.replace("ê","e")
    text = text.replace("ë","e")
    text = text.replace("à","a")
    text = text.replace("â","a")
    text = text.replace("ä","a")
    text = text.replace("ô","o")
    text = text.replace("ö","o")
    text = text.replace("î","i")
    text = text.replace("ï","i")
    text = text.replace("ù","u")
    text = text.replace("û","u")
    text = text.replace("ü","u")
    text = text.replace("ç","c")
    text = text.replace("-","")
    text = text.replace("'","")
    text = text.replace(" ","")
    return text

@client.event
async def on_ready():
    await client.change_presence(activity=discord.activity.CustomActivity(f'boucle = {boucle}'))
    await client.tree.sync()
    print(f'We have logged in as {client.user}')

@client.event
async def on_reaction_add(reaction, user):
    global question_type,_capitale,_difficulte,_pays,_code2,_article,condition,boucle,channel
    if reaction.emoji == "🔍" and reaction.count == 2 and question_type=="capitale":
        await reaction.message.channel.send(embed=discord.Embed(title=f":classical_building: __**Capitale**__ ({_difficulte})",description=f":flag_{_code2}: La bonne réponse était : **{_capitale}**", color=discord.Color.blue()))
        await reaction.message.clear_reactions()
        question_type = ""
        if boucle == True:
            question_type = "capitale"
            await reaction.message.channel.send("Chargement de la prochaine question...\n‎")
            time.sleep(1)
            #relance la commande !capitale automatiquement
            row = connexion_db(f"select * from pays{condition} ORDER BY RANDOM()")
            _pays = row[0]
            _capitale = row[6]
            _code2 = row[2].lower()
            if row[4]=="le": _article = "du "
            elif row[4]=="la": _article = "de la "
            elif row[4]=="les": _article = "des "
            elif row[4]=="l'": _article = "de l'"
            else: 
                if _pays[0] in "aeiouy":
                    _article = "d'"
                else:
                    _article = "de "
            if row[7]==1: _difficulte = "facile"
            elif row[7]==2: _difficulte = "moyen"
            elif row[7]==3: _difficulte = "difficile"
            elif row[7]==4: _difficulte = "impossible"
            embed = discord.Embed(title=f":classical_building: __**Capitale**__ ({_difficulte})",description=f":flag_{_code2}: Quelle est la capitale {_article}**{_pays.capitalize()}** ?", color=discord.Color.pink())
            new_msg = await reaction.message.channel.send(embed=embed)
            await new_msg.add_reaction("🔍")
    elif reaction.emoji == "🔍" and reaction.count == 2 and question_type=="pays":
        await reaction.message.channel.send(embed=discord.Embed(title=f":map: __**Pays**__ ({_difficulte})",description=f":flag_{_code2}: La bonne réponse était : **{_pays}**", color=discord.Color.blue()))
        await reaction.message.clear_reactions()
        question_type = ""
        if boucle == True:
            question_type = "pays"
            await reaction.message.channel.send("Chargement de la prochaine question...\n‎")
            time.sleep(1)
            #relance la commande !capitale automatiquement
            row = connexion_db(f"select * from pays{condition} ORDER BY RANDOM()")
            _pays = row[0]
            _capitale = row[6]
            _code2 = row[2].lower()
            if row[4]=="le": _article = "du "
            elif row[4]=="la": _article = "de la "
            elif row[4]=="les": _article = "des "
            elif row[4]=="l'": _article = "de l'"
            else: 
                if _pays[0] in "aeiouy":
                    _article = "d'"
                else:
                    _article = "de "
            if row[7]==1: _difficulte = "facile"
            elif row[7]==2: _difficulte = "moyen"
            elif row[7]==3: _difficulte = "difficile"
            elif row[7]==4: _difficulte = "impossible"
            embed = discord.Embed(title=f":map: __**Pays**__ ({_difficulte})",description=f"Quel pays a pour capitale **{_capitale.capitalize()}** ?", color=discord.Color.pink())
            new_msg = await reaction.message.channel.send(embed=embed)
            await new_msg.add_reaction("🔍")

@client.event
async def on_message(message):
    global question_type,_capitale,_difficulte,_pays,_code2,_article,condition,boucle,channel
    if message.author == client.user:
        return
    elif message.content.startswith("!help"):
        await message.delete()
        if question_type == "":
            embed = discord.Embed(title=":notepad_spiral: Aide",
                                description=f"Commandes disponibles :\n"
                                                    f"**!ping** : Affiche le ping du bot\n"
                                                    f"**!help** : Affiche l'aide\n"
                                                    f"**!capitale** : Envoie une question \"capitale\", il est possible de préciser la difficulté (1-4) et le continent (EU,AM,AS,AF,OC)\n",
                                color=discord.Color.purple())
        elif question_type == "capitale":
            embed = discord.Embed(title=":notepad_spiral: Aide - Quiz capitales",
                    description=f"Commandes disponibles :\n"
                                        f"**!boucle** : Active/désactive le mode boucle\n"
                                        f"**!help** : Affiche l'aide\n"
                                        f"**!ff** : Abandonne la question et arrête la boucle\n"
                                        f"**!hint** : Donne un indice\n",
                    color=discord.Color.purple())
        await message.channel.send(embed=embed)

    elif message.content.startswith("!hint"):
        """
        format de la commande : !hint
        révele une lettre aléatoire de la capitale
        """
        await message.delete()
        if question_type == "capitale":
            await message.channel.send(f"lettre aléatoire : {random.choice(_capitale)}")

    elif message.content.startswith("!boucle"):
        """
        format de la commande : !boucle
        -> change la valeur de la variable boucle (True ou False)
        """
        await message.delete()
        boucle = not boucle
        await client.change_presence(activity=discord.activity.CustomActivity(f'boucle = {boucle}'))

    elif question_type == "capitale" and channel == message.channel:
            if simp(message.content) == simp(_capitale):

                await message.channel.send(embed=discord.Embed(title=f":classical_building: __**Capitale**__ ({_difficulte})",description=f":flag_{_code2}: {message.author.display_name} a trouvé la bonne réponse !", color=discord.Color.green()))
                await message.add_reaction("✅")
                question_type = ""
                if boucle == True:
                    question_type = "capitale"
                    await channel.send("Chargement de la prochaine question...\n‎")
                    time.sleep(1)
                    #relance la commande !capitale automatiquement
                    row = connexion_db(f"select * from pays{condition} ORDER BY RANDOM()")
                    _pays = row[0]
                    _capitale = row[6]
                    _code2 = row[2].lower()
                    if row[4]=="le": _article = "du "
                    elif row[4]=="la": _article = "de la "
                    elif row[4]=="les": _article = "des "
                    elif row[4]=="l'": _article = "de l'"
                    else: 
                        if _pays[0] in "aeiouy":
                            _article = "d'"
                        else:
                            _article = "de "
                    if row[7]==1: _difficulte = "facile"
                    elif row[7]==2: _difficulte = "moyen"
                    elif row[7]==3: _difficulte = "difficile"
                    elif row[7]==4: _difficulte = "impossible"
                    embed = discord.Embed(title=f":classical_building: __**Capitale**__ ({_difficulte})",description=f":flag_{_code2}: Quelle est la capitale {_article}**{_pays.capitalize()}** ?", color=discord.Color.pink())
                    new_msg = await channel.send(embed=embed)
                    await new_msg.add_reaction("🔍")

            elif message.content == "!ff" or message.content == "!pass" or message.content == "!exit":
                await message.channel.send(embed=discord.Embed(title=f":classical_building: __**Capitale**__ ({_difficulte})",description=f":flag_{_code2}: La bonne réponse était : **{_capitale}**", color=discord.Color.red()))
                question_type = ""
            elif message.content == "!boucle":
                await message.delete()
                boucle = not boucle
                await client.change_presence(activity=discord.activity.CustomActivity(f'boucle = {boucle}'))
            else:
                await message.add_reaction("❌")

    elif message.content.startswith("!capitale") or message.content.startswith("!cap") and question_type == "":
        """
        format de la commande : !capitale [difficulte] [continent] ou !capitale [difficulte] ou !capitale [continent]
        """
        channel = message.channel
        condition = ""
        if not message.content.endswith("!capitale") and not message.content.endswith("!cap"):
            cmd = message.content.split(" ")
            if len(cmd) == 3:
                if cmd[1].isdigit():
                    difficulte = cmd[1]
                    continent = cmd[2]
                else:
                    difficulte = cmd[2]
                    continent = cmd[1]
            elif len(cmd) == 2:
                if cmd[1].isdigit():
                    difficulte = cmd[1]
                    continent = "ALL"
                else:
                    difficulte = "1234"
                    continent = cmd[1]
            condition = " where "
            if continent.upper() == "ALL":
                condition += ""
            elif continent.upper() == "EU":
                condition += "continent='EU'"
            elif continent.upper() == "AS":
                condition += "continent='AS'"
            elif continent.upper() == "AF":
                condition += "continent='AF'"
            elif continent.upper() == "AM":
                condition += "continent='AM'"
            elif continent.upper() == "OC":
                condition += "continent='OC'"
            if continent.upper() != "ALL" and difficulte != "1234":
                condition += " and "
            if difficulte == "1":
                condition += "difficulte=1"
            elif difficulte == "2":
                condition += "difficulte=2"
            elif difficulte == "3":
                condition += "difficulte=3"
            elif difficulte == "4":
                condition += "difficulte=4"
            elif difficulte == "12":
                condition += "(difficulte=1 or difficulte=2)"
            elif difficulte == "123":
                condition += "(difficulte=1 or difficulte=2 or difficulte=3)"
            elif difficulte == "23":
                condition += "(difficulte=2 or difficulte=3)"
            elif difficulte == "234":
                condition += "(difficulte=2 or difficulte=3 or difficulte=4)"
            elif difficulte == "34":
                condition += "(difficulte=3 or difficulte=4)"
            elif difficulte == "1234" or "\n":
                condition += ""
        #print(f"select * from pays {condition} ORDER BY RANDOM()")
        row = connexion_db(f"select * from pays{condition} ORDER BY RANDOM()")

        _pays = row[0]
        _capitale = row[6]
        _code2 = row[2].lower()
        if row[4]=="le": _article = "du "
        elif row[4]=="la": _article = "de la "
        elif row[4]=="les": _article = "des "
        elif row[4]=="l'": _article = "de l'"
        else: 
            if _pays[0] in "aeiouy":
                _article = "d'"
            else:
                _article = "de "
        if row[7]==1: _difficulte = "facile"
        elif row[7]==2: _difficulte = "moyen"
        elif row[7]==3: _difficulte = "difficile"
        elif row[7]==4: _difficulte = "impossible"
        question_type = "capitale"

        await message.delete()
        await message.channel.send("‎\n‎")
        embed = discord.Embed(title=f":classical_building: __**Capitale**__ ({_difficulte})",description=f":flag_{_code2}: Quelle est la capitale {_article}**{_pays.capitalize()}** ?", color=discord.Color.pink())
        new_msg = await message.channel.send(embed=embed)
        await new_msg.add_reaction("🔍")

    elif message.content.startswith("!pays") or message.content.startswith("!p") and question_type == "":
        """
        format de la commande : !pays [difficulte] [continent] ou !pays [difficulte] ou !pays [continent]
        """
        channel = message.channel
        condition = ""
        if not message.content.endswith("!pays") and not message.content.endswith("!p"):
            cmd = message.content.split(" ")
            if len(cmd) == 3:
                if cmd[1].isdigit():
                    difficulte = cmd[1]
                    continent = cmd[2]
                else:
                    difficulte = cmd[2]
                    continent = cmd[1]
            elif len(cmd) == 2:
                if cmd[1].isdigit():
                    difficulte = cmd[1]
                    continent = "ALL"
                else:
                    difficulte = "1234"
                    continent = cmd[1]
            condition = " where "
            if continent.upper() == "ALL":
                condition += ""
            elif continent.upper() == "EU":
                condition += "continent='EU'"
            elif continent.upper() == "AS":
                condition += "continent='AS'"
            elif continent.upper() == "AF":
                condition += "continent='AF'"
            elif continent.upper() == "AM":
                condition += "continent='AM'"
            elif continent.upper() == "OC":
                condition += "continent='OC'"
            if continent.upper() != "ALL" and difficulte != "1234":
                condition += " and "
            if difficulte == "1":
                condition += "difficulte=1"
            elif difficulte == "2":
                condition += "difficulte=2"
            elif difficulte == "3":
                condition += "difficulte=3"
            elif difficulte == "4":
                condition += "difficulte=4"
            elif difficulte == "12":
                condition += "(difficulte=1 or difficulte=2)"
            elif difficulte == "123":
                condition += "(difficulte=1 or difficulte=2 or difficulte=3)"
            elif difficulte == "23":
                condition += "(difficulte=2 or difficulte=3)"
            elif difficulte == "234":
                condition += "(difficulte=2 or difficulte=3 or difficulte=4)"
            elif difficulte == "34":
                condition += "(difficulte=3 or difficulte=4)"
            elif difficulte == "1234" or "\n":
                condition += ""
        #print(f"select * from pays {condition} ORDER BY RANDOM()")
        row = connexion_db(f"select * from pays{condition} ORDER BY RANDOM()")
        _pays = row[0]
        _capitale = row[6]
        _code2 = row[2].lower()
        if row[4]=="le": _article = "du "
        elif row[4]=="la": _article = "de la "
        elif row[4]=="les": _article = "des "
        elif row[4]=="l'": _article = "de l'"
        else: 
            if _pays[0] in "aeiouy":
                _article = "d'"
            else:
                _article = "de "
        if row[7]==1: _difficulte = "facile"
        elif row[7]==2: _difficulte = "moyen"
        elif row[7]==3: _difficulte = "difficile"
        elif row[7]==4: _difficulte = "impossible"
        question_type = "pays"
        await message.delete()
        await message.channel.send("‎\n‎")
        embed = discord.Embed(title=f":map:  __**Pays**__ ({_difficulte})",description=f"Quel pays a pour capitale **{_capitale.capitalize()}** ?", color=discord.Color.pink())
        new_msg = await message.channel.send(embed=embed)
        await new_msg.add_reaction("🔍")

    elif question_type == "pays" and channel == message.channel:
        if simp(message.content) == simp(_pays):
            await message.channel.send(embed=discord.Embed(title=f":map: __**Pays**__ ({_difficulte})",description=f":flag_{_code2}: {message.author.display_name} a trouvé la bonne réponse !", color=discord.Color.green()))
            await message.add_reaction("✅")
            question_type = ""
            if boucle == True:
                question_type = "pays"
                await channel.send("Chargement de la prochaine question...\n‎")
                time.sleep(1)
                #relance la commande !capitale automatiquement
                row = connexion_db(f"select * from pays{condition} ORDER BY RANDOM()")
                _pays = row[0]
                _capitale = row[6]
                _code2 = row[2].lower()
                if row[4]=="le": _article = "du "
                elif row[4]=="la": _article = "de la "
                elif row[4]=="les": _article = "des "
                elif row[4]=="l'": _article = "de l'"
                else: 
                    if _pays[0] in "aeiouy":
                        _article = "d'"
                    else:
                        _article = "de "
                if row[7]==1: _difficulte = "facile"
                elif row[7]==2: _difficulte = "moyen"
                elif row[7]==3: _difficulte = "difficile"
                elif row[7]==4: _difficulte = "impossible"
                embed = discord.Embed(title=f":map: __**Pays**__ ({_difficulte})",description=f"Quel pays a pour capitale **{_capitale.capitalize()}** ?", color=discord.Color.pink())
                new_msg = await channel.send(embed=embed)
                await new_msg.add_reaction("🔍")
        elif message.content == "!ff" or message.content == "!pass" or message.content == "!exit":
            await message.channel.send(embed=discord.Embed(title=f":map: __**Pays**__ ({_difficulte})",description=f":flag_{_code2}: La bonne réponse était : **{_pays}**", color=discord.Color.red()))
            question_type = ""
        elif message.content == "!boucle":
            await message.delete()
            boucle = not boucle
            await client.change_presence(activity=discord.activity.CustomActivity(f'boucle = {boucle}'))
        else:
            await message.add_reaction("❌")

    elif message.content.startswith("!ping") and question_type == "":
        """
        format de la commande : !ping
        -> affiche le ping du bot
        """
        await message.delete()
        bot_latency = round(client.latency*1000)
        embed = discord.Embed(title=":ping_pong: Pong !",description=f"Latence du bot : {bot_latency}ms", color=discord.Color.red())
        await message.channel.send(embed = embed)


# On récupère notre token discord dans l'env de Railway
bot_token = os.environ.get("DISCORD_BOT_TOKEN")

# Pour lancer le bot
client.run(bot_token)
