from discord.ext import commands
from discord_slash import SlashCommand

class JulesWinnfield:
    def __init__(self, token):
        self.startup_ext = ['jevents', 'jadmin', 'jmath']
        self.bot = commands.Bot(command_prefix='j.')
        self.ext_dir = 'cogs'
        self.slash = SlashCommand(self.bot, sync_commands=True, sync_on_cog_reload=True)
        self.load_extensions()
        self.bot.run(token)

    def load_extensions(self):
        for ext in self.startup_ext:
            try: 
                self.bot.load_extension(f'{self.ext_dir}.{ext}' )
            except Exception as e:
                print(e)

JulesWinnfield('token')