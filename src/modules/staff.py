"""
All Staff-Related Commands
"""

import base64
import inspect
import selfcord as discord
from selfcord.ext import commands

from ..bot import TheBot


class Staff(commands.Cog):
    """Contains All the Staff-Related Commands"""

    def __init__(self, bot: TheBot):
        self.bot = bot

    
    @commands.command(
        name="saaccept",
        aliases=['saapprove']
    )
    @commands.guild_only()
    async def sa_accept(self, ctx: commands.Context, user: discord.Member):
        """Sends the Response for Accepting a Vouch

        Parameters
        ----------
        user:
            The User to Ping.
        """

        await ctx.message.delete()
        await ctx.send(inspect.cleandoc(f"""
            {user.mention},

            Your Vouch has been **Approved!**

            If you Need Anything Else, Let us Know.
            Have a Good Day/Night!
        """))

    
    @commands.command(
        name="sadeny"
    )
    @commands.guild_only()
    async def sa_deny(self, ctx: commands.Context, user: discord.Member, reason: str):
        """Sends the Response for Denying a Vouch

        Parameters
        ----------
        user:
            The User to Ping.
        reason:
            The Denial Reason.
        """

        await ctx.message.delete()
        await ctx.send(inspect.cleandoc(f"""
            {user.mention},

            Your Vouch has been **Denied!**
            > {reason}
        """))
    

    @commands.command(
        name="recovery"
    )
    @commands.guild_only()
    async def recovery(self, ctx: commands.Context, user: discord.Member = None):
        """Sends the Response for Recovery Proofs

        Parameters
        ----------
        user:
            The User to Ping.
        """

        await ctx.message.delete()

        msg = inspect.cleandoc(f"""
            **Send Payment Proofs for the Vouches Given Above.**
            The Proofs MUST Include the Following:
            > - The Date
            > - The Time
            And All Proofs MUST be __NEW__ Screenshots, Not Old Ones.
                               
            Reply to Each Vouch Embed with your Proofs.
        """)

        if user:
            msg = f"{user.mention},\n\n{msg}"

        await ctx.send(msg)

    
    @commands.command(
        name="recoverydone",
        aliases=['recoverywait']
    )
    @commands.guild_only()
    async def recoverydone(self, ctx: commands.Context):
        """Sends the Response for Recovery Wait"""

        await ctx.message.delete()
        await ctx.send(inspect.cleandoc(f"""
            **Thanks for Submitting Proofs!**
                                        
            We will Review it within the Next 12 Hours.
        """))


    @commands.command(
        name="recoveryadmin"
    )
    @commands.guild_only()
    async def recoveryadmin(self, ctx: commands.Context, old: discord.User, new: discord.User):
        """Sends the Response to Ping Admins for Transfer

        Parameters
        ----------
        old:
            The Account to Transfer From.
        new:
            The Account to Transfer To.
        """

        await ctx.message.delete()

        admin_role = ctx.guild.get_role(888763368943534101)
        await ctx.send(inspect.cleandoc(f"""
            `{old.id}` >>> `{new.id}`

            **Provided Proof:**
            > - Payment Proofs

            {admin_role.mention}
        """))


    @commands.command(
        name="antispam"
    )
    @commands.guild_only()
    async def antispam(self, ctx: commands.Context, user: discord.Member):
        """Sends the Response for Guild-Blacklists

        Parameters
        ----------
        user:
            The User to Ping.
        """

        await ctx.message.delete()

        appeal_channel = ctx.guild.get_channel(888763422446084116)
        await ctx.send(inspect.cleandoc(f"""
            {user.mention},

            It Looks Like your Server has been **Blacklisted** due to **Anti-Spam**.

            If you Believe this is a Mistake, Please Open an Appeal:
            > - {appeal_channel.mention}
            > - Select `Server Bans`

            If you Need Anything Else, Let us Know.
            Have a Good Day/Night!
        """))

    
    @commands.command(
        name="invalidproof"
    )
    @commands.guild_only()
    async def invalidproof(self, ctx: commands.Context, user: discord.Member):
        """Sends the Response for Invalid Proofs

        Parameters
        ----------
        user:
            The User to Ping.
        """

        await ctx.message.delete()
        await ctx.send(inspect.cleandoc(f"""
            {user.mention},

            Your Current-Proofs seem to be Invalid.
            Please Make-Sure you are Following this Guide:
        """))
        await ctx.send("=uncropped") # hehe

    
    @commands.command(
        name="recoverystart",
        aliases=['recoveryproc']
    )
    @commands.guild_only()
    async def recoverystart(self, ctx: commands.Context, user: discord.Member):
        """Starts the Recovery Ticket

        Parameters
        ----------
        user:
            The User to Ping.
        """

        await ctx.message.delete()
        await ctx.send(f"=add {user.id}")
        await ctx.send(f"+vouches {user.mention}")

        resp = await self.bot.session.get(
            base64.b64decode("aHR0cHM6Ly9hcGkuc2NhbW1lcmFsZXJ0Lm9yZy9zd2lmdC1yZWNvdmVyeS1tZXNzYWdl").decode(),
            headers={
                'User-Agent': 'swift-staff-helper/4.0 (https://github.com/ScammerAlert/Swift-Staff-Helper)'
            }
        )
        msg = await resp.text()
        msg = msg.replace("@user", user.mention)
        msg = msg.replace("CHANNEL-ID", str(ctx.channel.id))
        await user.send(msg)


async def setup(bot: TheBot):
    await bot.add_cog(Staff(bot))
