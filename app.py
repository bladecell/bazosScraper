from flask import Flask, request, jsonify
from flask_cors import CORS
from BazosScraper import BazosScraper
import asyncio

app = Flask(__name__)
CORS(app)

@app.route('/api/search', methods=['GET'])
def search():
    search = request.args.get('search', '')
    location = request.args.get('location')
    distance = request.args.get('distance', '25')
    min_price = request.args.get('min_price')
    max_price = request.args.get('max_price')
    order = request.args.get('order')
    results_limit = request.args.get('results_limit')

    if min_price:
        min_price = int(min_price)
    if max_price:
        max_price = int(max_price)
    if order:
        order = int(order)
    if results_limit:
        results_limit = int(results_limit)

    scraper = BazosScraper(
        search=search,
        location=location,
        distance=distance,
        min_price=min_price,
        max_price=max_price,
        order=order,
        results_limit=results_limit
    )

    scraper.scrape()

    return jsonify(scraper.listings.to_dict_list())

@app.route('/api/async_search', methods=['GET'])
async def async_search():
    search = request.args.get('search', '')
    location = request.args.get('location')
    distance = request.args.get('distance', '25')
    min_price = request.args.get('min_price')
    max_price = request.args.get('max_price')
    order = request.args.get('order')
    results_limit = request.args.get('results_limit')

    if min_price:
        min_price = int(min_price)
    if max_price:
        max_price = int(max_price)
    if order:
        order = int(order)
    if results_limit:
        results_limit = int(results_limit)

    scraper = BazosScraper(
        search=search,
        location=location,
        distance=distance,
        min_price=min_price,
        max_price=max_price,
        order=order,
        results_limit=results_limit
    )

    await asyncio.to_thread(scraper.scrape)

    return jsonify(scraper.listings.to_dict_list())

if __name__ == '__main__':
    app.run()