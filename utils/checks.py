from discord.ext import commands


def is_nis_developer():
    async def predicate(ctx):
        return bool(await ctx.bot.pool.fetch('SELECT * FROM nisdev WHERE user_id = $1', ctx.author.id))

    return commands.check(predicate)


def is_in_nisdev():
    async def predicate(ctx):
        home = ctx.bot.config['bot']['nisdev']
        return ctx.guild.id == home

    return commands.check(predicate)
