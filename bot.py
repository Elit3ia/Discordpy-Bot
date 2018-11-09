# module imports
import discord
from discord.ext import commands
from rivescript import RiveScript
import asyncio
#import hangman
#import hangBot
import dbQueries
import re
import conversation
import sys, traceback
TOKEN = 'NTA0NjYwOTQ5OTcwNzE0NjQ1.DrJuWA.qYYoCL_xGOI_FB8UQBb1YyeBSCk'

bot = commands.Bot(command_prefix='!')

client = discord.Client()
rs = RiveScript()
rs.load_directory("../ChatBot/RiveFiles", ext=".rive")
rs.sort_replies()

@bot.command()
async def info(client, *, member: discord.Member):
    fmt = '{0} joined on {0.joined_at} and has {1} roles.'
    await client.send(fmt.format(member, len(member.roles)))

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_message(message):
    userID = message.author.id
    dbQueries.initialise(userID,rs)
    stringInp = message.content   
    
    async def onNotification(sender, text):
        print(text)
        await client.send_message(message.channel, "Test %s" % text)
    
    
    
    if "[notification]" in str(message):
        await client.send_message(message.channel, message)
    
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return
           
    if stringInp[0] == '!':
        reObj = re.match('!\w* *', stringInp)
        if reObj:
            stringAction = "{}".format(reObj.group(0))
            stringInp = stringInp.replace(stringAction,"")
            stringAction = stringAction.replace(" ", "")
    
    output = conversation.keywordToModule(rs.reply("localuser", stringInp), stringInp,rs, userID, client, onNotification)
    await client.send_message(message.channel, output)
    
# @bot.command()
# async def weather()

client.run(TOKEN)
asyncio.run(main())
