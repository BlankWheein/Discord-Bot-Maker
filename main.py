import asyncio
import discord
from discord.ext import commands
import os
import configparser
import ctypes
os.chdir(os.path.dirname(__file__))

cogs = ["first"]
TOKEN = "NzM2NDM4NjY5NTUxOTkyOTM2.Xxuz9Q.bqK2zosQXpEewxrvlwWOrgTFl8k"

client = commands.Bot(command_prefix = ".", owner_ids = (181125548389433344 , 97502897012490240))
ctypes.windll.kernel32.SetConsoleTitleA("BotMaker")

if __name__ == "__main__":
    for ex in cogs:
        try:
            client.load_extension(ex)
            print(f"Loaded {ex}")
        except Exception as error:
            print(error, error.__class__)
    print(client.extensions)
    client.run(TOKEN)
