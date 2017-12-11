# -*- coding: utf-8 -*-

from peewee import Model, CompositeKey, PrimaryKeyField, CharField, TimestampField, FloatField, BigIntegerField, DateTimeField

from libs.db import DB

db = DB().postgresql


class ChinaLocationCodeAboveCounty(Model):

    id = PrimaryKeyField()
    code = BigIntegerField(unique=True)
    name = CharField(max_length=255)

    class Meta:
        database = db
        db_table = 'china_location_code_above_county'



class ChinaLocationCode(Model):

    id = PrimaryKeyField()
    code = BigIntegerField(unique=True)
    name = CharField(max_length=255)

    class Meta:
        database = db
        db_table = 'china_location_code'


if __name__ == '__main__':
    # ChinaLocationCodeAboveCounty.drop_table()
    # ChinaLocationCodeAboveCounty.create_table()
    ChinaLocationCode.drop_table()
    ChinaLocationCode.create_table()
