# -*- coding: utf-8 -*-

import time

from flask import Flask, jsonify, request

from models.exchange_rate import ExchangeRate

app = Flask(__name__)


@app.route('/')
def index():
    return jsonify({
        'say': 'hello my worksapce api - flask'
    })


@app.route('/get_exchange_rate_history')
def get_exchange_rate_history():
    data = {}
    target_list = ["USD", "EUR"]
    query = ExchangeRate.select(ExchangeRate.timestamp, ExchangeRate.rate) \
        .where(ExchangeRate.source == "CNY")
    for target in target_list:
        cur_query = query.where(ExchangeRate.target == target)
        for item in cur_query.order_by(ExchangeRate.timestamp):
            target = target
            target_list = data.setdefault(target, [])
            target_list.append({
                'timestamp': time.mktime(item.timestamp.timetuple()),
                'rate': item.rate
            })
    return jsonify(data)


if __name__ == '__main__':
    app.run(port=10001, debug=True)
