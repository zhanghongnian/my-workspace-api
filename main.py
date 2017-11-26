# -*- coding: utf-8 -*-

import os
import json
import time
import datetime

import requests

import logging

from spider.exchange_rate import FixerIo

fixer_io = FixerIo('CNY')

fixer_io.get_all_day()
