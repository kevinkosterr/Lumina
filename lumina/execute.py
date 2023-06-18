import discord
from discord.ext import commands

from extensions import load_all_extensions, reload_extensions
from lumina import get_config

bot = discord.Bot()


@bot.slash_command(description="Reload all extensions. Will also load new extensions.")
@commands.has_role("Lumineer")
async def reload(ctx):
    errors = reload_extensions(bot=bot)
    if not errors:
        await ctx.send_response(
            ":white_check_mark: Successfully reloaded all extensions.", delete_after=3
        )
    else:
        await ctx.send_response(
            ":x: Some extensions couldn't be loaded, see logs for more details. :",
            delete_after=3,
        )


@bot.event
async def on_connect():
    try:
        load_all_extensions(bot=bot)
    except Exception as e:
        raise e


@bot.event
async def on_ready():
    print("Ready to go! Logged in as", bot.user)


if __name__ == "__main__":
    __token__ = get_config("MAIN", "token")
    bot.run(__token__)
