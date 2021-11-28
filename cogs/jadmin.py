from discord.ext import commands
import util

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.plugin_ops = {
            'load' : lambda x: self.bot.load_extension(f'cogs.{x}'),
            'unload' : lambda x: self.bot.unload_extension(f'cogs.{x}'),
            'reload' : lambda x: self.bot.reload_extension(f'cogs.{x}'),
        }
        self.admins = {
            159106433072365568 : ['global'], # PlatinumMaster
        }

    async def plugin_manager(self, ctx, name, operation):
        result = None
        if self.isAdmin(ctx.author.id, ctx.guild.id):
            try:
                self.plugin_ops[operation](name)
                result = [f'Successfully {operation}ed plugin \'{name}\'.', '']
            except Exception as e:
                result = [f'Failed to {operation} plugin \'{name}\'.', f'```{e}```']
                print(e)
        else:
            result = [f'Nope.', 'Not gonna happen.']
        await ctx.send(embed=util.generate_embed(title=result[0], description=result[1]))
        
    @commands.command()
    async def reload(self, ctx, *, content): await self.plugin_manager(ctx, content, 'reload')

    @commands.command()
    async def load(self, ctx, *, content): await self.plugin_manager(ctx, content, 'load')

    @commands.command()
    async def unload(self, ctx, *, content): await self.plugin_manager(ctx, content, 'unload')

    @commands.command()
    async def say(self, ctx, *, content='You gonna say something?'): await ctx.send(content) if self.isAdmin(ctx.author.id, ctx.guild.id) else ctx.reply("Hey pal. You just blow in from stupid town?")

    # Does a check for admin.
    isAdmin = lambda self, id, guild: id in self.admins.keys() and id != self.bot.user.id and (guild in self.admins[id] or 'global' in self.admins[id])

def setup(bot):
    bot.add_cog(Admin(bot))

