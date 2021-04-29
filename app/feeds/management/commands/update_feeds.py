#!/usr/bin/env python3
import logging

from django.core.management.base import BaseCommand

from feeds.utils.news_crawler import update_all_feeds

import time

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Update all feeds"

    def handle(self, *args, **options):

        t0 = time.time()
        logger.info("Updating feeds..")
        update_all_feeds()
        t1 = time.time()
        logger.info(f"Done. Took {t1 - t0:.2f}s")
