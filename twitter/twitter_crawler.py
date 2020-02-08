import logging
import os
import sys
from datetime import datetime, timedelta

import requests
from pymongo import MongoClient
from scrapy.selector import Selector

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.Formatter('%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s')

USERNAMES = os.getenv('TWITTER_USERNAMES', 'infomoney xp valorinveste')
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

    def _create_tweets_data(self, headers, containers):
        tweets = zip(headers, containers)
        return ({
            'dataUserId': header.xpath('./a').attrib['data-user-id'],
            'avatar': header.xpath('./a/img[@src]/@src').get(),
            'username': self.username,
            'dataTime': header.xpath('./small[@class="time"]/a/span/@data-time').get(),
            'dataTitle': header.xpath('./small[@class="time"]/a/@title').get(),
            'source': self.url,
            'title': ''.join(container.xpath('string()').getall()),
            # 'title': container.xpath('./text()[normalize-space()]').get('').strip(),
            'link': container.xpath('./a[@data-expanded-url]/@href').get(),
            'dateExtract': datetime.utcnow() - timedelta(hours=3),
        } for header, container in tweets)

    def get_tweets(self, username, save=True):
        self._get_response(username)
        if not self.response:
            return
        tweets_header = self.response.xpath(
            '//div[@class="content"]/div[@class="stream-item-header"]'
        )
        tweets_container = self.response.xpath(
            '//p[@class="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text"]'
        )
        tweets_data = self._create_tweets_data(tweets_header, tweets_container)
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
        for username in self.usernames:
            self.get_tweets(username)
        return [tweet for tweet in self.db['tweets'].find()]
