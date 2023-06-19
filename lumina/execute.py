import discord

from extensions import load_all_extensions
from lumina import get_config

bot = discord.Bot()


@bot.event
async def on_connect():
    try:
        await load_all_extensions(bot=bot)
        await bot.sync_commands()
    except Exception as e:
        raise e


@bot.event
async def on_ready():
    print("Ready to go! Logged in as", bot.user)


if __name__ == "__main__":
    __token__ = get_config("MAIN", "token")
    bot.run(__token__)
