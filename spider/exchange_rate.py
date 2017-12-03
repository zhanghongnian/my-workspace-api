# -*- coding: utf-8 -*-

import time
import requests
from datetime import datetime, timedelta

from peewee import fn

from models.exchange_rate import ExchangeRate
from libs.log import init_logger

logger = init_logger("spider")

class FixerIo():
    """
    http://fixer.io/
    完全免费，提供每天的数据
    """

    base_url = 'https://api.fixer.io/{}?base={}'

    def __init__(self, source):
        self.source = source

    def get_one_day(self, day):
        url = self.base_url.format(day.strftime('%Y-%m-%d'), self.source)      # todo: urlencode
        # url = self.base_url_2.format(day.strftime('%Y-%m-%d'))     
        logger.info('[crawl %s exchange sipder] <fixer.io> url: %s', day, url)
        resp = requests.get(url)
        data = resp.json()
        base = data['base']
        rates = data['rates']
        for tartget, rate in rates.items():
            ExchangeRate.upsert_(day, base, tartget, rate)

    def get_all_day(self, continue_=True):
        if continue_:
            cur_day = ExchangeRate.select(fn.Min(ExchangeRate.timestamp)).scalar(convert=True)
            cur_day = cur_day.date()
        else:
            cur_day = datetime.now().date()
        while True:
            logger.debug('[crawl history exchange sipder] <fixer.io> %s', cur_day)
            self.get_one_day(cur_day)
            cur_day = cur_day - timedelta(days=1)
            if cur_day.year < 2000:
                break
            time.sleep(2)
