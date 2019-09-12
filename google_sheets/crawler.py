import logging
import os
import pickle
import sys
from datetime import datetime, timedelta
from decimal import Decimal

import requests
from bson.decimal128 import Decimal128
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from requests.exceptions import RequestException

from google_sheets.models import Stock, format_value, headers_data

SCOPES = ('https://www.googleapis.com/auth/spreadsheets.readonly',)
SPREADSHEET_ID = os.getenv('SPREADSHEET_ID')
RANGE_NAME = os.getenv('RANGE_NAME')
TOKEN_PICKLE_PATH = os.getenv('TOKEN_PICKLE_PATH')

logging.basicConfig(stream=sys.stdout, level=logging.INFO)


class SheetCrawler:
    def __init__(self, sheet_id=SPREADSHEET_ID, range_name=RANGE_NAME, scopes=SCOPES, db=None):
        self.sheet_id = sheet_id
        self.range_name = range_name
        self.scopes = scopes
        self.authenticated = False
        self.service = None
        self.sheet = None
        self.result = None
        self.values = None
        self.stocks = None
        self.db = db

    def _authenticate(self):
        if not TOKEN_PICKLE_PATH:
            message = 'Could not authenticate. Token Pickle Path is missing'
            logging.error(message)
            raise Exception(message)
        else:
            logging.info('Token Pickle path was found.')
            response = requests.get(TOKEN_PICKLE_PATH)
            try:
                response.raise_for_status()
            except RequestException:
                message = 'Token Pickle file could not be downloaded.'
                logging.error(message)
                raise
            token_content = response.content
            creds = pickle.loads(token_content)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())

        self.service = build('sheets', 'v4', credentials=creds)
        self.authenticated = True
        return self.authenticated

    def save_data(self, data, collection, has_decimals=False):
        def convert_decimal(doc):
            for key, value in doc.items():
                if type(value) == Decimal:
                    doc[key] = Decimal128(value)
            return doc

        if not self.db:
            logging.error('Could not save data. Please choose a database')
            return
        collection = self.db[collection]
        many = not isinstance(data, dict) and len(data) > 1

        if many:
            if not has_decimals:
                return collection.insert_many(data)
            return collection.insert_many([convert_decimal(d) for d in data])
        if not has_decimals:
            return collection.insert_one(data)
        return collection.insert_one(convert_decimal(data))

    def get_values(self):
        if not self.authenticated:
            self._authenticate()
        logging.info('Calling sheets API')
        self.sheet = self.service.spreadsheets()
        self.result = self.sheet.values().get(
            spreadsheetId=SPREADSHEET_ID,
            range=RANGE_NAME,
        ).execute()
        self.values = self.result.get('values', [])
        return self.values

    def get_stock_data(self, save=False, as_dict=False, force_update=False):
        data = self.values
        if force_update:
            data = None
        if not data:
            data = self.get_values()
        if not data:
            raise Exception('No data found')
        time = datetime.utcnow() - timedelta(hours=3)
        formatted_values = [[format_value(method, value) for method, value in zip(
            headers_data.values(), row,
        )] for row in data][1:]
        self.stocks = [Stock(*values, time.isoformat()) for values in formatted_values]
        if save:
            self.save_data(
                [stock._asdict() for stock in self.stocks],
                'stocksSheet',
                has_decimals=True
            )
        if as_dict:
            return [stock._asdict() for stock in self.stocks]
        return self.stocks
