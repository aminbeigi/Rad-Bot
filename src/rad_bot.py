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

# globals
SOUND_LIKE_API_URL = 'https://api.datamuse.com/words?sl='
RHYME_API_URL = 'https://api.datamuse.com/words?rel_rhy='


CONFIG_FILE_PATH = 'config/config.ini'

config = configparser.ConfigParser()
config.read(CONFIG_FILE_PATH)

PREFIX = config.get('SERVER', 'Prefix')

browser = mechanicalsoup.Browser()

client = discord.Client()

# functions
def get_random_word(api_url, plain_text):
    url = api_url + plain_text
    response = browser.get(url)
    data = json.loads(response.text)
    random_num = randrange(len(data))
    random_word = data[random_num]['word']
    return random_word

# discord stuff
@client.event
async def on_ready():
    print(f"We have logged in as {client.user}.")

@client.event
async def on_message(message):
    if message.author == client.user:
        return 

    if message.content.startswith(PREFIX + "version"):
        await message.channel.send("1.2.1")  

    if message.content.startswith(PREFIX + "help"):
        await message.channel.send(" Rad Bot currently supports the following commands:\n" \
                                    "!version, !word like radovan/rado/rad, !radovan/rado/rad rhyme")

    if message.content == (PREFIX + "rad meme"):
        await message.channel.send(file=discord.File('images/image2.png'))

    if message.content == (PREFIX + "word like radovan"):
        await message.channel.send(get_random_word(SOUND_LIKE_API_URL, 'radovan'))
    if message.content == (PREFIX + "word like rado"):
        await message.channel.send(get_random_word(SOUND_LIKE_API_URL, 'rado'))
    if message.content == (PREFIX + "word like rad"):

        await message.channel.send(get_random_word(SOUND_LIKE_API_URL, 'rad'))
    if message.content == (PREFIX + "radovan rhyme"):
        await message.channel.send(get_random_word(RHYME_API_URL, 'radovan'))
    if message.content == (PREFIX + "rado rhyme"):
        await message.channel.send(get_random_word(RHYME_API_URL, 'rado'))
    if message.content == (PREFIX + "rad rhyme"):
        await message.channel.send(get_random_word(RHYME_API_URL, 'rad'))
    
def main():
    client.run(config.get('SERVER', 'Token'))
    on_ready()

if __name__ == '__main__':
    main()