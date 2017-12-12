# -*- coding: utf-8 -*-

import time

import requests

from conf.config import zhixin_conf
from models.weather import Weather
from models.china_location_code import ChinaLocationCodeAboveCounty
from libs.log import init_logger

logger = init_logger("spider")

location_list = ChinaLocationCodeAboveCounty.raw(
    "select * from china_location_code_above_county where code %% 100 = 0")

# print(location_list)

def fetch(item):
    resp = requests.get(API, params={
        'key': zhixin_conf['key'],
        'location': LOCATION,
        'language': LANGUAGE,
        'unit': UNIT,
        'days': 1
    })

    data = resp.json()

    results = data.get('results',[])
    print('-------------')
    if results:
        result = results[0]['daily'][0]
        print(result)
        Weather.upsert_(
            location_code=item.code,
            location=item.name,
            timestamp=result['date'],
            high=result['high'],
            low=result['low'],
            precip=result['precip'],
            text_day=result['text_day'],
            text_night=result['text_night'],
            wind_direction=result['wind_direction'],
            wind_direction_degree=result['wind_direction_degree'],
            wind_scale=result['wind_scale'],
            wind_speed=result['wind_speed']
        )

    time.sleep(10)


for item in location_list:
    print(item.code, item.name)
    LOCATION = item.name  # 所查询的位置，可以使用城市拼音、v3 ID、经纬度等
    API = 'https://api.seniverse.com/v3/weather/daily.json'  # API URL，可替换为其他 URL
    UNIT = 'c'  # 单位
    LANGUAGE = 'zh-Hans'  # 查询结果的返回语言

    for i in range(10):
        try:
            fetch(item)
            break
        except Exception as e:
            logger.exception(e)
