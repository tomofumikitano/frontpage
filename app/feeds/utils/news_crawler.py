#!/usr/bin/env python3
import concurrent.futures
import datetime
from pathlib import Path
import requests
import sys
import time
import timeit

from django.utils import timezone
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

    try:
        rss = feedparser.parse(feed.url)
        entries = rss.entries
        logger.info(f"Found {len(entries)} entries for {feed.title}")

        if len(entries) > 0:
            num_items_deleted = Article.objects.filter(feed=feed).delete()
            logger.info(f"Deleted {num_items_deleted[0]} articles for {feed}")

            for e in entries:
                article = Article(url=e["link"],
                                  title=e["title"],
                                  feed=feed,
                                  date_published=build_date_str(e['updated_parsed']))
                article.save()
    except Exception:
        logger.error(f"Error updating feed {feed}")

    feed.date_updated = timezone.now() 
    feed.save()


# def update_all_feeds(user_id):

    start = timeit.default_timer()

    logger.info("Updating all the feeds..")
    # feeds = Feed.objects.filter(user=user_id).filter(date_updated__lte=timezone.now() - datetime.timedelta(minutes=10))
    feeds = Feed.objects.filter(date_updated__lte=timezone.now() - datetime.timedelta(minutes=10))

    if len(feeds) > 0:
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            futures = {executor.submit(update_feed_by_id, feed.id): feed for feed in feeds}
            for future in concurrent.futures.as_completed(futures):
                pass

        end = timeit.default_timer()
        logger.info(f"Updated all the feeds. Took {end - start:.3}s")
    else:
        logger.info("No feeds to update.")
