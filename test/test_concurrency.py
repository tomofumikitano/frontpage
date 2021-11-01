#!/usr/bin/env python3
import os
from os.path import join, dirname
from dotenv import load_dotenv

import aiohttp
import asyncio
from bs4 import BeautifulSoup

NUM_CONCURRENT_REQ = 3

LOGIN_URL = "http://localhost:8000/feeds/login"

dotenv_path = join(dirname(__file__), "..", ".env")
load_dotenv(dotenv_path)

username = os.environ.get('LOCALHOST_USERNAME')
password = os.environ.get('LOCALHOST_PASSWORD')


async def login():
    async with aiohttp.ClientSession(headers={}) as session:
        resp = await session.get(LOGIN_URL)
        content = await resp.content.read(1024 * 1024)
        soup = BeautifulSoup(content, 'html.parser')

        csrfmiddlewaretoken = soup.select(
            '[name="csrfmiddlewaretoken"]')[0].get("value")

        form = {
            "username": username,
            "password": password,
            "csrfmiddlewaretoken": csrfmiddlewaretoken
        }
        resp = await session.post(LOGIN_URL, data=form)


async def main():
    requests = [login() for i in range(NUM_CONCURRENT_REQ)]
    await asyncio.gather(*requests)


if __name__ == "__main__":
    asyncio.run(main())
