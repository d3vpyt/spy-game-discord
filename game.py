""" Spy game discord bot"""
import json
import os
import random

from discord.ext import commands
from discord.ext.commands import bot

bot = commands.Bot(command_prefix='!')


@bot.event
async def on_ready():
    """Defining a variable with game text"""
    print('Bot connected')
    try:
        with open('text-vars.json', 'r') as text_vars:
            bot.text_vars = json.load(text_vars)
    except FileNotFoundError:
        raise SystemExit('No game text file')
    except json.decoder.JSONDecodeError:
        raise SystemExit('File error')


def generation_of_roles(members):
    """Generation of roles and locations"""
    location = random.choice(bot.text_vars['locations'].split('\n'))
    list_roles = [location for _ in range(members)]
    list_roles[0] = 'Шпион'
    random.shuffle(list_roles)
    return list_roles


@bot.command(pass_context=True)
async def spy_rules(ctx):
    """Submitting game rules"""
    await ctx.author.send(bot.text_vars['regulations'])


@bot.command(pass_context=True)
async def spy_game(ctx):
    """Parsing channel members"""
    members_list = []
    for guild in bot.guilds:
        for channel in guild.channels:
            if channel.name == 'Spy-game':
                for member in channel.members:
                    members_list.append(member)
    if members_list:
        roles = generation_of_roles(len(members_list))
        """Sending game data"""
        for ind, member in enumerate(members_list):
            await member.send(f"{bot.text_vars['locations']} \nДанная локация: {roles[ind]}")
    else:
        await ctx.send('Всем участникам необходимо находится в комнате Spy-game')


try:
    bot.run(os.getenv('BOT_TOKEN'))
except AttributeError:
    raise SystemExit('Not found BOT_TOKEN')
