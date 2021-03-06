import discord
from discord.ext.commands import Cog


class ReactionRoles(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.reactions = {
            'python': 'Programmer',
            'grass': 'Gamer',
            'really': 'Anime',
            'genius': 'Meme Creator',
            'musician': 'Musician',
            'happypepe': 'Tester'
        }

    @Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.message_id == 739847026560336014:
            guild = discord.utils.find(lambda g: g.id == payload.guild_id, self.bot.guilds)

            for emoji_name, role_name in self.reactions.items():
                if str(payload.emoji) == emoji_name:
                    role = discord.utils.get(guild.roles, name=role_name)

            if role:
                member = discord.utils.find(lambda m: m.id == payload.user_id, guild.members)
                if member:
                    await member.add_roles(role)
                else:
                    print('Member Not Found')
            else:
                print('Role Not Found')

    @Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        if payload.message_id == 739847026560336014:
            guild = discord.utils.find(lambda g: g.id == payload.guild_id, self.bot.guilds)

            for emoji_name, role_name in self.reactions.items():
                if str(payload.emoji) == emoji_name:
                    role = discord.utils.get(guild.roles, name=role_name)

            if role:
                member = discord.utils.find(lambda m: m.id == payload.user_id, guild.members)
                if member:
                    await member.remove_roles(role)
                else:
                    print('Member Not Found')
            else:
                print('Role Not Found')


def setup(bot):
    bot.add_cog(ReactionRoles(bot))
