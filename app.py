import os

from flask import Flask, jsonify
from flask_pymongo import PyMongo

MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/stocksCrawler')

app = Flask(__name__)
app.config['MONGO_URI'] = MONGODB_URI

mongo = PyMongo(app)
db = mongo.db
stocks_collection = db.stocks_collection


@app.route('/')
def index():
    stocks = [stock for stock in stocks_collection.find()]
    return jsonify(stocks)


if __name__ == '__main__':
    app.run(debug=True)
