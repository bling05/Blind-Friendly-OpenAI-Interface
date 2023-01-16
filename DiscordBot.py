import discord
import openai
from discord.ext import commands
import asyncio
from gtts import gTTS

TOKEN = ''
CHATGPT_TOKEN = ''

LANG = 'en'
TLD = 'com'
openai.api_key = CHATGPT_TOKEN


intents = discord.Intents.all()
intents.members = True
client = discord.Client(command_prefix = ',', intents=intents)

def response(message, slice):
    if slice:
        message.content = ' '.join(message.content.split()[1:])
    print(message.content)
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=message.content,
        max_tokens=1024,
        temperature=0.7,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    return response["choices"][0]["text"]

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    print(f"{message.author}: {message.content}")
    if message.author == client.user:
        return

    if 'join kat' in message.content.lower() or 'join cat' in message.content.lower():
        if message.author.voice: # If the person is in a channel
            channel = message.author.voice.channel
            await channel.connect()
            await message.channel.send('Joined!')
        else: #But is (s)he isn't in a voice channel
            await message.channel.send("You must be in a voice channel first so I can join it.")
        return
    if 'leave kat' in message.content.lower() or 'leave cat' in message.content.lower():
        if (message.guild.voice_client): # If the bot is in a voice channel 
            await message.guild.voice_client.disconnect() # Leave the channel
            await message.channel.send('Bye!')
        else: # But if it isn't
            await message.channel.send("I'm not in a voice channel, use the join command to make me join.")
        return


    if 'cat' in message.content.lower() or 'kat' in message.content.lower():
        # send the response
        str = response(message, True)
        if str != '':
            await message.channel.send(str)
            
            if message.guild.voice_client is not None:
                tts = gTTS(text=str, tld=TLD, lang=LANG)
                tts.save("string_audio.mp3")
                vc = client.voice_clients[0]
                if vc.is_connected():
                    vc.play(discord.FFmpegPCMAudio("string_audio.mp3"))
                    vc.source = discord.PCMVolumeTransformer(vc.source)
                    vc.source.volume = 0.15
            if message.content.startswith('branton is so awesome (top 133 tank prodigy)'):
                vc = client.voice_clients[0]
                vc.play(discord.FFmpegPCMAudio("grind.mp3"))


        return

client.run(TOKEN)
