import random
import discord
from discord.ext import commands

class Curse(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.load_curses()

    def load_curses(self):
        file = open("curses.txt", "r", encoding="utf-8")
        self.curses = file.read().splitlines()

    def get_random_curse(self):
        if(len(self.curses) > 0 and self.curses != None):
            return random.choice(self.curses)

    @commands.Cog.listener()
    async def on_ready(self):
        print('Curse Cog loaded.')

    @commands.command(aliases=['insult'])
    async def curse(self, ctx, member: discord.Member = None):
        message = ''
        if member is not None: 
            message += member.mention + ' you '
        await ctx.send(f'{message}**{self.get_random_curse()}**')

    @commands.command()
    async def addcurse(self, ctx, curse_to_add):
        if(len(curse_to_add) > 0 and curse_to_add not in self.curses):
            with open("curses.txt", "a", encoding="utf-8") as file:
                file.write(f'\n{curse_to_add}')
                self.load_curses()
                await ctx.send(f"*{curse_to_add}* was added to my database!")
        elif(curse_to_add in self.curses):
            await ctx.send(f"*{curse_to_add}* already is in my database you **{self.get_random_curse()}**!")


def setup(client):
    client.add_cog(Curse(client))