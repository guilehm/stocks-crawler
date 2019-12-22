import os

STOCK_TIME_SERIES_ENDPOINT = os.getenv('STOCK_TIME_SERIES_ENDPOINT')
STOCK_TIME_SERIES_TOKEN = os.getenv('STOCK_TIME_SERIES_TOKEN')


class StockTimeSeries:
    def __init__(self):
        self.url = STOCK_TIME_SERIES_ENDPOINT
        self.token = STOCK_TIME_SERIES_TOKEN
