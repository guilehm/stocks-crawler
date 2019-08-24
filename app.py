import os

from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from stocks_spider import StockSpider


DEBUG = os.getenv('DEBUG', False)
MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/stocksCrawler')
CRAWLER_EMAIL = os.getenv('CRAWLER_EMAIL')
CRAWLER_PASSWORD = os.getenv('CRAWLER_PASSWORD')

app = Flask(__name__)
app.config['MONGO_URI'] = MONGODB_URI

mongo = PyMongo(app)
db = mongo.db
stocks_collection = db.stocks
stocks_analysis_collection = db.stocksAnalysis


def convert_id(document):
    document['_id'] = str(document['_id'])
    return document


@app.route('/')
def index():
    stocks = [convert_id(stock) for stock in stocks_collection.find()]
    return jsonify(stocks)


if __name__ == '__main__':
    app.run(debug=True)
