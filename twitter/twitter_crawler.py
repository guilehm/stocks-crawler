import logging
import os
import sys
from datetime import datetime, timedelta

import requests
from pymongo import MongoClient
from scrapy.selector import Selector

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.Formatter('%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s')

USERNAMES = os.getenv('TWITTER_USERNAMES', 'valorinveste infomoney')
MONGO_URL = 'mongodb://localhost:27017/'
DB_NAME = 'stocksCrawler'


class TwitterCrawler:
    def __init__(self, usernames=USERNAMES, mongo_url=MONGO_URL, db_name=DB_NAME, retry_writes='true'):
        self.mongo_client = MongoClient(f'{mongo_url}?retryWrites={retry_writes}')
        self.db = self.mongo_client[db_name]
        self.usernames = usernames.split()
        self.response = None
        self.base_url = 'https://twitter.com/{username}/'
        self.url = None

    def _get_response(self, username):
        url = self.base_url.format(username=username)
        self.url = url
        self.username = username
        response = requests.get(self.url)
        try:
            response.raise_for_status()
            self.response = Selector(text=response.text)
        except requests.RequestException:
            message = f'Could not request to {url}'
            logging.exception(
                message,
                exc_info=True,
            )
            raise
        return self.response

    def _create_tweets_data(self, tweets):
        return ({
            'source': self.url,
            'title': tweet.xpath('./text()[normalize-space()]').get('').strip(),
            'link': tweet.xpath('./a[@data-expanded-url]/@href').get(),
            'date': datetime.utcnow() - timedelta(hours=3),
        } for tweet in tweets)

    def get_tweets(self, save=True):
        self._get_response()
        if not self.response:
            return
        tweets = self.response.xpath(
            '//p[@class="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text"]'
        )
        tweets_data = self._create_tweets_data(tweets)
        if save:
            collection = self.db['tweets']
            for tweet in tweets_data:
                collection.update_many(
                    filter={'title': tweet['title']},
                    update={'$set': tweet},
                    upsert=True,
                )
        return [tweet for tweet in tweets_data]

    def get_all_tweets(self):
        self.get_tweets()
        return [tweet for tweet in self.db['tweets'].find()]

# c = TwitterCrawler()
# r = c.get_tweets()