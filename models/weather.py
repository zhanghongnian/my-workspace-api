# -*- coding: utf-8 -*-

from peewee import Model, PrimaryKeyField, CharField, TimestampField, IntegerField, DateTimeField

from libs.db import DB

db = DB().postgresql


class Weather(Model):

    id = PrimaryKeyField()
    location_code = IntegerField()
    location = CharField(max_length=50)
    timestamp = DateTimeField()
    high = IntegerField()
    low = IntegerField()
    precip = CharField(max_length=10)
    text_day = CharField(max_length=10)
    text_night = CharField(max_length=10)
    wind_direction = CharField(max_length=10)
    wind_direction_degree = CharField(max_length=10)
    wind_scale = CharField(max_length=10)
    wind_speed = CharField(max_length=10)

    @staticmethod
    def upsert_(location_code, location, timestamp, high, low, precip, text_day,
                text_night, wind_direction, wind_direction_degree, wind_scale, wind_speed):
        sql = """
        insert into weather (location_code, location, timestamp, high, low, precip, text_day, 
                text_night, wind_direction, wind_direction_degree, wind_scale, wind_speed) 
            values({location_code}, '{location}', '{timestamp}', {high}, {low}, '{precip}', '{text_day}',
                '{text_night}', '{wind_direction}', '{wind_direction_degree}', '{wind_scale}', '{wind_speed}')
        on conflict (location_code, timestamp)      
        do update set
            high = {high},
            low = {low},
            precip = '{precip}',
            text_day = '{text_day}',
            text_night = '{text_night}',
            wind_direction = '{wind_direction}',
            wind_direction_degree = '{wind_direction_degree}',
            wind_scale = '{wind_scale}',
            wind_speed = '{wind_speed}'
        """.format(
            location_code=location_code,
            location=location,
            timestamp=timestamp,
            high=high,
            low=low,
            precip=precip,
            text_day=text_day,
            text_night=text_night,
            wind_direction=wind_direction,
            wind_direction_degree=wind_direction_degree,
            wind_scale=wind_scale,
            wind_speed=wind_speed
        )
        # print(sql)
        db.execute_sql(sql)

    class Meta:
        database = db
        db_table = 'weather'
        indexes = (
            (('location_code', 'timestamp'), True),
        )


if __name__ == '__main__':
    Weather.drop_table()
    Weather.create_table()
