import random

import discord
from discord.ext import commands, tasks
from discord.utils import get

import config
from config import PREFIX


class Tools(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.description = "Collection of utilities"

    @commands.Cog.listener()
    async def on_ready(self):
        self.random_status.start()
        print('Tools activated.')

    @commands.command(brief="Ping Banana",
                      description="Ping Banana")
    async def ping(self, ctx):
        await ctx.send(f'Pong! {round(self.client.latency * 1000)}')

    @commands.command(aliases=['mc', 'conch'],
                      brief="Ask a yes or no question to the magic conch",
                      description="Ask a yes or no question to the magic conch",
                      usage=",,mc QUESTION")
    async def magic_conch(self, ctx, *, question):
        responses = config.responses
        await ctx.send(random.choice(responses))

    @magic_conch.error
    async def magic_conch_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Usage: ",,mc <yes/no question>"')

    @commands.command(brief="Clear recent message",
                      description="Clear recent messages",
                      usage=f"{PREFIX}clear NUM")
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount=5):
        if amount > 0:
            await ctx.channel.purge(limit=amount)

    @commands.command(brief="Sends a picture of a banana",
                      description="Sends a picture of a banana")
    async def banana(self, ctx):
        banana = discord.Embed()
        banana.set_image(url='http://weknowyourdreams.com/images/banana/banana-02.jpg')
        await ctx.send(embed=banana)

    @commands.command(aliases=['dice'],
                      brief="Roll a dice",
                      description="Roll a dice",
                      usage=f"{PREFIX}roll NUM")
    async def roll(self, ctx, lower=1, upper=6):
        await ctx.send(random.randint(int(lower), int(upper)))

    @tasks.loop(seconds=20)
    async def random_status(self):
        status = f'{next(config.bot_statuses)} | {PREFIX}help'
        await self.client.change_presence(activity=discord.Game(status))


def setup(client):
    client.add_cog(Tools(client))
