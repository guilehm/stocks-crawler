import logging
import os
import sys

import requests
from requests import RequestException
from requests.models import PreparedRequest
from scrapy.selector import Selector

logging.basicConfig(stream=sys.stdout, level=logging.INFO)

FUNDS_EXPLORER_URL = os.getenv('FUNDS_EXPLORER_URL')


class FundsCrawler:
    def __init__(self, base_url=FUNDS_EXPLORER_URL, db=None):
        self.base_url = base_url
        self.response = None
        self.db = db

    def _get_response(self, endpoint, **params):
        url = f'{self.base_url}/{endpoint}'
        prepared_request = PreparedRequest()
        prepared_request.prepare_url(url, params)
        response = requests.get(prepared_request.url)
        try:
            response.raise_for_status()
        except RequestException:
            logging.error('Could not request', exc_info=True)
        else:
            self.response = Selector(text=response.text)
        return self.response
