import asyncio
import re
from datetime import datetime, timedelta
import aiohttp
import discord
import toml
from discord.ext import commands
from utils.Embed import Embed


class NisBot(commands.Bot):
    intents = discord.Intents.all()

    def __init__(self, *args, **kwargs):
        super().__init__(
            'nis ',
            intents=self.intents,
            activity=discord.Game(name='nis help'),
            case_insensitive=True,
            max_messages=1000,
            allowed_mentions=discord.AllowedMentions(everyone=False, roles=False),
            member_cache_flags=discord.flags.MemberCacheFlags.from_intents(self.intents),
            chunk_guilds_at_startup=False
        )
        self.config = toml.load('config.toml')
        self.embed = Embed
        self.start_time = datetime.now()
        self.loop = asyncio.get_event_loop()
        self.session = aiohttp.ClientSession(loop=self.loop)

    @property
    async def uptime(self) -> timedelta:
        return int((datetime.now() - self.start_time).total_seconds())

    async def close(self):
        await super().close()
        await self.session.close()

    async def get_context(self, message, *, cls=commands.Context):
        return await super().get_context(message, cls=cls)

    async def on_message(self, message):
        if not self.is_ready():
            return

        if re.fullmatch(f'<@(!)?{self.user.id}>', message.content):
            ctx = await self.get_context(message)
            cmd = self.get_command('prefix')
            await cmd(ctx)

        await self.process_commands(message)

    async def on_message_edit(self, before, after):
        if before.content != after.content:
            return await self.process_commands(after)
        if before.embeds:
            return
