import discord
from discord.ext import commands
import json
import logging, sys, re, time, asyncio

from BotMakerExceptions import *



def init_logger():
    global logger
    formatter = logging.Formatter(
        '[(%(asctime)s) (%(module)s:%(lineno)s) : %(levelname)s] "%(message)s"'
    )
    logger = logging.getLogger(name="tw_logger")
    logger.setLevel(logging.DEBUG)

    streamhandler = logging.StreamHandler(sys.stdout)
    streamhandler.setLevel(logging.DEBUG)
    streamhandler.setFormatter(formatter)
    logger.addHandler(streamhandler)

    filehandler = logging.FileHandler(r"logs/Main.log")
    filehandler.setLevel(logging.DEBUG)
    filehandler.setFormatter(formatter)
    logger.addHandler(filehandler)

    filehandler = logging.FileHandler(r"logs/all.log")
    filehandler.setLevel(logging.DEBUG)
    filehandler.setFormatter(formatter)
    logger.addHandler(filehandler)

    return logger
class Main(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.logger = init_logger()


    @commands.Cog.listener()
    async def on_message(self, message):
        message = message
        self.commands = json.load(open("commands.json", "r"))
        if message.author.id == self.client.user.id: return
        ctx = await self.client.get_context(message)
        for x in self.commands:
            if str(message.content).split(" ")[0] == x:
                cake = self.client.cake(ctx, x, self)
                if str(message.content).split(" ")[0] not in cake.events:
                    await cake.processCommands()

    @commands.Cog.listener()
    async def on_ready(self):
        self.commands = json.load(open("commands.json", "r"))
        if "on_ready" in self.commands:
            await self.client.cake(None, "on_ready", self).processCommands()

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        self.commands = json.load(open("commands.json", "r"))
        if "on_message_delete" in self.commands:
            await self.client.cake(None, "on_message_delete", self, message=message).processCommands()


def setup(client):
    client.add_cog(Main(client))
