from decimal import Decimal

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