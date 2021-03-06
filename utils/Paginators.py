import discord
from discord.ext import menus


class Paginator(menus.MenuPages):
    def __init__(self, source, **kwargs):
        super().__init__(source=source, check_embeds=True, **kwargs)

    async def finalize(self, timed_out):
        try:
            if timed_out:
                await self.message.clear_reactions()
            else:
                await self.message.delete()
        except discord.HTTPException:
            pass
