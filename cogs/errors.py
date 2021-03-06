from sys import stderr
from traceback import print_exception

from discord.ext import commands


class ErrorHandler(commands.Cog, command_attrs={'hidden': True}):

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if hasattr(ctx.command, 'on_error'):
            await ctx.send('Error occurred on doing this command.')

        error = getattr(error, 'original', error)

        if isinstance(error, commands.CommandNotFound):
            return

        if isinstance(error, (
            IndexError,
            KeyError,
            commands.CheckFailure,
            commands.MissingRole,
            commands.NSFWChannelRequired,
            commands.BadArgument,
            commands.MemberNotFound
        )):
            return await ctx.send(embed=ctx.bot.embed.error(
                title='⚠ | Error!', description=str(error)
            ))

        if isinstance(error, (
            commands.TooManyArguments,
            commands.MissingRequiredArgument
        )):
            return await ctx.send_help(ctx.command)

        else:
            print(f'Ignoring exception in command {ctx.command}:', file=stderr)
            print_exception(type(error), error, error.__traceback__, file=stderr)


def setup(bot):
    bot.add_cog(ErrorHandler())
