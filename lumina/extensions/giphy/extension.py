import discord
from discord.ext import commands
from discord import ApplicationContext

from lumina import get_config
from .api import GiphyAPI, GiphyError


class GiphyExtension(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.__api = GiphyAPI(api_key=get_config("GIPHY", "api_key"))

    @commands.slash_command(
        name="gif", description="Search for a random gif, or query for a gif."
    )
    async def gif_command(self, ctx: ApplicationContext, query: str = "") -> None:
        """Sends an API request to the GIPHY API based on the user input."""
        embed = discord.Embed(color=discord.Color.blue())
        error_msg = "Oops! :sob: Something went wrong trying to get your GIF."
        msg = await ctx.send_response("Getting a GIF just for you...")
        try:
            gif_url = await self.__api.get_gif(query)
        except (KeyError, GiphyError) as e:
            await msg.edit_original_response(content=error_msg)
            print(e)
            return
        embed.set_image(url=gif_url)

        await msg.edit_original_response(
            content="This is what I found, I hope you like it :pleading_face:",
            embed=embed,
        )

    @commands.slash_command(name="sticker", description="Request a random sticker")
    async def sticker_command(self, ctx: ApplicationContext):
        """Request a random sticker from GIPHY."""
        msg = await ctx.send_response("Getting a sticker just for you...")
        sticker_url = await self.__api.get_sticker()
        await msg.edit_original_response(content=sticker_url)
