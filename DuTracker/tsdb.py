#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/03/14 00:02
# @Author  : Xu
# @Site    : https://xuccc.github.io/

from scrapy.utils.project import get_project_settings
from influxdb import InfluxDBClient

_settings = get_project_settings()

_host = _settings.get('INFLUXDB_HOST', 'localhost')
_port = _settings.get('INFLUXDB_PORT', 8086)
_username = _settings.get('INFLUXDB_USER', 'root')
_password = _settings.get('INFLUXDB_PASSWORD', 'root')
_database = _settings.get('FLUXDB_DATABASE')

influxdb = InfluxDBClient(_host, _port, _username, _password, _database)


def gen_points(brandId, productId, title, size, formatSize, price):
    return [{
        'measurement': f"branId_{brandId}",
        'tags': {
            'productId': productId,
            'title': title,
            'size': size,
            'formatSize': formatSize,
        },
        'fields': {
            'price': price
        }
    }]
