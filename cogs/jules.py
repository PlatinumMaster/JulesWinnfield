from discord.ext import commands
import re
import unicodedata
import asyncio
import datetime

class JulesWinnfieldQuotes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ban_list = [808390819954032680, 653811465567993937]
        self.quoteNum = 0
        self.time_window_milliseconds = 6000
        self.max_msg_per_window = 5
        self.rate_limit = {}
        self.quotes = [
            "What does Marsellus Wallace looks like?",
            "What country are you from?",
            "'What' ain't no country I ever heard of! They speak English in 'What'?",
            "ENGLISH MOTHERFUCKER! Do you speak it?!",
            "Then you know what I'm saying. Describe what Marsellus Wallace looks like!",
            "SAY WHAT AGAIN. SAY. WHAT. AGAIN. I DARE YOU. I DOUBLE DARE YOU, MOTHERFUCKER. SAY WHAT ONE MORE GOD DAMN TIME.",
            "The path of the righteous man is beset on all sides by the inequities of the selfish and the tyranny of evil men. Blessed is he who, in the name of charity and good will, shepherds the weak through the valley of the darkness. For he is truly his brother's keeper and the finder of lost children. And I will strike down upon thee with great vengeance and furious anger those who attempt to poison and destroy my brothers. And you will know I am the Lord when I lay my vengeance upon thee."
        ]

    @commands.Cog.listener()  
    async def on_message(self, ctx):
        # Get current epoch time in milliseconds
        curr_time = datetime.datetime.now().timestamp() * 1000

        # Make empty list for author id, if it does not exist
        if not self.rate_limit.get(ctx.author.id, False):
            self.rate_limit[ctx.author.id] = []

        # Append the time of this message to the users list of message times
        self.rate_limit[ctx.author.id].append(curr_time)

        # Find the beginning of our time window.
        expr_time = curr_time - self.time_window_milliseconds

        # Find message times which occurred before the start of our window
        expired_msgs = [
            msg_time for msg_time in self.rate_limit[ctx.author.id]
            if msg_time < expr_time
        ]

        # Remove all the expired messages times from our list
        for msg_time in expired_msgs:
            self.rate_limit[ctx.author.id].remove(msg_time)

        if len(self.rate_limit[ctx.author.id]) > self.max_msg_per_window and ctx.author.id != self.bot.user.id:
            await ctx.reply("Knock it off, Boo Boo the Fool.")
        else:
            # If mentioned:
            if self.bot.user in ctx.mentions and ctx.author.id != self.bot.user.id:
                await ctx.reply('I don\'t remember asking you a god damn thing.')
                return
            # If someone says what:
            tokenized_string = [re.sub(r'[^a-zA-Z0-9]', '', inp) for inp in "".join(dict.fromkeys(re.sub(r'[^A-Za-z0-9 ]+', '', unicodedata.normalize('NFKD', ctx.content).lower()))).split(' ')]
            if "what" == "".join(tokenized_string) and ctx.author.id != self.bot.user.id:
                if ctx.guild.id not in self.ban_list:
                    await ctx.reply('%s' % self.quotes[self.quoteNum])    
                    if self.quoteNum + 1 is len(self.quotes):
                        self.quoteNum = 0
                    else:
                        self.quoteNum += 1
                    await asyncio.sleep(10)
                return

def setup(bot):
    bot.add_cog(JulesWinnfieldQuotes(bot))
