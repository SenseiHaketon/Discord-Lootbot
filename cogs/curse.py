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
    async def addcurse(self, ctx, *curse_to_add):
        combined_curse = ' '.join(curse_to_add)
        if(len(combined_curse) > 0 and combined_curse.casefold() not in (entry.casefold() for entry in self.curses)):
            with open("curses.txt", "a", encoding="utf-8") as file:
                file.write(f'\n{combined_curse}')
                self.load_curses()
                await ctx.send(f"*{combined_curse}* was added to my database!")
        elif(combined_curse in self.curses):
            await ctx.send(f"*{combined_curse}* already is in my database you **{self.get_random_curse()}**!")


def setup(client):
    client.add_cog(Curse(client))