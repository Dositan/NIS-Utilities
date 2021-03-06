from discord.ext import commands


class Owner(commands.Cog, command_attrs={'hidden': True}):

    async def cog_check(self, ctx):
        """Cog checker for this extension, checks if the called author was
        the bot owner, otherwise, does nothing."""
        return await ctx.bot.is_owner(ctx.author)

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

    @commands.group(invoke_without_command=True, aliases=['r'])
    async def reload(self, ctx, *, module: str):
        """Reloads a module."""
        try:
            module = module.split(' | ')
            for ext in module:
                ctx.bot.reload_extension(ext)
        except commands.ExtensionError as e:
            await ctx.send(f'{e.__class__.__name__}: {e}')
        else:
            await ctx.send(f'Ext {", ".join(module)} reloaded🔄')

    @reload.command(name='all', aliases=['a'])
    async def reload_all(self, ctx):
        """Reloads all modules at a time."""
        try:
            for ext in ctx.bot.config['bot']['exts']:
                ctx.bot.reload_extension(ext)
        except commands.ExtensionError as e:
            await ctx.send(f'{e.__class__.__name__}: {e}')
        else:
            await ctx.message.add_reaction('🔄')


def setup(bot):
    bot.add_cog(Owner())
