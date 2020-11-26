import os

import discord
import configparser

"""Easy to use reaction Discord bot.
A Discord bot that takes user messages as input and reacts with emotes.
Requires a token input in config.ini.
  
"""
CONFIG_FILE_PATH = 'src//config.ini'

config = configparser.ConfigParser()
config.read(CONFIG_FILE_PATH)

PREFIX = config.get('SERVER', 'Prefix')

client = discord.Client()

@client.event
async def on_ready():
    print(f"We have logged in as {client.user}.")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith(PREFIX + "help"):
        print(f"halp") 
  
def main():
    client.run(config.get('SERVER', 'Token'))
    on_ready()

if __name__ == '__main__':
    main()