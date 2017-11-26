# -*- coding: utf-8 -*-

from peewee import Model, CompositeKey, PrimaryKeyField, CharField, TimestampField, FloatField, IntegerField, DateTimeField

from libs.db import DB

db = DB().postgresql


class ExchangeRate(Model):

    id = PrimaryKeyField()
    timestamp = DateTimeField()
    source = CharField(max_length=3)
    target = CharField(max_length=3)
    rate = FloatField()

    @classmethod
    def upsert_(cls, timestamp, source, target, rate):
        cur = cls.select().where(cls.timestamp == timestamp,
                                 cls.source == source,
                                 cls.target == target).first()
        if cur:
            cur.rate = rate
            cur.save()
        else:
            cur = cls()
            cur.timestamp = timestamp
            cur.source = source
            cur.target = target
            cur.rate = rate
            cur.save()

    class Meta:
        database = db
        db_table = 'exchange_rate'
        indexes = (
            (('timestamp', 'source', 'target'), True),
        )


if __name__ == '__main__':
    ExchangeRate.create_table()
