"""An example of using Strava.get_strava_nickname_from_uri from async_class package"""
import asyncio
import os

from typing import List, NoReturn
from dotenv import load_dotenv

import async_strava


def read_file(file_name='strava_uris.txt'):
    """
    Generator, which yield's file line by line

    :param file_name: file path
    """
    with open(file_name, 'r') as file:
        for row in file:
            yield row.rstrip('\n')


async def get_nicknames(strava_obj) -> List[str]:
    """
    Asynchronously retrieves nicknames from links in a 'strava_uris.txt' file

    :param strava_obj: instance of the Strava class

    :return: list of users nicknames, if uri is invalid - item will be ''
    """
    semaphore = asyncio.Semaphore(200)  # works as a resource counter
    async with semaphore:
        # # you can use synchronous reading, it's just my own "night" preference
        # loop = asyncio.get_event_loop()
        # uris_generator = await loop.run_in_executor(None, read_file, 'strava_uris.txt')
        uris_generator = read_file()
        tasks = [asyncio.create_task(strava_obj.get_strava_nickname_from_uri(uri)) for uri in uris_generator]

        results: list = await asyncio.gather(*tasks)
        return results


async def main() -> NoReturn:
    """Example executor"""
    _login: str = os.getenv('LOGIN')
    _password: str = os.getenv('PASSWORD')

    async with async_strava.strava_connector(_login, _password) as strava_obj:
        nicknames: list = await get_nicknames(strava_obj)
        print(nicknames)
        # await get_nicknames(strava_obj)
        # await get_nicknames(strava_obj)
        # await get_nicknames(strava_obj)
        # await get_nicknames(strava_obj)


if __name__ == '__main__':
    load_dotenv()

    asyncio.run(main())