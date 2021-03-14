import discord
from discord.ext import commands, tasks
from discord.utils import get
import asyncio
import config
import os


class SoundBoard(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('SoundBoard activated.')

    @commands.command()
    @commands.guild_only()
    async def listSounds(self, ctx):
        soundboard = './cogs/soundboard'
        # TODO: implement
        for root, d_names, f_names in os.walk(soundboard):
            if len(d_names) == 0:
                # TODO: print all the f_names
                print(f_names)

    @commands.command(aliases=['sb', 'sound'])
    @commands.guild_only()
    async def soundboard(self, ctx, *args):
        collection = args[0]
        sound = args[1]
        path = f'./cogs/Soundboard/{collection}/{sound}.mp3'
        voice = ctx.guild.voice_client
        author = ctx.author
        channel = author.voice.channel

        def leave(err):
            asyncio.run_coroutine_threadsafe(voice.disconnect(),
                                             self.client.loop)

        if not os.path.isfile(path):
            return

        if voice and voice.channel and not voice.is_playing():
            voice.play(discord.FFmpegPCMAudio(path), after=leave)
            voice.source = discord.PCMVolumeTransformer(voice.source)
            voice.source.volume = 1
        elif author.voice is not None and author.voice.channel is not None:
            voice = await channel.connect()
            voice.play(discord.FFmpegPCMAudio(path), after=leave)
            voice.source = discord.PCMVolumeTransformer(voice.source)
            voice.source.volume = 1


def setup(client):
    client.add_cog(SoundBoard(client))
