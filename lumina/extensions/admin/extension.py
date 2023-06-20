from discord.ext import commands
from discord import ApplicationContext


class AdminExtension(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="purge", description="Get rid of x amount of messages.")
    @commands.has_permissions(manage_messages=True)
    async def purge_command(self, ctx: ApplicationContext, amount: int) -> None:
        """Purge messages."""
        await ctx.send_response(f":fire: Burning {amount} message(s).")
        await ctx.channel.purge(limit=amount + 1)

    @commands.slash_command(name="sync", description="Synchronize the commands.")
    @commands.has_role("Lumineer")
    async def sync_command(self, ctx: ApplicationContext):
        """Synchronize all available commands."""
        await self.bot.sync_commands()
        await ctx.send_response(":robot: Synchronized commands", delete_after=3)
