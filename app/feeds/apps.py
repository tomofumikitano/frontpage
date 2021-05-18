import sys
from django.conf import settings
from django.apps import AppConfig


import logging
logging.basicConfig(level=logging.INFO,
                    format="[%(asctime)s] %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S")
logger = logging.getLogger(__name__)


def start_scheduler():
    from django_apscheduler.jobstores import DjangoJobStore
    from apscheduler.triggers.cron import CronTrigger
    from apscheduler.schedulers.background import BackgroundScheduler

    from .utils.news_crawler import update_all_feeds
    update_all_feeds()

    scheduler = BackgroundScheduler(timezone=settings.TIME_ZONE)
    scheduler.add_jobstore(DjangoJobStore(), "default")

    scheduler.add_job(
        update_all_feeds,
        trigger=CronTrigger(hour="*", minute="*/5"),
        id="update_all_feeds",  # The `id` assigned to each job MUST be unique
        max_instances=1,
        replace_existing=True,
    )
    logger.info("Added job 'update_all_feeds'.")

    try:
        logger.info("Starting scheduler...")
        scheduler.start()
    except KeyboardInterrupt:
        logger.info("Stopping scheduler...")
        scheduler.shutdown()


class FeedsConfig(AppConfig):
    name = 'feeds'
    default_auto_field = 'django.db.models.BigAutoField'

    def ready(self):
        if 'runserver' in sys.argv:
            start_scheduler()
