#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/03/10 13:43
# @Author  : Xu
# @Site    : https://xuccc.github.io/

from pony.orm import *
import arrow

db = Database()


class Product(db.Entity):
    id = PrimaryKey(int, auto=True)
    url = Optional(str)
    title = Optional(str)
    soldNum = Optional(int)
    logo = Optional(str)
    categoryId = Optional(int)
    images = Optional(StrArray)
    sellDate = Optional(str)
    articleNumber = Optional(str)
    authPrice = Optional(int)
    goodsId = Optional(int)
    sizeList = Optional(StrArray)
    json = Optional(Json)
    datetime = Optional(str, default=arrow.now().format('YYYY-MM-DD HH:mm:ss'))
    brand = Optional(str)
    serie = Optional(str)
    imageAndText = Optional(str)


db.bind(provider='sqlite', filename='../product.sqlite', create_db=True)
db.generate_mapping(create_tables=True)
