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


@app.route('/stocks/', methods=['GET', 'POST'])
def index():
    if request.method != 'POST':
        stocks = [stock for stock in stocks_collection.find()]
    else:
        if not CRAWLER_EMAIL or not CRAWLER_PASSWORD:
            return jsonify({
                'error': True,
                'message': 'Credentials not set',
            })
        uri_data = MONGODB_URI.rsplit('/', 1)
        db_name = uri_data[-1]
        mongo_url = ''.join(uri_data[:-1])
        spider = StockSpider(
            CRAWLER_EMAIL, CRAWLER_PASSWORD, mongo_url=mongo_url, db_name=db_name,
        )
        stocks = spider.parse_stocks(save=True)
    return jsonify([convert_id(stock) for stock in stocks])


if __name__ == '__main__':
    app.run(debug=DEBUG)
