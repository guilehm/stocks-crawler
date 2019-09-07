import logging
import os
import pickle
import sys

import requests
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from requests.exceptions import RequestException

from google_sheets.models import Stock

SCOPES = ('https://www.googleapis.com/auth/spreadsheets.readonly',)
SPREADSHEET_ID = os.getenv('SPREADSHEET_ID')
RANGE_NAME = os.getenv('RANGE_NAME')
TOKEN_PICKLE_PATH = os.getenv('TOKEN_PICKLE_PATH')

logging.basicConfig(stream=sys.stdout, level=logging.INFO)


class SheetCrawler:
    def __init__(self, sheet_id=SPREADSHEET_ID, range_name=RANGE_NAME, scopes=SCOPES):
        self.sheet_id = sheet_id
        self.range_name = range_name
        self.scopes = scopes
        self.authenticated = False
        self.service = None
        self.sheet = None
        self.result = None
        self.values = None
        self.stocks = None

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
                raise Exception(message)
            token_content = response.content
            creds = pickle.loads(token_content)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())

        self.service = build('sheets', 'v4', credentials=creds)
        self.authenticated = True
        return self.authenticated

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

    def get_stock_data(self):
        data = None
        if not self.values:
            data = self.get_values()
        if not data:
            raise Exception('No data found')

        self.stocks = [Stock(*row) for row in data]
        return self.stocks
