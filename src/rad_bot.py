import os
import mechanicalsoup
import json
import discord
from static_config_parser import StaticConfigParser
from random import randrange
from random import choice


"""Easy to use Discord bot.

Rad-Bot posts images from inside a directory and interacts with APIs
to output relevant data.
Requires a token input in config.ini.
"""

# globals
SOUND_LIKE_API_URL = 'https://api.datamuse.com/words?sl='
RHYME_API_URL = 'https://api.datamuse.com/words?rel_rhy='

CONFIG = StaticConfigParser()
PREFIX = CONFIG.get('SERVER', 'Prefix')
IMAGE_PATH =  'images/'

BROWSER = mechanicalsoup.Browser()

client = discord.Client()

# functions
def get_random_word(api_url, plain_text):
    url = api_url + plain_text
    response = BROWSER.get(url)
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

    if message.content.lower().startswith(PREFIX + "version"):
        await message.channel.send("1.8.4")  

    if message.content.lower().startswith(PREFIX + "help"):
        await message.channel.send(" Rad Bot currently supports the following commands:\n" \
                                    "!help  !version  !source code\n" \
                                    "!sound like radovan  !sound like rado  !sound like rad\n" \
                                    "!radovan rhyme  !rado rhyme  !rad rhyme\n" \
                                    "!rad meme"
                                    )

    if message.content.lower().startswith(PREFIX + "source code"):
        await message.channel.send("https://github.com/aminbeigi/Rad-Bot")  

    if message.content.lower() == (PREFIX + "rad meme"):
        image_lst = os.listdir(IMAGE_PATH)
        # try to find .png and .jpg file
        try:
            await message.channel.send(file=discord.File(IMAGE_PATH + choice(image_lst)))
        except (OSError, IOError) as e:
            raise Exception("Couldn't find any files in directory.") from e

    if message.content.lower() == (PREFIX + "sound like radovan"):
        await message.channel.send(get_random_word(SOUND_LIKE_API_URL, 'radovan'))
    if message.content.lower() == (PREFIX + "sound like rado"):
        await message.channel.send(get_random_word(SOUND_LIKE_API_URL, 'rado'))
    if message.content.lower() == (PREFIX + "sound like rad"):
        await message.channel.send(get_random_word(SOUND_LIKE_API_URL, 'rad'))
        
    if message.content.lower() == (PREFIX + "radovan rhyme"):
        await message.channel.send(get_random_word(RHYME_API_URL, 'radovan'))
    if message.content.lower() == (PREFIX + "rado rhyme"):
        await message.channel.send(get_random_word(RHYME_API_URL, 'rado'))
    if message.content.lower() == (PREFIX + "rad rhyme"):
        await message.channel.send(get_random_word(RHYME_API_URL, 'rad'))
    
def main():
    client.run(CONFIG.get('SERVER', 'Token'))
    on_ready()

if __name__ == '__main__':
    main()