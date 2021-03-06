from difflib import get_close_matches
from discord.ext import commands, menus
from utils.Embed import Embed
from utils.Paginators import Paginator


class GroupHelp(menus.ListPageSource):
    '''Sends help for group-commands.'''

    def __init__(self, ctx, group, cmds):
        super().__init__(entries=cmds, per_page=3)
        self.ctx = ctx
        self.group = group

    async def format_page(self, menu, cmds):
        embed = Embed(
            title=f'Help for category `{self.group.qualified_name}`',
            description='```fix\n<> ← required argument\n[] ← optional argument```'
        )

        for cmd in cmds:
            signature = f'{self.ctx.prefix}{cmd.qualified_name} {cmd.signature}'
            embed.add_field(name=signature, value=cmd.description.format(prefix=self.ctx.prefix), inline=False)

        if (maximum := self.get_max_pages()) > 1:
            embed.set_author(name=f'Page {menu.current_page + 1} of {maximum} ({len(self.entries)} commands)')

        embed.set_footer(text=f'{self.ctx.prefix}help to see all commands list.')
        return embed


class MainHelp(menus.ListPageSource):
    def __init__(self, ctx, categories: list):
        super().__init__(entries=categories, per_page=3)
        self.ctx = ctx
        self.count = len(categories)

    async def format_page(self, menu, category):
        embed = Embed(
            description=f'{self.ctx.prefix}help [category | group] to get module help\n',
        ).set_footer(text=f'{self.ctx.prefix}help <command> to get command help.')

        embed.set_author(
            name=f'Page {menu.current_page + 1} of {self.get_max_pages()} ({self.count} categories)',
            icon_url=self.ctx.author.avatar_url_as(size=128)
        )

        for name, value in category:
            embed.add_field(name=name, value=value, inline=False)

        return embed


class MyHelpCommand(commands.HelpCommand):

    async def get_ending_note(self):
        return f'Type {self.clean_prefix}{self.invoked_with} [Category] to get help for a category.'

    async def send_bot_help(self, mapping):
        cats = []
        for cog, cmds in mapping.items():
            filtered = await self.filter_commands(cmds, sort=True)
            if filtered:
                all_cmds = ' • '.join(f'`{cmd}`' for cmd in cmds)
                if cog:
                    cats.append([cog.qualified_name, f"> {all_cmds}\n"])

        await Paginator(source=MainHelp(self.context, cats), timeout=30.0).start(self.context)

    async def send_cog_help(self, cog: commands.Cog):
        ctx = self.context

        if not hasattr(cog, 'name'):
            pass

        entries = await self.filter_commands(cog.get_commands(), sort=True)
        await Paginator(
            GroupHelp(ctx, cog, entries),
            clear_reactions_after=True,
            timeout=30.0
        ).start(ctx)

    async def send_command_help(self, command):
        embed = Embed(
            title=self.get_command_signature(command),
            description=command.help or 'No help found...'
        ).set_footer(text=await self.get_ending_note())

        if aliases := command.aliases:
            embed.add_field(name='Aliases', value=' | '.join(aliases), inline=True)

        if category := command.cog_name:
            embed.add_field(name='Category', value=category, inline=True)

        await self.get_destination().send(embed=embed)

    async def send_group_help(self, group):
        ctx = self.context

        if len(subcommands := group.commands) == 0:
            return await self.send_command_help(group)

        if len(entries := await self.filter_commands(subcommands, sort=True)) == 0:
            return await self.send_command_help(group)

        source = GroupHelp(ctx, group, entries)
        await Paginator(source, timeout=30.0).start(ctx)

    async def command_not_found(self, string):
        commands_list = [str(cmd) for cmd in self.context.bot.commands]
        dym = '\n'.join(get_close_matches(string, commands_list))
        msg = f'Could not find the command `{string}`.'
        return msg if not dym else msg + f' Did you mean...\n{dym}'

    def get_command_signature(self, command: commands.Command):
        return f'{self.clean_prefix}{command.qualified_name} {command.signature}'


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._original_help_command = bot.help_command
        bot.help_command = MyHelpCommand(command_attrs={'hidden': True, 'aliases': ['h']})

    @commands.command(hidden=True)
    async def prefix(self, ctx):
        """Shows the current prefix bot works for."""
        embed = ctx.bot.embed(description=f'The prefix is `nis ` or {ctx.bot.user.mention}.')
        await ctx.send(embed=embed)

    def cog_unload(self):
        self.bot.help_command = self._original_help_command


def setup(bot):
    bot.add_cog(Help(bot))
