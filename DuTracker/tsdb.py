#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/03/14 00:02
# @Author  : Xu
# @Site    : https://xuccc.github.io/

import sys
from scrapy.utils.project import get_project_settings
from influxdb import InfluxDBClient

from DuTracker.utils.log import log

_settings = get_project_settings()

_host = _settings.get('INFLUXDB_HOST', 'localhost')
_port = _settings.get('INFLUXDB_PORT', 8086)
_username = _settings.get('INFLUXDB_USER', 'root')
_password = _settings.get('INFLUXDB_PASSWORD', 'root')
_database = _settings.get('FLUXDB_DATABASE')

influxdb = InfluxDBClient(_host, _port, _username, _password, _database)
try:
    influxdb.ping()
except  Exception as e:
    log.error(f'InfluxDB 连接错误')
    sys.exit(1)
else:
    log.success(f'InfluxDB 连接成功')


def gen_points(brand, serie, productId, title, size, formatSize, price, soldNum):
    return [{
        'measurement': "pHistory",
        'tags': {
            'productId': productId,
            'title': title,
            'brand': brand,
            'serie': serie,
            'size': size,
            'formatSize': formatSize,
        },
        'fields': {
            'price': price,
            'soldNum': soldNum
        }
    }]
