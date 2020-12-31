import asyncio
import discord
from discord.ext import commands
import os
import configparser
from jsonProcessor import *
intents = discord.Intents.default()
intents.members = True
intents.guilds = True
intents.messages = True
intents.dm_messages = True
intents.emojis = True
intents.guild_messages = True
intents.all()

cogs = ["first"]
TOKEN = "NzM2NDM4NjY5NTUxOTkyOTM2.Xxuz9Q.bqK2zosQXpEewxrvlwWOrgTFl8k"

client = commands.Bot(command_prefix = ".", owner_ids = (181125548389433344 , 97502897012490240), intents=intents)

if __name__ == "__main__":
    client.cake = cake
    for ex in cogs:
        try:
            client.load_extension(ex)
            print(f"Loaded {ex}")
        except Exception as error:
            print(error, error.__class__)
    print(client.extensions)
    client.run(TOKEN)
