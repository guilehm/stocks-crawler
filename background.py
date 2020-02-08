import logging
import sys

from apscheduler.schedulers.background import BackgroundScheduler

from app import TWITTER_CRAWLER

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
scheduler = BackgroundScheduler()


@scheduler.scheduled_job('interval', minutes=5)
def fetch_tweets():
    logging.info('Fetching Tweets')
    TWITTER_CRAWLER.get_tweets()


scheduler.start()


while True:
    pass
