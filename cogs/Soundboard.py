import discord
from discord.ext import commands, tasks
from discord.utils import get
import asyncio
#import config
import os
import re

# TODO: test
class SoundBoard(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('SoundBoard activated.')


    @commands.command()
    @commands.guild_only()
    async def listSounds(self, ctx, *args):
        # this gives a wonky path if args is like "path/to/directory" rather than "path to directory", need check
        path = '/'.join(args)
        msg = self.rlistSounds(path)
        if msg is None:
            await ctx.send("Sorry, I couldn't find your path")
            return
        await ctx.send(msg)


    """
    Given a path relative to ./cogs/soundboard/, return a formatted message displaying all subdirectories and files
    recursively
    """
    def rlistSounds(self, path, depth=0):
        root = './cogs/soundboard/'
        rel = os.path.join(root, path)
        if not os.path.exists(rel):
            return None
        msg = ''
        for item in os.listdir(rel):
            rel_item_path = os.path.join(rel, item)
            if os.path.isdir(rel_item_path):
                msg += f"{'  ' * depth}/{item}\n"
                msg += self.rlistSounds(os.path.join(path, item), depth=depth+1)
            else:
                regex = '([^.]*).[^.]*'
                basename = os.path.basename(rel_item_path)
                match = re.search(regex, basename)
                if match is not None:
                    msg += f"{'  ' * depth}-{match.group(1)}\n"
        return msg

    @commands.command(aliases=['sb', 'sound'])
    @commands.guild_only()
    async def soundboard(self, ctx, *args):
        path = '/'.join(args)
        root = './cogs/Soundboard/'
        relpath = os.path.join(root, f'{path}.mp3')
        if not os.path.exists(relpath):
            await ctx.send("Couldn't find the sound.")
            return

        voice = ctx.guild.voice_client
        author = ctx.author
        channel = author.voice.channel

        # Possibly change to have it stay after it plays a sound
        def leave(err):
            asyncio.run_coroutine_threadsafe(voice.disconnect(),
                                             self.client.loop)

        if not os.path.isfile(relpath):
            await ctx.send("Sorry, I couldn't find your sound.")
            return

        if voice and voice.channel and not voice.is_playing():
            voice.play(discord.FFmpegPCMAudio(relpath), after=leave)
            voice.source = discord.PCMVolumeTransformer(voice.source)
            voice.source.volume = 1
        elif author.voice is not None and author.voice.channel is not None:
            voice = await channel.connect()
            voice.play(discord.FFmpegPCMAudio(relpath), after=leave)
            voice.source = discord.PCMVolumeTransformer(voice.source)
            voice.source.volume = 1


def setup(client):
    client.add_cog(SoundBoard(client))
