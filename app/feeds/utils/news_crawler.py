#!/usr/bin/env python3
import concurrent.futures
import datetime
import os
from pathlib import Path
import requests
import sys
import time
import timeit
from threading import Lock
lock = Lock()

from django.utils import timezone
from bs4 import BeautifulSoup
import feedparser

import logging
logger = logging.getLogger(__name__)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'frontpage.settings')

sys.path.append(str(Path(__file__).parent.parent))
from feeds.models import Feed, Article  # NOQA

FEED_UPDATE_INTERVAL_MIN = 5 
FEED_UPDATE_MAX_WORKERS = 10


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
        start = timeit.default_timer()
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
        end = timeit.default_timer() 
        logger.info(f"Updated feed: {feed.title}. Took {end - start:.3}s")

    except Exception:
        logger.error(f"Error updating feed {feed}")

    feed.date_updated = timezone.now()
    feed.save()


def update_all_feeds(user_id):
    
    lock.acquire()
    start = timeit.default_timer()

    logger.info("Updating all the feeds..")
    feeds = Feed.objects.filter(user=user_id).filter(date_updated__lte=timezone.now(
    ) - datetime.timedelta(minutes=FEED_UPDATE_INTERVAL_MIN))

    if len(feeds) > 0:
        for feed in feeds:
            feed.date_updated = timezone.now()
            feed.save()

        with concurrent.futures.ThreadPoolExecutor(max_workers=FEED_UPDATE_MAX_WORKERS) as executor:
            futures = {executor.submit(
                update_feed_by_id, feed.id): feed for feed in feeds}
            for future in concurrent.futures.as_completed(futures):
                pass

        end = timeit.default_timer()
        logger.info(f"Updated all the feeds. Took {end - start:.3}s")
    else:
        logger.info("No feeds to update.")
    lock.release()
