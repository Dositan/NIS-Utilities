from typing import Optional

import discord
from discord.ext import commands
from utils import Cog, is_in_nisdev, is_nis_developer


class NisDev(Cog):
    icon = '👨‍💻'
    name = 'NISDev'

    async def cog_check(self, ctx):
        return await is_in_nisdev().predicate(ctx)

    @commands.command()
    async def login(self, ctx, name: str, who: str, accepted: str.lower):
        """Log in as NIS Developer through this command!

        Args:
            name (str): Your first name.
            who (str): Who are you, enter either `student` or `teacher`.
            accepted (str): Do you accept rules? Enter `no` if you don't."""

        if accepted in ['no', 'nope']:
            return await ctx.send('👌 You don\'t get full access since you have rejected our rules.')

        elif who not in ['student', 'teacher']:
            raise commands.BadArgument('Wrong profession. Enter one of `student` or `teacher`.')

        elif await is_nis_developer().predicate(ctx):
            raise commands.BadArgument('You have already logged in. Check your info by typing `nis info`.')

        query = 'INSERT INTO nisdev(name, who, accepted, user_id) VALUES($1, $2, $3, $4)'
        await ctx.bot.pool.execute(query, name, who, bool(accepted), ctx.author.id)

        role = ctx.guild.get_role(803159920098803722)
        await ctx.author.add_roles(role, reason='Logged into NISDev successfully.')

        await ctx.send(f'🎉 Now, you are the part of **{ctx.guild}** community!')

    @commands.command()
    async def logout(self, ctx):
        """Log out from nisdev account by deleting your data from the database."""
        query = 'DELETE FROM nisdev WHERE user_id = $1'
        await ctx.bot.pool.execute(query, ctx.author.id)
        await ctx.message.add_reaction('✅')

    @commands.command()
    @is_nis_developer()
    async def info(self, ctx, member: Optional[discord.Member]):
        """Get information about a user who is stored in the database."""
        member = member or ctx.author
        query = 'SELECT name, who, accepted FROM nisdev WHERE user_id = $1'
        user = await ctx.bot.pool.fetchrow(query, member.id)

        embed = ctx.bot.embed(
            title=f'About {member}',
            description='\n'.join(f'**{k.capitalize()}:** {v}' for k, v in user.items())
        ).set_thumbnail(url=member.avatar_url)

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(NisDev())
