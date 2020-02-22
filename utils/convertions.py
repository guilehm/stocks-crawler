from decimal import Decimal

from bson.decimal128 import Decimal128


def convert_decimal(doc):
    for key, value in doc.items():
        if type(value) == Decimal:
            doc[key] = Decimal128(value)
    return doc
