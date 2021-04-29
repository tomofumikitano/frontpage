#!/usr/bin/env python3
import sys
import time
from bs4 import BeautifulSoup
import feedparser
import requests

import re
from pathlib import Path

# 1. Load os first
import os  # NOQA

app_base_dir = os.path.join(Path(__file__).parent.parent, 'app')
# print(f"Adding {app_base_dir} to sys.path")
sys.path.append(app_base_dir)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'frontpage.settings')

# 2. Load django second
import django  # NOQA
django.setup()

# 3. Load model
from feeds.models import Feed, Article  # NOQA


def add_feed_by_url(url, title=None):
    feeds = Feed.objects.all()
    urls = [feed.url for feed in feeds]
    if url in urls:
        raise Exception("feed already exists.")

    if not title:
        res = requests.get(url)
        if res.status_code == 200:
            soup = BeautifulSoup(res.content, 'html.parser')
            title = soup.title.text
    print(f"Registering {title}")
    new_feed = Feed(url=url, title=title)
    new_feed.save()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("python add_feed.py <feed_url..>")
        sys.exit()

    for url in sys.argv[1:]:
        print(url)
        add_feed_by_url(url)
