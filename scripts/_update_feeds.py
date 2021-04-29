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
sys.path.append(app_base_dir)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'frontpage.settings')

# 2. Load django second
import django  # NOQA
django.setup()

# 3. Load model
from feeds.models import Feed, Article  # NOQA


def build_date_str(update_parsed):
    return time.strftime('%Y-%m-%dT%H:%M:%SZ', update_parsed)


def update_feed_by_id(_id):
    feed = Feed.objects.get(pk=_id)
    existing_articles = Article.objects.filter(feed=feed)
    existing_urls = [a.url for a in existing_articles]
    entries = feedparser.parse(feed.url).entries
    # print(f"Found {len(entries)} entries")
    count = 0
    for e in entries:
        url = e["link"]
        title = e["title"]
        date_published = build_date_str(e['updated_parsed'])
        if e["link"] not in existing_urls:
            article = Article(url=url, title=title, feed=feed,
                              date_published=date_published)
            article.save()
            count += 1
    print(f"{count} new items for {feed.title}")


if __name__ == "__main__":
    entries = Feed.objects.all()
    for f in entries:
        update_feed_by_id(f.id)
