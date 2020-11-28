import os
import mechanicalsoup
import json
import discord
from discord.ext import commands
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

def get_image_count():
    return len(os.listdir(IMAGE_PATH))

# globals
SOUND_LIKE_RADOVAN_DATA = fetch_data(SOUND_LIKE_API_URL, 'radovan')
SOUND_LIKE_RADO_DATA = fetch_data(SOUND_LIKE_API_URL, 'rado')
SOUND_LIKE_RAD_DATA = fetch_data(SOUND_LIKE_API_URL, 'rad')

RHYME_WITH_RADOVAN_DATA = fetch_data(SOUND_LIKE_API_URL, 'radovan')
RHYME_WITH_RADO_DATA = fetch_data(SOUND_LIKE_API_URL, 'rado')
RHYME_WITH_RAD_DATA = fetch_data(SOUND_LIKE_API_URL, 'rad')

RAD_BOT_CHANNEL = 667002924886523912

# discord stuff
@client.event
async def on_ready():
    print(f"We have logged in as {client.user}.")

@client.event
async def on_message(message):
    if message.author == client.user:
        return 

    if message.content.lower().startswith(PREFIX + "help"):
        await message.channel.send("!help\t!version\t!source code\t!whats new?\n" \
                                    "!sound like radovan/rado/rad\n" \
                                    "!rhyme with radovan/rado/rad\n" \
                                    "!rad meme\t!how many rad memes?"
                                    )

    if message.content.lower() == (PREFIX + "version"):
        await message.channel.send("2.0.1")  

    if message.content.lower().startswith(PREFIX + "source"):
        await message.channel.send("https://github.com/aminbeigi/Rad-Bot") 

    if message.content.lower().startswith(PREFIX + "whats new"):
        await message.channel.send("You can now private message Rad Bot rad memes.") 

    if message.content.lower().startswith(PREFIX + "how many"):
        await message.channel.send(f"Rad Bot currenlty holds {get_image_count()} rad memes!")

    if message.content.lower() == (PREFIX + "rad meme"):
        image_lst = os.listdir(IMAGE_PATH)
        # raise exception if empty directory OR invalid file format
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

    # await client.process_commands(message)
    if not message.guild:
        try:
            for attachment in message.attachments:
                await attachment.save(f'images/{get_image_count()}_{attachment.filename}') # the file name attachment.filename
            await message.author.send(f"Received imaged, thanks!\nRad Bot currenlty holds {get_image_count()} rad memes.")
            await client.get_channel(RAD_BOT_CHANNEL).send(f"@{message.author} has just submitted a rad meme")
        except (OSError, IOError) as e:
            await message.author.send(f"Woah something went wrong... Please don't do that again :(.")
            raise Exception("Coudln't process the file(?).") from e
    
    # easter egg
    if 'golf' in message.content.lower():
        await message.channel.send(":man_golfing: did someone say golf? :man_golfing:")

# entry to program
def main():
    client.run(CONFIG.get('SERVER', 'Token'))
    on_ready()

if __name__ == '__main__':
    main()