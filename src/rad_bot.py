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

# helper functions
def fetch_data(api_url, plain_text):
    url = api_url + plain_text
    response = BROWSER.get(url)
    data = json.loads(response.text)
    return data

def get_random_word(data):
    random_num = randrange(len(data))
    random_word = data[random_num]['word']
    return random_word

# globals
SOUND_LIKE_RADOVAN_DATA = fetch_data(SOUND_LIKE_API_URL, 'radovan')
SOUND_LIKE_RADO_DATA = fetch_data(SOUND_LIKE_API_URL, 'rado')
SOUND_LIKE_RAD_DATA = fetch_data(SOUND_LIKE_API_URL, 'rad')

RHYME_WITH_RADOVAN_DATA = fetch_data(SOUND_LIKE_API_URL, 'radovan')
RHYME_WITH_RADO_DATA = fetch_data(SOUND_LIKE_API_URL, 'rado')
RHYME_WITH_RAD_DATA = fetch_data(SOUND_LIKE_API_URL, 'rad')

# discord stuff
@client.event
async def on_ready():
    print(f"We have logged in as {client.user}.")

@client.event
async def on_message(message):
    if message.author == client.user:
        return 

    if message.content.lower().startswith(PREFIX + "help"):
        await message.channel.send(" Rad Bot currently supports the following commands:\n" \
                                    "!help\t!version\t!source code\n" \
                                    "!sound\tlike radovan\t!sound like rado\t!sound like rad\n" \
                                    "!rhyme with radovan\t!rhyme with rado\t!rhyme with rad\n" \
                                    "!rad meme"
                                    )

    if message.content.lower().startswith(PREFIX + "version"):
        await message.channel.send("1.11.2")  

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
        await message.channel.send(get_random_word(SOUND_LIKE_RADOVAN_DATA))
    if message.content.lower() == (PREFIX + "sound like rado"):
        await message.channel.send(get_random_word(SOUND_LIKE_RADO_DATA))
    if message.content.lower() == (PREFIX + "sound like rad"):
        await message.channel.send(get_random_word(SOUND_LIKE_RAD_DATA))
        
    if message.content.lower() == (PREFIX + "rhyme with radovan"):
        await message.channel.send(get_random_word(RHYME_WITH_RADOVAN_DATA))
    if message.content.lower() == (PREFIX + "rhyme with rado"):
        await message.channel.send(get_random_word(RHYME_WITH_RADO_DATA))
    if message.content.lower() == (PREFIX + "rhyme with rad"):
        await message.channel.send(get_random_word(RHYME_WITH_RAD_DATA))

# entry to program
def main():
    client.run(CONFIG.get('SERVER', 'Token'))
    on_ready()

if __name__ == '__main__':
    main()