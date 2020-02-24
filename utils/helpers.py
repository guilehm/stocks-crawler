from decimal import Decimal
from flask import request
from bson.decimal128 import Decimal128


def convert_decimal_for_db(doc):
    for key, value in doc.items():
        if type(value) == Decimal:
            doc[key] = Decimal128(value)
    return doc


def convert_decimal_for_response(document):
    for key, value in document.items():
        if type(value) == Decimal:
            document[key] = float(value)
        elif type(value) == Decimal128:
            document[key] = float(str(value))
    return document


def convert_id(document):
    if document.get('_id'):
        document['_id'] = str(document['_id'])
    return document


def add_url(document):
    url_root = request.url_root
    code = document['url'].rsplit('/', 2)[-2]
    document['analysisUrl'] = f'{url_root}stocks/{code}/analysis/'
    return document
