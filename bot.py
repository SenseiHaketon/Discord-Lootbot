import random
import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True

default_channelname = 'Allgemein'

client = commands.Bot(command_prefix = '!', intents=intents)
client.channelref = None
client.curses = ['']


@client.event
async def on_ready():
    print('Bot is ready.')

def get_curses():
    file = open("curses.txt", "r", encoding="utf-8")
    client.curses = file.readlines()

@client.command()
async def curse(ctx):
    await ctx.send(get_random_curse())

def get_random_curse():
    if(client.curses == None):
        get_curses()   
    if(len(client.curses) > 0):
        return random.choice(client.curses)

@client.command()
async def addcurse(ctx, curse_to_add):
    if(len(curse_to_add) > 0 and curse_to_add not in client.curses):
        with open("curses.txt", "a", encoding="utf-8") as file:
            file.write(f'\n{curse_to_add}')
            get_curses()
            await ctx.send(f"'{curse_to_add}' was added to my database!")
    elif(curse_to_add in client.curses):
        await ctx.send(f"'{curse_to_add}' already is in my database you {get_random_curse()}")

@client.command(aliases=['channel'])
async def _channel(ctx, channelname=''):
    print('Channel command started.')
    if(channelname == ''):
        if(client.channelref != None):
            print(client.channelref.id)
            await ctx.send(f"Current channel: '{client.channelref}'")
        else:
            print('No channel was set!')
            await ctx.send("No channel was set! Running this command with '[channelname]' as parameter sets the current channel.")
    else:
        await set_channel(ctx, channelname)
        
async def set_channel(ctx, channelname): # Make this work with text channels too!
    new_channel = get_channel(ctx, channelname)
    if(new_channel != None):
        client.channelref = new_channel           
        print(f'New voice channel: {client.channelref.name} ({client.channelref.id})')
        await ctx.send(f"New channel set to '{channelname}'!")
    else:
        print(f'Voice channel {channelname} not found!')
        await ctx.send(f"Channel '{channelname}' not found!")        

def get_channel(ctx, channelname):
    for channel in ctx.guild.voice_channels:
        if(channel.name == channelname):
            return channel
    return None

@client.command(aliases=['loot'])
async def roll(ctx, channelname=''):  
    print('Roll command started.')
    channel_to_roll = client.channelref
    if(channelname != ''):
        channel_to_roll = get_channel(ctx, channelname)
    elif(client.channelref == None):
        print(f'No channel was set. Trying to get default channel {default_channelname}.')
        await set_channel(ctx, default_channelname)
        channel_to_roll = client.channelref

    if(channel_to_roll != None):       
        await roll_over_members(ctx, channel_to_roll.members)          
    else:
        print('Failed to find default channel! Aborting Roll command...')
        await ctx.send(f"Error: Channel was not set correctly. Try using '!channel [channel name]' command!")

@client.command()
async def rollall(ctx):    
    await roll_over_members(ctx, ctx.guild.members)

async def roll_over_members(ctx, members):
    selected_member = random.choice(members)
    print(f'User {selected_member} won the roll!')
    await ctx.send(selected_member.mention + ' won!')

get_curses()
client.run('NzgzNjg3MjcyODcyNDExMTU2.X8eXpg.nVq9z8HhuNXXUEg3Dzd0EYPoj84')