from discord.ext import commands
from config import settings
from config import ilyusURL
import logging

from Game import *

#Логгер
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')

#Бот
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.presences = True
bot = commands.Bot(command_prefix = settings['prefix'], intents=intents)
game = Game(bot)

def getOnlineList(guild):
    onlineList = ''
    memberIndex = 0
    for member in guild.members:
        if member.status == discord.Status.online:
            memberIndex += 1
            onlineList += f'\n{memberIndex}. {member.global_name} ({member.name})'

    #onlineList = f'Online ({memberIndex}/{guild.member_count})' + onlineList
    return onlineList

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

    for guild in bot.guilds:
        print(f'\nGuild name: {guild.name}, count: {guild.member_count}')
        try:
            for ind, member in enumerate(guild.members):
                print(f'{ind + 1}. {member.global_name} ({member.name})')
            print('\n')
        except:
            pass
        print(getOnlineList(guild))

@bot.command()
async def online(ctx):
    embed = discord.Embed(title='Онлайн', description=getOnlineList(ctx.guild), color=0xffff00)
    await ctx.send(embed=embed)

@bot.command()
async def hello(ctx):
    author = ctx.message.author
    await ctx.send(f'Привет, {author.mention}!')

@bot.command()
@commands.has_permissions(administrator = True)
async def start(ctx):
    ch = bot.get_channel(gameChannels['lobbyVoiceChannelID']) #лобби
    await ctx.send(f'Игра запущена')
    await ctx.send(f'На данный момент в лобби ' + str(len(ch.members)) + ' игроков')
    await game.checkLobbyLoop.start()

@bot.command(description="Отправляет противную фотографию")#Локальный мем
async def пенис(ctx):
    embed = discord.Embed(color=0xff9900, title='Ильюс наблевал')  # Создание Embed'a
    embed.set_image(url=ilyusURL)
    await ctx.send(embed=embed)

bot.run(settings['token'], log_handler=handler, log_level=logging.DEBUG)

