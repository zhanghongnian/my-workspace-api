# -*- coding: utf-8 -*-
import os
import logging

postgresql_conf = {
    'host': os.getenv('POSTGRESQL_HOST'),
    'port': os.getenv('POSTGRESQL_PORT'),
    'database': os.getenv('POSTGRESQL_DATABASE'),
    'user': os.getenv('POSTGRESQL_USER'),
    'password': os.getenv('POSTGRESQL_PASSWORD')
}

log_conf = {
    "log_dir": "/tmp/logs",
    "level": logging.DEBUG
}