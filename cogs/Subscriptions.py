import discord
from discord.ext import commands, tasks
from itertools import cycle
import random
import config
import json


class Subscription(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Adds BananaBot's server ids to subscriptions.json
    @commands.Cog.listener()
    async def on_ready(self):
        self._initializeJson()
        print('Subscriptions activated.')

    @commands.command(aliases=['cSub'])
    @commands.guild_only()
    async def createSubscription(self, ctx, sub_name):
        # TODO: error check file opening
        json_file = self._loadJsonFile()
        server_id = str(ctx.guild.id)
        if server_id in json_file:
            sub_dict = json_file[server_id]
            if sub_name in sub_dict:
                await ctx.send(f'Subscription \'{sub_name}\' already exists. Please choose a different name.')
                return
            else:
                sub_dict[sub_name] = []
        else:
            json_file[server_id] = {sub_name: []}

        self._writeToJson(json_file)
        await ctx.send(f'Subscription  \'{sub_name}\' successfully created.')



    @commands.command(aliases=['rSub'])
    @commands.guild_only()
    async def removeSubscription(self, ctx, sub_name):
        # TODO: error check file opening
        json_file = self._loadJsonFile()
        server_id = str(ctx.guild.id)
        if server_id in json_file:
            sub_dict = json_file[server_id]
            if sub_name in sub_dict:
                sub_dict.pop(sub_name)
            else:
                await ctx.send(f'Subscription \'{sub_name}\' does not exist.')
        else:
            await ctx.send(f'Subscriptions not initialized, call ,,create <subscription name>.')

        self._writeToJson(json_file)
        await ctx.send(f'Subscription  \'{sub_name}\' successfully removed.')

    @commands.command()
    @commands.guild_only()
    async def subscribe(self, ctx, sub_name):
        json_file = self._loadJsonFile()
        server_id = str(ctx.guild.id)
        if server_id in json_file:
            sub_dict = json_file[server_id]
            if sub_name in sub_dict:
                sub_dict[sub_name].append(str(ctx.author.id))
            else:
                await ctx.send(f'Subscription \'{sub_name}\' does not exist, call ,,create \'{sub_name}\' first.')
        else:
            await ctx.send(f'Subscriptions not initialized, call ,,create <subscription name>.')

        self._writeToJson(json_file)
        await ctx.send(f'Subscribed to \'{sub_name}\' successfully.')

    @commands.command()
    @commands.guild_only()
    async def unsubscribe(self, ctx, sub_name):
        json_file = self._loadJsonFile()
        server_id = str(ctx.guild.id)
        if server_id in json_file:
            sub_dict = json_file[server_id]
            if sub_name in sub_dict:
                sub_dict[sub_name].remove(str(ctx.author.id))
            else:
                await ctx.send(f'Subscription \'{sub_name}\' does not exist.')
        else:
            await ctx.send(f'Subscriptions not initialized, call ,,create <subscription name>.')

        self._writeToJson(json_file)
        await ctx.send(f'Unsubscribed from \'{sub_name}\' successfully.')

    @commands.command()
    @commands.guild_only()
    async def listSubscriptions(self, ctx):
        json_file = self._loadJsonFile()
        server_id = str(ctx.guild.id)
        if server_id not in json_file:
            return
        sub_dict = json_file[server_id]
        message = f"{ctx.guild.name} subscriptions:\n"
        for sub_name in sub_dict.keys():
            message += f'    - {sub_name}\n'

        await ctx.send(message)

    @commands.command()
    @commands.guild_only()
    async def atSubscriptions(self, ctx, sub_name):
        json_file = self._loadJsonFile()
        server_id = str(ctx.guild.id)

        if server_id in json_file:
            sub_dict = json_file[server_id]
            if sub_name in sub_dict:
                user_ids = sub_dict[sub_name]
                users = [await ctx.guild.fetch_member(i) for i in user_ids]

                message = f"Calling all {sub_name} members!\n"
                for user in users:
                    message += f'{user.mention} '
                await ctx.send(message)
            else:
                await ctx.send(f'Subscription \'{sub_name}\' does not exist.')
        else:
            await ctx.send(f'Subscriptions not initialized, call ,,create <subscription name>.')

    @commands.command()
    @commands.guild_only()
    async def listSubscribers(self, ctx, sub_name):
        json_file = self._loadJsonFile()
        server_id = str(ctx.guild.id)

        if server_id in json_file:
            sub_dict = json_file[server_id]
            if sub_name in sub_dict:
                user_ids = sub_dict[sub_name]
                users = [await ctx.guild.fetch_member(i) for i in user_ids]

                message = f"{sub_name} members:\n"
                for user in users:
                    message += f'    - {user.name}\n'
                await ctx.send(message)
            else:
                await ctx.send(f'Subscription \'{sub_name}\' does not exist.')
        else:
            await ctx.send(f'Subscriptions not initialized, call ,,create <subscription name>.')

    @commands.command()
    @commands.guild_only()
    async def listSubscribed(self, ctx):
        json_file = self._loadJsonFile()
        server_id = str(ctx.guild.id)
        message = "Subscribed:\n"

        if server_id in json_file:
            sub_dict = json_file[server_id]
            for sub in sub_dict:
                if str(ctx.author.id) in sub_dict[sub]:
                    message += f"    - {sub}\n"
        else:
            await ctx.send(f'Subscriptions not initialized, call ,,create <subscription name>.')
        await ctx.send(message)

    def _initializeJson(self):
        json_file = self._loadJsonFile()
        for server in self.client.guilds:
            server_id = str(server.id)
            if server_id not in json_file:
                json_file[server_id] = {}

        self._writeToJson(json_file)

    def _loadJsonFile(self):
        file = open("./cogs/subscription/subscriptions.json", mode='r')
        json_file = json.load(file)
        file.close()
        return json_file

    def _writeToJson(self, json_file):
        file = open("./cogs/subscription/subscriptions.json", mode='w')
        json.dump(json_file, file, indent=4)
        file.close()

def setup(client):
    client.add_cog(Subscription(client))
