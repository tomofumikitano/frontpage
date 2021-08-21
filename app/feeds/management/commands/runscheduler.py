#!/usr/bin/env python3
import logging

from apscheduler.schedulers.blocking import BlockingScheduler 
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django.conf import settings
from django_apscheduler.jobstores import DjangoJobStore

# from feeds.utils.news_crawler import update_all_feeds


logging.basicConfig(level=logging.INFO,
                    format="[%(asctime)s] %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S")
logger = logging.getLogger(__name__)


def run_scheduler(force_update_on_strtup=False):
    if force_update_on_strtup:
        # update_all_feeds()

    scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
    scheduler.add_jobstore(DjangoJobStore(), "default")

    # scheduler.add_job(
    #     update_all_feeds,
    #     trigger=CronTrigger(hour="*", minute="*/15"),
    #     id="update_all_feeds",  # The `id` assigned to each job MUST be unique
    #     max_instances=1,
    #     replace_existing=True,
    # )

    try:
        logger.info("Starting scheduler...")
        scheduler.start()
    except KeyboardInterrupt:
        logger.info("Stopping scheduler...")
        scheduler.shutdown()


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        run_scheduler()
