from json import load

import discord
from discord.ext import commands, flags


class Table(commands.Cog):

    @commands.command()
    async def table(self, ctx):
        """See your class' table."""
        await ctx.send('help yourself lol', file=discord.File('./data/table.xlsx'))

    @commands.command()
    async def sau(self, ctx, grade: int = None):
        """The school Summative Assessments for the Unit table."""
        if grade:
            try:
                await ctx.send('help yourself lol', file=discord.File(f'./data/sau/{grade}.xlsx'))

            except FileNotFoundError:
                await ctx.send(f'I don\'t have this grade ({grade}) in my data, sorry.')
        else:
            await ctx.send(f'huh? no grade specifed, do one of {", ".join([str(i) for i in range(7, 13)])}')

    @flags.add_flag('--language', '-l', choices=['kaz', 'rus'], required=True)
    @flags.command(aliases=['lit'])
    async def literature(self, ctx, **flags):
        """See the literature list for a given language.
        Language is either Kazakh or Russian."""
        language = flags.pop('language')
        titles = {'kaz': 'Қазақ Әдебиеті', 'rus': 'Русская Литература'}
        lit = load(open(f'./data/grades/8/{language}lit.json', 'r'))
        embed = ctx.bot.embed(
            title=titles[language],
            description='\n'.join(f'**[{name}]({value})**' for name, value in lit.items())
        )
        await ctx.send(embed=embed)

    @commands.command()
    @commands.has_role('D-student')
    async def bday(self, ctx):
        """D class students' birthdays."""
        birthdays = load(open('./data/grades/8/birthdays.json', 'r'))
        embed = ctx.bot.embed(
            title='Дни Рождения 8 «Д»',
            description='\n'.join(f'**{name}**: {value}' for name, value in birthdays.items())
        )
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Table())
