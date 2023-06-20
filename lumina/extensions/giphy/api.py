import aiohttp
import json
import random

from typing import Dict


class GiphyError(RuntimeError):
    pass


class GiphyAPI:
    def __init__(self, api_key):
        self.__api_key = api_key

    @staticmethod
    async def _send_request(url: str) -> Dict:
        """Send a request to a given url."""
        async with aiohttp.ClientSession() as session:
            response = await session.get(url)
            return json.loads(await response.text())

    async def get_sticker(self) -> str:
        data = await self._send_request(f"https://api.giphy.com/v1/stickers/random?api_key={self.__api_key}")
        return data["data"]["embed_url"]

    async def __get_random_gif(self) -> str:
        """Get a random GIF.

        :return: url leading to GIF.
        """
        data = await self._send_request(f"https://api.giphy.com/v1/gifs/random?api_key={self.__api_key}")
        return data["data"]["images"]["original"]["url"]

    async def get_gif(self, query: str) -> str:
        """Get a GIF based on the query, if none is provided it will get a random GIF instead.

        :param query: search query, what kind of GIF the api should return.
        :return: GIF url based on the query.
        """
        if not query:
            return await self.__get_random_gif()
        offset, gif_choice = random.randint(0, 20), random.randint(0, 5)
        data = await self._send_request(
            f"https://api.giphy.com/v1/gifs/search?q={query}&api_key={self.__api_key}&limit=25&offset={offset}")
        response_data = data["data"]
        if not response_data:
            raise GiphyError("Something went wrong when trying to find a GIF for", query)
        try:
            return data["data"][gif_choice]["images"]["original"]["url"]
        except IndexError:
            return data["data"][0]["images"]["original"]["url"]
