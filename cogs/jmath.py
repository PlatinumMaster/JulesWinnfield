from inspect import trace
from types import TracebackType
from sympy import integrate, diff, latex, Symbol
from sympy.plotting import plot, plot_implicit
from sympy.parsing.latex import parse_latex
from requests import post
from discord import File, embeds
import matplotlib.pyplot as plt
import json
from sympy.abc import *
import traceback
from discord.ext import commands
from os import remove
import util

class Math(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.line_cols = {
            0 : 'red',
            1 : 'orange',
            2 : 'yellow',
            3 : 'green',
            4 : 'blue',
			5 : 'purple',
            6 : 'black',
        }

    def latex2png(self, latex_commands):
        dataToSend = {
            'auth': { 
                'user': "guest", 
                'password': "guest" 
            },
            'latex': latex_commands,
            'resolution': 600,
            'color': "00FFFF",
	    }
        request = post('http://www.latex2png.com/api/convert', data=json.dumps(dataToSend))
        try:
            return f"http://www.latex2png.com{request.json()['url']}"
        except KeyError:
            return f"Error: {request.json()['result-message']})"

    # LaTeX commands.
    @commands.command()
    async def latex(self, ctx, *, expression):
        result = self.latex2png(expression)
        success = "Error" not in result[0:5]
        await ctx.reply(embed=util.generate_embed(title="Invalid LaTeX Expression" if not success else "LaTeX", 
            description=f'```{result}```' if not success else '', 
            image_link=result if success else '')
        )

    async def integral_latex(self, isDefinite, respect_to, lower_bound, upper_bound, expression):
        integral_configuration = (parse_latex(respect_to), parse_latex(lower_bound), parse_latex(upper_bound)) if isDefinite else (parse_latex(respect_to))
        answer = integrate(parse_latex(expression), integral_configuration)
        return self.latex2png(f'\\int_{{{lower_bound if isDefinite else ""}}}^{{{upper_bound if isDefinite else ""}}} {expression} d{respect_to} = {latex(answer)} {"+ C" if not isDefinite else ""}')

    # Calculus commands.
    @commands.command()
    async def antiderivative(self, ctx, respect_to, *, expression):
        '''Finds the antiderivative of <expression>.'''
        result = None
        try:
            result = [
                f'Definite integral of {expression} d{respect_to} [{a}, {b}]', 
                await self.integral_latex(False, respect_to, 0, 0, expression),
                True
            ]
        except Exception as e:
            result = [
                f'Failed to integrate {expression}.', 
                f'```{e}```',
                False
            ]
        await ctx.reply(embed=util.generate_embed(title=result[0], description=result[1] if not result[2] else '', image_link=result[1] if result[2] else ''))


    @commands.command()
    async def definite_integral(self, ctx, respect_to, lower_bound, upper_bound, *, expression):
        '''Definite integral of <expression> d<respect_to> from <a> to <b>'''
        result = None
        try:
            result = [
                f'Definite integral of {expression} d{respect_to} [{a}, {b}]', 
                await self.integral_latex(True, respect_to, lower_bound, upper_bound, expression),
                True
            ]
        except Exception as e:
            result = [
                f'Failed to integrate {expression}.', 
                f'```{e}```',
                False
            ]
        await ctx.reply(embed=util.generate_embed(title=result[0], description=result[1] if not result[2] else '', image_link=result[1] if result[2] else ''))

    # Graphing commands.
    @commands.command()
    async def plot_explicit(self, ctx, xmin, xmax, ymin, ymax, *, functions):          
        p = plot(*[parse_latex(function) for function in functions.split(',')], xlim=(xmin, xmax), ylim=(ymin, ymax), title='Graph', show=False)
        for x in range(functions.count(',') + 1): 
            p[x].line_color = self.line_cols[x % self.line_cols.keys().__len__()]
        p.save('tmp.png')      
        await ctx.reply(file=File('tmp.png'), embed=util.generate_embed(title="Graph", description="", image_link='attachment://tmp.png'))

    @commands.command()
    async def plot_implicit(self, ctx, xmin, xmax, ymin, ymax, x_axis_var, y_axis_var, *, function):          
        p = plot_implicit(parse_latex(function), (x_axis_var, xmin, xmax), (y_axis_var, ymin, ymax), title='Graph', show=False, line_color=self.line_cols[0])
        p.save('tmp.png')
        await ctx.reply(file=File('tmp.png'), embed=util.generate_embed(title="Graph", description="", image_link='attachment://tmp.png'))

def setup(bot):
    bot.add_cog(Math(bot))
    
