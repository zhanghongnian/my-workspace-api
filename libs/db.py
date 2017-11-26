# -*- encoding: utf-8 -*-

import os

from playhouse.shortcuts import RetryOperationalError
from peewee import PostgresqlDatabase
from conf.config import postgresql_conf


class PostRetryDB(RetryOperationalError, PostgresqlDatabase):
    pass


def singleton(cls, *args, **kw):
    instances = {}

    def _singleton(*args, **kw):
        key = str(cls) + str(os.getpid())
        if key not in instances:
            instances[key] = cls(*args, **kw)
        return instances[key]

    return _singleton


@singleton
class DB(object):
    def __init__(self):
        self.postgresql = PostRetryDB(host=postgresql_conf['host'],
                                      port=postgresql_conf['port'],
                                      database=postgresql_conf['database'],
                                      user=postgresql_conf['user'],
                                      password=postgresql_conf['password'])
