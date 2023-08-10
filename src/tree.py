"""
The Tree Class.
"""

# External Libraries
import discord
from discord import app_commands
from discord.abc import Snowflake

from typing import Dict, List, Optional, Union, TYPE_CHECKING

if TYPE_CHECKING:
    from .bot import TheBot
    from .modules.events import Events


AppCommandStore = Dict[str, app_commands.AppCommand]

class TheTree(app_commands.CommandTree):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bot: TheBot = self.client
        self._global_app_commands: AppCommandStore = {}
        self._guild_app_commands: Dict[int, AppCommandStore] = {}

    
    async def on_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError) -> None:
        """Global App Command Error Handler

        Parameters
        ----------
        interaction: :class:`discord.Interaction`
            The Interaction that Raised the Error
        error: :class:`app_commands.AppCommandError`
            The Error that was Raised
        """

        if isinstance(error, app_commands.CheckFailure):
            if isinstance(error, app_commands.BotMissingPermissions):
                missing_perms = '\n'.join([f"- `{perm.replace('_', ' ').replace('guild', 'server').title()}`" for perm in error.missing_permissions])
                return await interaction.response.send_message(
                    f"{self.bot.emotes.cross()} **I am Missing the Following Permission(s) to Execute this Command:**\n{missing_perms}",
                    ephemeral=True
                )

            elif isinstance(error, (app_commands.MissingAnyRole, app_commands.MissingRole)):
                missing = []
                if isinstance(error, app_commands.MissingAnyRole):
                    missing = error.missing_roles
                elif isinstance(error, app_commands.MissingRole):
                    missing = [error.missing_role]

                missing_roles: Optional[List[discord.Role]] = []
                for m_r in missing:
                    missing_role = None
                    if isinstance(missing_role, int):
                        missing_role = interaction.guild.get_role(m_r)
                    elif isinstance(missing_role, str):
                        missing_role = discord.utils.get(interaction.guild.roles, name=m_r)
                    if missing_role:
                        missing_roles.append(missing_role)

                if missing_roles != []:
                    missing_roles = '\n'.join([f"- {m_r.mention}" for m_r in missing_roles])
                    return await interaction.response.send_message(
                        f"{self.bot.emotes.cross()} **You are Missing the Following Role(s) to Execute this Command:**\n{missing_roles}",
                        allowed_mentions=discord.AllowedMentions(roles=False),
                        ephemeral=True
                    )
                else:
                    return await interaction.response.send_message(
                        f"{self.bot.emotes.cross()} **You are Missing a Role(s) to Execute this Command!**",
                        ephemeral=True
                    )
                
            elif isinstance(error, app_commands.MissingPermissions):
                missing_perms = '\n'.join([f"- `{perm.replace('_', ' ').replace('guild', 'server').title()}`" for perm in error.missing_permissions])
                return await interaction.response.send_message(
                    f"{self.bot.emotes.cross()} **You are Missing the Following Permission(s) to Execute this Command:**\n{missing_perms}",
                    ephemeral=True
                )
                                
            elif isinstance(error, app_commands.NoPrivateMessage):
                return await interaction.response.send_message(
                    f"{self.bot.emotes.cross()} **This Command can only be Executed in a Server!**",
                    ephemeral=True
                )
            
            elif isinstance(error, app_commands.CommandOnCooldown):
                m, s = divmod(error.retry_after, 60)
                h, m = divmod(m, 60)

                if int(h) == 0 and int(m) == 0:
                    return await interaction.response.send_message(
                        f"{self.bot.emotes.cross()} **You must Wait `{int(s)} Seconds` before Re-Using this Command!**",
                        ephemeral=True
                    )
                elif int(h) == 0 and int(m) != 0:
                    return await interaction.response.send_message(
                        f"{self.bot.emotes.cross()} **You must Wait `{int(m)} Minutes` before Re-Using this Command!**",
                        ephemeral=True
                    )
                else:
                    time = (int(m)/60) + int(h)
                    return await interaction.response.send_message(
                        f"{self.bot.emotes.cross()} **You must Wait `{time} Hours` before Re-Using this Command!**",
                        ephemeral=True
                    )
            
            else:
                return await interaction.response.send_message(
                    f"{self.bot.emotes.cross()} **You are Missing Permissions to Execute this Command!**",
                    ephemeral=True
                )


        elif isinstance(error, app_commands.CommandLimitReached):
            return await interaction.response.send_message(
                f"{self.bot.emotes.cross()} **This Command has Reached it's Concurrent Limit!** `[Try Again Later]`",
                ephemeral=True
            )
        
        
        if interaction.response.is_done():	
            await interaction.followup.send(	
                f"{self.bot.emotes.cross()} **An Un-Expected Error has Occured `[The Dev has been Notified]`**",	
                ephemeral=True	
            )	
        else:	
            await interaction.response.send_message(	
                f"{self.bot.emotes.cross()} **An Un-Expected Error has Occured `[The Dev has been Notified]`**",	
                ephemeral=True	
            )

        cog: Events = self.bot.get_cog("Events")
        await cog.log_error(interaction, error)


    def resolve_command(self, value: Union[str, int], guild: Optional[Union[Snowflake, int]] = None) -> Optional[app_commands.AppCommand]:
        """Gets an Application Command by its Name or ID"""
        
        def search_dict(d: AppCommandStore) -> Optional[app_commands.AppCommand]:
            for cmd_name, cmd in d.items():
                if value == cmd_name or (str(value).isdigit() and int(value) == cmd.id):
                    return cmd
            return None

        if guild:
            guild_id = guild.id if not isinstance(guild, int) else guild
            guild_commands = self._guild_app_commands.get(guild_id, {})
            if not self.fallback_to_global:
                return search_dict(guild_commands)
            else:
                return search_dict(guild_commands) or search_dict(self._global_app_commands)
        else:
            return search_dict(self._global_app_commands)


    @staticmethod
    def _unpack_app_commands(commands: List[app_commands.AppCommand]) -> AppCommandStore:
        """Unpacks a List of Application Commands into a Dictionary"""

        ret: AppCommandStore = {}

        def unpack_options(options: List[Union[app_commands.AppCommand, app_commands.AppCommandGroup, app_commands.Argument]]):
            for option in options:
                if isinstance(option, app_commands.AppCommandGroup):
                    ret[option.qualified_name] = option
                    unpack_options(option.options)

        for command in commands:
            ret[command.name] = command
            unpack_options(command.options)

        return ret


    def _update_cache(self, commands: List[app_commands.AppCommand], guild: Optional[Union[Snowflake, int]] = None) -> None:
        """Updates the Cache with a List of Application Commands"""

        _guild: Optional[Snowflake] = None
        if guild is not None:
            if isinstance(guild, int):
                _guild = discord.Object(guild)
            else:
                _guild = guild

        if _guild:
            self._guild_app_commands[_guild.id] = self._unpack_app_commands(commands)
        else:
            self._global_app_commands = self._unpack_app_commands(commands)


    async def fetch_command(self, command_id: int, /, *, guild: Optional[Snowflake] = None) -> app_commands.AppCommand:
        """Fetches an Application Command by its ID"""

        res = await super().fetch_command(command_id, guild=guild)
        self._update_cache([res], guild=guild)
        return res


    async def fetch_commands(self, *, guild: Optional[Snowflake] = None) -> List[app_commands.AppCommand]:
        """Fetches All Application Commands"""

        res = await super().fetch_commands(guild=guild)
        self._update_cache(res, guild=guild)
        return res


    def _clear_command_cache(self, *, guild: Optional[Snowflake]) -> None:
        """Clears the Application Commands Cache"""

        if guild:
            self._guild_app_commands.pop(guild.id, None)
        else:
            self._global_app_commands = {}


    def clear_commands(self, *, guild: Optional[Snowflake], type: Optional[discord.AppCommandType] = None, clear_app_commands_cache: bool = True) -> None:
        """Clears the Application Commands"""

        super().clear_commands(guild=guild)
        if clear_app_commands_cache:
            self._clear_command_cache(guild=guild)


    async def sync(self, *, guild: Optional[Snowflake] = None) -> List[app_commands.AppCommand]:
        """Syncs the Application Commands"""
        
        res = await super().sync(guild=guild)
        self._update_cache(res, guild=guild)
        return res
