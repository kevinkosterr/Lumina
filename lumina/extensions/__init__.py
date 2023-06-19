import discord
import os

from typing import List, Tuple


def __get_extensions() -> Tuple[List[str], List[str]]:
    extensions = [f'{_.split(".py")[0]}' for _ in os.listdir('extensions') if not _.startswith("__")]
    return [f'extensions.{_}' for _ in extensions], extensions


async def load_all_extensions(bot: discord.Bot) -> None:
    extensions, extension_names = __get_extensions()
    bot.load_extensions(*extensions)
    print(f"Extensions loaded successfully: {extension_names}")
