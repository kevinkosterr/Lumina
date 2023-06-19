import discord
from discord.ext import commands
from discord import ApplicationContext

from lumina import get_config

import aiohttp
import json
import random


class GiphyExtension(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.api_key = get_config("GIPHY", "api_key")

    @commands.slash_command(
        name="gif", description="Search for a random gif, or query for a gif."
    )
    async def gif_command(self, ctx: ApplicationContext, query: str = "") -> None:
        """Sends an API request to the GIPHY API based on the user input."""
        embed = discord.Embed(color=discord.Color.blue())
        error_msg = "Oops! :sob: Something went wrong trying to get your GIF."
        async with aiohttp.ClientSession() as session:
            msg = await ctx.send_response("Getting a GIF just for you...")
            if not query:
                url = f"https://api.giphy.com/v1/gifs/random?api_key={self.api_key}"
            else:
                # we'll provide an offset to make the results more varied when the bot is queried multiple times
                offset = random.randint(0, 300)
                url = f"https://api.giphy.com/v1/gifs/search?q={query}&api_key={self.api_key}&limit=25&offset={offset}"
                gif_choice = random.randint(0, 24)

            response = await session.get(url)
            data = json.loads(await response.text())
            try:
                _url = (data["data"]["images"]["original"]["url"] if not query else
                        data["data"][gif_choice]["images"]["original"]["url"])
            except KeyError:
                await msg.edit_original_response(content=error_msg)
                return
            embed.set_image(url=_url)

        await msg.edit_original_response(
            content="This is what I found, I hope you like it :pleading_face:",
            embed=embed,
        )
