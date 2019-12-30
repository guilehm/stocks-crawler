import logging
import os
import sys

import requests
from requests.models import PreparedRequest

STOCK_TIME_SERIES_ENDPOINT = os.getenv('STOCK_TIME_SERIES_ENDPOINT')
STOCK_TIME_SERIES_TOKEN = os.getenv('STOCK_TIME_SERIES_TOKEN')

logging.basicConfig(stream=sys.stdout, level=logging.INFO)


class StockTimeSeries:
    def __init__(self):
        self.base_url = STOCK_TIME_SERIES_ENDPOINT
        self.token = STOCK_TIME_SERIES_TOKEN
        self.response = None

    def get_response(self, **params):
        endpoint = f'{self.base_url}/query'
        prepared_url = PreparedRequest().prepare_url(endpoint, params).url
        response = requests.get(prepared_url)
        try:
            response.raise_for_status()
        except requests.RequestException:
            logging.error('Could not request to the API', exc_info=True)
            raise

        self.response = response
        return self.response.json()
