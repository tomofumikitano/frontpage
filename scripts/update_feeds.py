#!/usr/bin/env python3
import sys
import time
from bs4 import BeautifulSoup
import feedparser
import requests

import re

# 1. Load os first
import os  # NOQA
current_dir = os.path.dirname(os.path.realpath(__file__))

parent_dir = re.search('.+/', current_dir).group(0)
print(f"Adding {parent_dir} to sys.path")

sys.path.append(parent_dir)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'frontpage.settings')

# 2. Load django second
import django  # NOQA
django.setup()

# 3. Load model
from feeds.models import Feed, Article  # NOQA


# def add_feed_by_url(url, title=None):
#     feeds = Feed.objects.all()
#     urls = [feed.url for feed in feeds]
#     if url in urls:
#         raise Exception("feed already exists.")
#
#     if not title:
#         res = requests.get(url)
#         if res.status_code == 200:
#             soup = BeautifulSoup(res.content, 'html.parser')
#             title = soup.title.text
#     print(f"Registering {title}")
#     new_feed = Feed(url=url, title=title)
#     new_feed.save()


def build_date_str(update_parsed):
    return time.strftime('%Y-%m-%dT%H:%M:%SZ', update_parsed)


def update_feed_by_id(_id):
    feed = Feed.objects.get(pk=_id)
    print(f"Updating {feed.title}..")
    existing_articles = Article.objects.filter(feed=feed)
    existing_urls = [a.url for a in existing_articles]
    entries = feedparser.parse(feed.url).entries
    print(f"Found {len(entries)} entries")
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
    print(f"Added {count} new items.")


if __name__ == "__main__":
    # if len(sys.argv) > 1:
    #     for url in sys.argv[1:]:
    #         print(url)
    #         add_feed_by_url(url)
    entries = Feed.objects.all()
    for f in entries:
        update_feed_by_id(f.id)
