#!/usr/bin/env python3
import aiohttp
import asyncio
from bs4 import BeautifulSoup


urls = [
    'https://frontpageshowcase.herokuapp.com/',
]


async def get_url(session, url):
    async with session.get(url) as res:
        text = await res.text()
        soup = BeautifulSoup(text, 'html.parser')
        return soup.title.text


async def main():

    async with aiohttp.ClientSession() as session:

        tasks = []
        for url in urls:
            tasks.append(asyncio.ensure_future(get_url(session, url)))

        results = await asyncio.gather(*tasks)
        for result in results:
            print(result)


if __name__ == "__main__":
    asyncio.run(main())
