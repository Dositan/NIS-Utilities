from typing import Optional

from discord.ext import commands
from jishaku.codeblocks import codeblock_converter
from utils import Cog, TabularData


class Owner(Cog, command_attrs={'hidden': True}):
    icon = '👑'
    name = 'Owner'

    async def cog_check(self, ctx):
        """Cog checker for this extension, checks if the called author was
        the bot owner, otherwise, does nothing."""
        return await ctx.bot.is_owner(ctx.author)

    @commands.command()
    async def sql(self, ctx, *, query: codeblock_converter):
        """Does some nice SQL queries."""
        query = query.content

        if query.lower().startswith('select'):
            strategy = ctx.bot.pool.fetch

        else:
            strategy = ctx.bot.pool.execute

        results = await strategy(query)

        if isinstance(results, list):
            columns = list(results[0].keys())
            table = TabularData()
            table.set_columns(columns)
            table.add_rows(list(result.values()) for result in results)
            render = table.render()
            msg = f'```py\n{render}\n```'

        else:
            msg = results

        await ctx.send(msg)

    @commands.command(aliases=['close'])
    async def shutdown(self, ctx):
        """Shutdowns the bot (stops all the processes)."""
        await ctx.message.add_reaction('👌')
        await ctx.bot.close()

    @commands.command(aliases=['l'])
    async def load(self, ctx, *, module: str):
        """Loads a module."""
        try:
            ctx.bot.load_extension('cogs.' + module)
        except commands.ExtensionError as e:
            await ctx.send(f'{e.__class__.__name__}: {e}')
        else:
            await ctx.send('\N{OK HAND SIGN}')

    @commands.command(aliases=['u'])
    async def unload(self, ctx, *, module: str):
        """Unloads a module."""
        try:
            ctx.bot.unload_extension('cogs.' + module)
        except commands.ExtensionError as e:
            await ctx.send(f'{e.__class__.__name__}: {e}')
        else:
            await ctx.send('\N{OK HAND SIGN}')

    @commands.command(aliases=['r'])
    async def reload(self, ctx, module: Optional[str]):
        """Reloads a module. Takes all extensions if none was given."""
        if module:
            ctx.bot.reload_extension(module)
            return await ctx.send(f'🔄 Ext `{module}` reloaded.')

        for ext in ctx.bot.config['bot']['exts']:
            ctx.bot.reload_extension(ext)

        await ctx.send('✅ Reloaded all extensions!')


def setup(bot):
    bot.add_cog(Owner())
