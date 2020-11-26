import mechanicalsoup
import json
import discord
import configparser
from random import randrange
from random import randint
from random import choice

"""Easy to use Discord bot.
A Discord bot that takes ...
Requires a token input in config.ini.
  
"""
API_URL = 'https://api.datamuse.com/words?sp='

CONFIG_FILE_PATH = 'config/config.ini'

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

    if message.content.startswith(PREFIX + "word like radovan"):
        url = API_URL + 'radovan'
        browser = mechanicalsoup.Browser()
        response = browser.get(url)
        data = json.loads(response.text)
        print(data)
        random_num = randrange(len(data))
        random_word = data[random_num]['word']     
        await message.channel.send(random_word)
    
    if message.content.startswith(PREFIX + "help"):
        await message.channel.send("""Currently Rad-Bot supports the following commands: 
        !version, !words like radovan
        """)

    if message.content.startswith(PREFIX + "version"):
        await message.channel.send("1.1.0")        
  
def main():
    client.run(config.get('SERVER', 'Token'))
    on_ready()

if __name__ == '__main__':
    main()