"""
The Bot Instance
"""

# Standard Libraries
import os
import inspect
import logging

# External Libraries
import aiohttp
import selfcord as discord
from selfcord.ext import commands
from pystyle import Center, Colors, Colorate

from typing import Optional

# Local Libraries
from .utils import *


class TheBot(commands.Bot):
    """The Bot"""
    def __init__(self, *args, **kwargs) -> None:
        """Initialising the Bot"""

        _logger = kwargs.pop("logger", None)
        super().__init__(*args, **kwargs)

        self._logger = _logger or logging.getLogger()
        self.initial_prefix: str = read_json(resolve_path() + "/config/" + "settings.json")['PREFIX']
        self._start_time = discord.utils.utcnow()


    @property
    def logger(self) -> logging.Logger:
        """Returns the Logger"""
        return self._logger

    @property
    def version(self) -> str:
        """Returns the Version of the Bot."""
        return "4.0"
    
    @property
    def cwd(self) -> str:
        """Returns the Current Directory Path."""
        return resolve_path()
    
    @property
    def session(self) -> aiohttp.ClientSession:
        """Returns the Request Handler"""
        return self.__session
    
    @staticmethod
    async def get_prefix(message: discord.Message) -> str:
        """Returns the Prefix"""
        return read_json(resolve_path() + "/config/" + "settings.json")['PREFIX']
    
    @property
    def cwd(self) -> str:
        """Returns the Current Directory Path."""
        return resolve_path()
       
    def execute(self) -> None:
        """Starts the Bot"""
        self.run(
            read_json(self.cwd + "/config/" + "settings.json")['DISCORD-TOKEN'],
            log_handler=None
        )
    
    def die(self) -> None:	
        """Stops the Bot"""	
        if self.session:	
            self.loop.run_until_complete(self.session.close())


    # DISCORD-EVENTS
    async def setup_hook(self):
        """Initalisation"""

        # Creating HTTP-Session
        self.__session = aiohttp.ClientSession(loop=self.loop)

        # Loading Cogs
        for file in os.listdir(self.cwd + "/modules"):
            if file.endswith(".py") and not file.startswith("_"):
                await self.load_extension(f"src.modules.{file[:-3]}")


    async def on_ready(self):
        """Called when the Bot is READY"""
        os.system("cls" if os.name == "nt" else "clear")
        if os.name == "nt":
            os.system(f"title Swift-Staff-Helper v{self.version}｜ Logged-In As: @{self.resolve_username(self.user)}")

        logo = inspect.cleandoc(r"""
         ___________      ___________________________
        /   _____/  \    /  \   \_   _____|__    ___/
        \_____  \\   \/\/   /   ||    __)   |    |   
        /        \\        /|   ||     \    |    |   
       /_______  / \__/\  / |___|\___  /    |____|   
               \/       \/           \/ H E L P E R              
        """)

        divider = "─────────────────────────────────────────────"
        col = os.get_terminal_size().columns
        for _ in range(len(divider), col):
            divider += "─"

        print()
        print(Colorate.Horizontal(Colors.blue_to_cyan, Center.XCenter(logo)))
        print(Colorate.Horizontal(Colors.blue_to_cyan, Center.XCenter(divider)))

        self.logger.info(f"Logged-In As: @{self.resolve_username(self.user)}\n")

    
    async def on_command(self, ctx: commands.Context):
        """Called when a Valid Command is Run"""

        if ctx.command.name == "help":
            await ctx.message.delete()
            
        self.logger.info(f"Command Used: {ctx.message.clean_content}")


    # DISCORD-METHODS
    def resolve_username(self, user: discord.User) -> str:
        """Returns a User's Username Nicely

        Parameters
        -----------
        user: :class:`discord.User`
            The User
        
        Returns
        -------
        :class:`str`
            The User Name
        """
        if user.discriminator == "0":
            return user.name
        else:
            return f"{user.name}#{user.discriminator}"
        

    def resolve_avatar(self, user: discord.User) -> str:
        """Returns a User's Avatar

        Parameters
        -----------
        user: :class:`discord.User`
            The User
        
        Returns
        -------
        :class:`str`
            The Avatar URL
        """
        if user.avatar:
            return user.avatar.url
        else:
            return user.default_avatar.url


    async def resolve_member(self, guild: discord.Guild, user_id: int) -> Optional[discord.Member]:
        """Returns a :class:`discord.Member`

        Parameters
        -----------
        guild: :class:`discord.Guild`
            The Guild to Search from
        user_id: :class:`int`
            The Member's ID to Search for
        
        Returns
        -------
        Optional[:class:`discord.Member`]
            The Member
        """
        member = guild.get_member(user_id)
        if member:
            return member
        else:
            return await guild.fetch_member(user_id)


    async def resolve_user(self, user_id: int) -> discord.User:
        """Returns a :class:`discord.User`

        Parameters
        -----------
        user_id: :class:`int`
            The User to Retrieve

        Raises
        ------
        :class:`commands.UserNotFound`
            Raised when the User-ID provided is Invalid

        Returns
        -------
        :class:`discord.User`
            The User
        """
        return self.get_user(user_id) or await self.fetch_user(user_id)
