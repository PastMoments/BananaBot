import random

import discord
from discord.ext import commands, tasks

import config


class Tools(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        self.random_status.start()
        print('Tools activated.')

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f'Pong! {round(self.client.latency * 1000)}')

    @commands.command(aliases=['mc', 'conch'])
    async def magic_conch(self, ctx, *, question):
        responses = config.responses
        await ctx.send(random.choice(responses))

    @magic_conch.error
    async def magic_conch_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Incorrect usage.\n'
                           'Correct usage: ",,mc <yes/no question>"')

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount=5):
        if amount > 0:
            await ctx.channel.purge(limit=amount)

    def _loadgisinfo(self):
        with open('./gis') as file:
            api_key = file.readline()
            cx = file.readline()
        return api_key, cx

    # Sends an image of a random banana
    # TODO: test
    @commands.command()
    async def banana(self, ctx):
        banana = discord.Embed()
        banana.set_image(url='http://weknowyourdreams.com/images/banana/banana-02.jpg')
        await ctx.send(embed=banana)

    @commands.command()
    async def hi(self, ctx):
        await ctx.send(f'Hello {ctx.author.mention}, I am Banana Bot!')

    @commands.command(aliases=['dice'])
    async def roll(self, ctx, lower=1, upper=6):
        await ctx.send(random.randint(int(lower), int(upper)))

    @tasks.loop(seconds=20)
    async def random_status(self):
        status = f'{next(config.bot_statuses)} | ,,help'
        await self.client.change_presence(activity=discord.Game(status))


def setup(client):
    client.add_cog(Tools(client))
