# -*- coding: utf-8 -*-

import time
from urllib.parse import urljoin

import requests
from lxml import etree

from models.china_location_code import ChinaLocationCodeAboveCounty, ChinaLocationCode


class AboveCounty():
    """爬取县及县以上的行政区划代码"""

    def __init__(self):
        self.url = "http://www.stats.gov.cn/tjsj/tjbz/xzqhdm/201703/t20170310_1471429.html"
        self.session = requests.session()
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36"
        }
        self.session.headers.update(headers)
        ChinaLocationCodeAboveCounty.truncate_table()

    def crawl(self):
        resp = self.session.get(self.url)
        e = etree.HTML(resp.content)
        for item in e.xpath('//p[@class="MsoNormal"]'):
            span_list = item.xpath('.//span')
            code = span_list[-3].xpath('string(.)').strip()
            name = span_list[-1].xpath('string(.)').strip()
            if name == '市辖区':
                continue
            ChinaLocationCodeAboveCounty.create(
                code=code,
                name=name
            )


class All():
    """爬取所有行政区划代码"""

    level_list = ['city', 'county', 'town', 'village']

    def __init__(self):
        self.start = "http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2016/index.html"
        self.session = requests.session()
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36"
        }
        self.session.headers.update(headers)
        ChinaLocationCode.truncate_table()

    def fetch(self, url):
        resp = self.session.get(url)
        time.sleep(2)
        return resp

    def crawl(self, url, index, text=''):
        level = self.level_list[index]
        table_class = '{}table'.format(level)
        tr_class = '{}tr'.format(level)
        resp = self.fetch(url)
        e = etree.HTML(resp.content)
        for item in e.xpath('//table[@class="{}"]//tr[@class="{}"]'.format(table_class, tr_class)):
            code = item.xpath('.//td')[0].xpath('string(.)')
            name = item.xpath('.//td')[-1].xpath('string(.)')
            if name == '市辖区':
                name = text
            href = item.xpath('.//a/@href')
            print(code, name, href)
            ChinaLocationCode.create(code=code, name=name)
            if href:
                href = href[0]
                new_url = urljoin(url, href)
                self.crawl(new_url, index + 1)

    def crawl_all(self):
        resp = self.fetch(self.start)
        e = etree.HTML(resp.content)
        for item in e.xpath('//tr[@class="provincetr"]//a'):
            text = item.xpath('string(.)')
            href = item.xpath('./@href')[0]
            url = urljoin(self.start, href)
            print(text, url)
            self.crawl(url, 0, text)


if __name__ == '__main__':
    # above_xian = AboveCounty()
    # above_xian.crawl()
    all = All()
    all.crawl_all()
