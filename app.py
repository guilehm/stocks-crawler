import os

from flask import Flask, jsonify
from flask_pymongo import PyMongo

MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/stocksCrawler')

app = Flask(__name__)
app.config['MONGO_URI'] = MONGODB_URI

mongo = PyMongo(app)
db = mongo.db
stocks_collection = db.fundamentalistAnalysis


def convert_id(document):
    document['_id'] = str(document['_id'])
    return document


@app.route('/')
def index():
    stocks = [convert_id(stock) for stock in stocks_collection.find()]
    return jsonify(stocks)


if __name__ == '__main__':
    app.run(debug=True)
