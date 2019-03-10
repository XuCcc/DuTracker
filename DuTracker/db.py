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
    url = Required(str)
    title = Optional(str)
    soldNum = Optional(int)
    logo = Optional(str)
    brandId = Optional(int)
    categoryId = Optional(int)
    images = Optional(StrArray)
    sellDate = Optional(str)
    articleNumber = Optional(str)
    authPrice = Optional(int)
    goodsId = Optional(int)
    sizeList = Optional(StrArray)
    json = Optional(Json)
    datetime = Optional(str, default=arrow.now().format('YYYY-MM-DD HH:mm:ss'))
    brand = Optional('Brand')
    series = Optional('Series')
    imageAndText = Optional(str)

class Brand(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str)
    logo = Required(str)
    products = Set(Product)


class Series(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str)
    coverUrl = Required(str)
    products = Set(Product)


class RetryUrl(db.Entity):
    id = PrimaryKey(int, auto=True)
    url = Optional(str)
    reason = Optional(str)
    datetime = Optional(str, default=arrow.now().format('YYYY-MM-DD HH:mm:ss'))
    callback = Optional(str)
