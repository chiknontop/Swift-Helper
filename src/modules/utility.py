"""
All Utility-Related Commands
"""

import selfcord as discord
from selfcord.ext import commands

from ..bot import TheBot


class Utility(commands.Cog):
    """Contains All the Utility-Related Commands"""

    def __init__(self, bot: TheBot):
        self.bot = bot

    
    @commands.command(
        name="theme"
    )
    async def theme(self, ctx: commands.Context, new_theme: str):
        """Switches the Discord Client Theme

        Parameters
        ----------
        new_theme:
            The Theme to Switch To.
        """

        await ctx.message.delete()

        if new_theme == "light":
            await self.bot.settings.edit(
                theme=discord.Theme.light
            )
            self.bot.logger.info("Updated Client-Theme to LIGHT.")
        elif new_theme == "dark":
            await self.bot.settings.edit(
                theme=discord.Theme.dark
            )
            self.bot.logger.info("Updated Client-Theme to DARK.")
        else:
            self.bot.logger.error(commands.BadArgument(f"'{new_theme}' is an Invalid Argument"))


async def setup(bot: TheBot):
    await bot.add_cog(Utility(bot))
