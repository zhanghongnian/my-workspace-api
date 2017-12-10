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

    def get_yesterday(self):
        yesterday = datetime.now().date() - timedelta(days=1)
        self.get_one_day(yesterday)

    def get_one_day(self, day):
        url = self.base_url.format(day.strftime(
            '%Y-%m-%d'), self.source)      # todo: urlencode
        logger.info('[crawl %s exchange sipder] <fixer.io> url: %s', day, url)
        resp = requests.get(url)
        data = resp.json()
        base = data['base']
        rates = data['rates']
        for tartget, rate in rates.items():
            ExchangeRate.upsert_(day, base, tartget, rate)

    def get_all_day(self, check=False):
        cur_day = datetime.now().date()
        while True:
            logger.debug(
                '[crawl all history exchange sipder] <fixer.io> %s', cur_day)
            try:
                if ExchangeRate.select().where(ExchangeRate.timestamp == cur_day).count() == 0:
                    self.get_one_day(cur_day)
                elif check is False:
                    logger.info('[crawled, crawl done]')
                    break
                else:
                    logger.debug('[check history]')
                cur_day = cur_day - timedelta(days=1)
                if cur_day.year < 2000:
                    logger.info('[too early, crawl done]')
                    break
                time.sleep(2)
            except Exception as e:
                # this msg often raise timeout exception
                logger.exception(e)
                time.sleep(2)


if __name__ == '__main__':
    # todo 改为 click
    fixer_io = FixerIo('CNY')
    fixer_io.get_all_day()
