import logging
import os
import sys
from datetime import datetime, timedelta

import requests
from pymongo import MongoClient
from scrapy.selector import Selector

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.Formatter('%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s')

URL = os.getenv('VALOR_TWITTER_URL', 'https://twitter.com/valorinveste/')
MONGO_URL = 'mongodb://localhost:27017/'
DB_NAME = 'stocksCrawler'


class TwitterCrawler:
    def __init__(self, url=URL, mongo_url=MONGO_URL, db_name=DB_NAME, retry_writes='true'):
        self.mongo_client = MongoClient(mongo_url + f'?retryWrites={retry_writes}')
        self.db = self.mongo_client[db_name]
        self.url = url
        self.response = None
        self.tweets = set()

    def _get_response(self):
        response = requests.get(self.url)
        try:
            response.raise_for_status()
            self.response = Selector(text=response.text)
        except requests.RequestException:
            message = 'Could not request to Valor Investe Twitter URL'
            logging.exception(
                message,
                exc_info=True,
            )
            return {'error': True, 'message': message}
        return self.response

    def _create_tweets_data(self, tweets):
        return ({
            'title': tweet.xpath('./text()').get(),
            'link': tweet.xpath('./a').attrib['data-expanded-url'] if tweet.xpath('./a') else None,
            'date': datetime.utcnow() - timedelta(hours=3),
        } for tweet in tweets)

    def get_tweets(self, save=True):
        self._get_response()
        tweets = self.response.xpath(
            '//p[@class="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text"]'
        )
        tweets_data = self._create_tweets_data(tweets)
        if save:
            collection = self.db['tweets']
            for tweet in tweets_data:
                collection.update_many(
                    filter={'link': tweet['link']},
                    update={'$set': tweet},
                    upsert=True,
                )
        return [tweet for tweet in tweets_data]

    def get_all_tweets(self):
        self.get_tweets()
        return [tweet for tweet in self.db['tweets'].find()]
