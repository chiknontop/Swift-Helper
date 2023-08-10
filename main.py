"""
The Main-Running File
"""

import logging

import selfcord as discord
from selfcord.ext import commands

from src.bot import TheBot
from src.utils import get_Formatter


if __name__ == "__main__":

    # Setting-Up Logging
    logger = logging.getLogger()
    handler = logging.StreamHandler()
    logger.addHandler(handler)

    discord.utils.setup_logging(
        level=logging.INFO,
        handler=handler,
        formatter=get_Formatter(handler)
    )
    logging.getLogger("discord.http").setLevel(logging.WARNING)

    # Initialising Bot
    bot = TheBot(
        command_prefix=TheBot.get_prefix,
        case_insensitive=True,
        help_command=commands.DefaultHelpCommand(
            sort_commands=True,
            show_parameter_descriptions=True
        ),
        max_messages=0,
        chunk_guilds_at_startup=False,
        self_bot=True,
        sync_presence=False,
        logger=logger
    )

    # Running the Bot
    try:
        bot.execute()
    except discord.LoginFailure:
        bot.logger.error("Invalid Token - Make Sure to Etner the Correct One in src/config/settings.json")
    finally:
        bot.die()
    input()
