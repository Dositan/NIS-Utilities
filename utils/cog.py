from discord.ext.commands import Cog as C


class Cog(C):
    """No extra features currently. TODO add use ideas from notes."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __str__(self):
        return '{0.icon} {0.name}'.format(self)  # each cog has icon and name instances
