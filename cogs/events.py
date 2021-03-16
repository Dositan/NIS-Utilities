from discord import utils
from utils import Cog


class Events(Cog):
    icon = '🎲'
    name = 'Events'

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
    async def on_member_join(self, member):
        if member.bot:
            return

        g = member.guild
        cfg = self.bot.config['bot']

        if g.id == cfg['home']:
            wc = self.bot.get_channel(cfg['welcome'])  # wc → welcome channel
            await wc.send(f'{member.mention}, welcome to {g}!\n'
                          'Type `nis login <your_name> <student/teacher> <yes/no>` last parameter is for: "Do you accept rules?"\n'
                          'Example: **nis login Yerassyl student yes**. Happy hacking!')

    @Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.message_id == 739847026560336014:
            guild = utils.find(lambda g: g.id == payload.guild_id, self.bot.guilds)

            for emoji_name, role_name in self.reactions.items():
                if str(payload.emoji) == emoji_name:
                    role = utils.get(guild.roles, name=role_name)

            await payload.member.add_roles(role)

    @Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        if payload.message_id == 739847026560336014:
            guild = utils.find(lambda g: g.id == payload.guild_id, self.bot.guilds)

            for emoji_name, role_name in self.reactions.items():
                if str(payload.emoji) == emoji_name:
                    role = utils.get(guild.roles, name=role_name)

            member = utils.find(lambda m: m.id == payload.user_id, guild.members)
            await member.remove_roles(role)


def setup(bot):
    bot.add_cog(Events(bot))
