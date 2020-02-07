import os
from scrapy.selector import Selector
import requests
import sys
import logging

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.Formatter('%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s')
URL = os.getenv('VALOR_TWITTER_URL', 'https://twitter.com/valorinveste/')


class TwitterCrawler:
    def __init__(self, url=URL):
        self.url = url
        self.response = None

    def get_response(self):
        response = requests.get(self.url)
        try:
            response.raise_for_status()
            self.response = Selector(text=response.text)
        except requests.RequestException:
            logging.exception(
                'Could not request to Valor Invest Twitter URL',
                exc_info=True,
            )
        return self.response

c = TwitterCrawler()
r = c.get_response()