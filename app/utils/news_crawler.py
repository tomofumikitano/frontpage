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
    existing_articles = Article.objects.filter(feed=feed)
    # Keep old articles 
    # TODO - What if the artcle get updated with same URL ??
    existing_urls = [a.url for a in existing_articles]
    entries = feedparser.parse(feed.url).entries
    count = 0
    for e in entries:
        if e["link"] not in existing_urls:
            article = Article(url=e["link"],
                              title=e["title"],
                              feed=feed,
                              date_published=build_date_str(e['updated_parsed']))
            article.save()
            count += 1
    logger.info(f"Found {len(entries)} ({count} new) entries for {feed.title}")


def update_all_feeds():
    logger.info("Updating all the feeds")
    feeds = Feed.objects.all()
    for f in feeds:
        update_feed_by_id(f.id)


if __name__ == "__main__":
    update_all_feeds()
