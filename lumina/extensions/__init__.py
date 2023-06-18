import discord
from discord.errors import ExtensionNotLoaded, ExtensionNotFound, ExtensionFailed

from typing import List

import logging
import os


def __get_extensions() -> List[str]:
    return [
        f'extension.{_.split(".py")[0]}'
        for _ in os.listdir("extensions")
        if not _.startswith("__")
    ]


def load_all_extensions(bot: discord.Bot) -> None:
    if extensions := __get_extensions():
        bot.load_extensions(*extensions)
        print(f"Extensions loaded successfully: {extensions}")


def reload_extensions(bot: discord.Bot) -> List[str]:
    faulty_extensions = []
    if extensions := __get_extensions():
        for extension in extensions:
            try:
                bot.reload_extension(extension)
            except ExtensionNotLoaded:
                # load the extension anyway, this means that a new extension has been added
                bot.load_extensions(extension)
            except ExtensionNotFound:
                logging.error(
                    f"Couldn't find extension: '{extension}'. Ignoring it instead."
                )
                faulty_extensions.append(extension)
    return faulty_extensions
