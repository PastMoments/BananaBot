import os

import discord
from discord.ext import commands

import config

client = commands.Bot(command_prefix=config.PREFIX)


# Gives debug feedback that the bot has successfully launched.
@client.event
async def on_ready():
    print(f'Logged in as\n{client.user.name}\n{client.user.id}\n------')
    await client.change_presence(status=discord.Status.online)


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send('Invalid command used.')


# Loading cogs from the subdirectory
def loadCogs():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            client.load_extension(f'cogs.{filename[:-3]}')


@client.command(aliases=['rel', 'rl'], hidden=True)
async def reload(ctx, extension):
    try:
        client.unload_extension(f'cogs.{extension}')
        client.load_extension(f'cogs.{extension}')
        await ctx.send(f'{extension} reloaded.')
    except Exception as e:
        await ctx.send(e)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    loadCogs()
    client.run(config.token)

