#!/usr/bin/env python3
from pathlib import Path
import requests
import sys
import time

from bs4 import BeautifulSoup
import feedparser

import logging
logger = logging.getLogger(__name__)

# 1. Load os first
import os  # NOQA

app_base_dir = Path(__file__).parent.parent
sys.path.append(str(app_base_dir))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'frontpage.settings')

# 2. Load django second
# import django  # NOQA
# django.setup()

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
    logger.info(f"Registering {title}")
    new_feed = Feed(url=url, title=title)
    new_feed.save()


def build_date_str(update_parsed):
    return time.strftime('%Y-%m-%dT%H:%M:%SZ', update_parsed)


def update_feed_by_id(_id):
    feed = Feed.objects.get(pk=_id)

    Article.objects.filter(feed=feed).delete()
    num_items_deleted = Article.objects.filter(feed=feed).delete()
    # logger.info(f"Deleted {num_items_deleted[0]} articles for feed {feed}")

    entries = feedparser.parse(feed.url).entries
    for e in entries:
        article = Article(url=e["link"],
                          title=e["title"],
                          feed=feed,
                          date_published=build_date_str(e['updated_parsed']))
        article.save()
    logger.info(f"Found {len(entries)} entries for {feed.title}")


def update_all_feeds():
    logger.info("Updating all the feeds")
    feeds = Feed.objects.all()
    for f in feeds:
        update_feed_by_id(f.id)
