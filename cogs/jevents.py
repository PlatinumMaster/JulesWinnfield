from discord.ext import commands
from discord import Game, Status
from datetime import datetime

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('%s, Bot ID %s.' % (self.bot.user.name, self.bot.user.id))
        await self.bot.change_presence(status=Status.dnd, activity=Game("Pulp Fiction."))

    @commands.Cog.listener()
    async def on_message(self, ctx):
        try:
            print("[%s] ('%s'/'#%s') %s: %s" % (datetime.now(), ctx.guild.name, ctx.channel.name, ctx.author, ctx.content))
        except:
            print("[%s] (Direct Message) %s: %s" % (datetime.now(), ctx.author, ctx.content))

def setup(bot):
    bot.add_cog(Events(bot))