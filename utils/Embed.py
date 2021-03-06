from datetime import datetime as dt
from discord import Embed as E


class Embed(E):
    def __init__(self, color=0xf5f5f5, timestamp=None, **kwargs):
        super(Embed, self).__init__(
            color=color,
            timestamp=timestamp or dt.utcnow(),
            **kwargs
        )

    @classmethod
    def error(cls, color=0xff0000, **kwargs):
        return cls(color=color, **kwargs)
