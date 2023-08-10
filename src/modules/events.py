"""
All Discord Events
"""

import selfcord as discord
from selfcord.ext import commands

from ..bot import TheBot


class Events(commands.Cog):
    """Contains All the Events-Listeners"""
    
    def __init__(self, bot: TheBot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error: commands.CommandError) -> None:
        """Global Command Error Handler

        Parameters
        ----------
        ctx: :class:`commands.Context`
            The Context of the Command
        error: :class:`commands.CommandError`
            The Error
        """
        
        raise error


async def setup(bot: TheBot):
    await bot.add_cog(Events(bot))
