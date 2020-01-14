import logging
import os
import sys
from json import JSONDecodeError

import requests
from requests.models import PreparedRequest

STOCK_TIME_SERIES_ENDPOINT = os.getenv('STOCK_TIME_SERIES_ENDPOINT')
STOCK_TIME_SERIES_TOKEN = os.getenv('STOCK_TIME_SERIES_TOKEN')
VALIDATION_KEYS = ['Global Quote', 'Meta Data']

logging.basicConfig(stream=sys.stdout, level=logging.INFO)


class StockTimeSeries:
    def __init__(self):
        self.base_url = STOCK_TIME_SERIES_ENDPOINT
        self.token = STOCK_TIME_SERIES_TOKEN
        self.response = None
        self.status_code = None

    def _validate_api(self):
        if not self.token or not self.base_url:
            raise Exception('Could not validate Stock Time Series credentials.')
        return True

    def _validate_response(self, response):
        try:
            json_response = response.json()
        except JSONDecodeError:
            message = 'Could not request to the API.'
            logging.error(message, exc_info=True)
            self.response = {'error': True, 'message': message}
            self.status_code = 500
            return self.response

        if not any([key in json_response for key in VALIDATION_KEYS]):
            message = 'Bad Request.'
            self.response = {'error': True, 'message': message}
            self.status_code = 400
            return self.response

        self.response = json_response
        self.status_code = 200
        return self.response

    def _build_url(self, **params):
        endpoint = f'{self.base_url}/query'
        parameters = {
            'function': 'TIME_SERIES_INTRADAY',
            'outputsize': 'full',
            'apikey': self.token,
        }
        parameters.update(**params)
        prepared_request = PreparedRequest()
        prepared_request.prepare_url(endpoint, parameters)
        return prepared_request.url

    def get_response(self, **params):
        self._validate_api()
        url = self._build_url(**params)
        self.status_code = None
        self.response = self._validate_response(requests.get(url))
        return self.response
