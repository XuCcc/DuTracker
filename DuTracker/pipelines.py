# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


from DuTracker.db import *
from DuTracker.utils.log import log
from DuTracker.tsdb import influxdb, gen_points

import traceback


class SaveProductId():
    @db_session
    def process_item(self, item, spider):
        pid = item.get('id')
        title = item.get('title')
        name = item.get('name')
        if Product.exists(id=pid):
            p = Product[pid]
        else:
            p = Product(id=pid)
        p.title = title
        if spider.name == 'brand':
            p.brand = name
        elif spider.name == 'serie':
            p.serie = name
        log.success(f'商品：{title} 编号：{pid}')
        return item


class SaveProductItem():
    @db_session
    def process_item(self, item, spider):
        pid = item.get('id')
        title = item.get('title')
        articleNumber = item.get('articleNumber')
        url = item.get('url')
        soldNum = item.get('soldNum')
        logo = item.get('logo')
        categoryId = item.get('categoryId')
        images = item.get('images')
        sellDate = item.get('sellDate')
        authPrice = item.get('authPrice')
        goodsId = item.get('goodsId')
        sizeList = item.get('sizeList')
        imageAndText = item.get('imageAndText')
        detailJson = item.get('detailJson')
        if not Product.exists(id=pid):
            p = Product(id=pid)
        else:
            p = Product[pid]
        p.url = url
        p.title = title
        p.soldNum = soldNum
        p.logo = logo
        p.categoryId = categoryId
        p.images = images
        p.sellDate = sellDate
        p.articleNumber = articleNumber
        p.authPrice = authPrice
        p.goodsId = goodsId
        p.sizeList = sizeList
        p.imageAndText = imageAndText
        p.json = detailJson
        log.success(f'商品:{title} 编号：{pid} 发售日期：{sellDate} 售出量: {soldNum} ')
        return item


class SavePriceItem(object):
    def process_item(self, item, spider):
        pid = item.get('id')
        brand = item.get('brand')
        serie = item.get('serie')
        title = item.get('title')
        size = item.get('size')
        formatSize = item.get('formatSize')
        price = item.get('price')
        soldNum = item.get('soldNum')
        points = gen_points(brand, serie, pid, title, size, formatSize, price, soldNum)
        try:
            result = influxdb.write_points(points)
        except Exception as e:
            log.fail(f'写入数据库失败({e.__class__.__name__}) 商品:{title} 编号：{pid} 尺码: {size} 价格: {price}')
            log.debug(traceback.format_exc())
        else:
            if not result:
                log.fail(f'写入数据库失败 商品:{title} 编号：{pid} 尺码: {size} 价格: {price}')
        return item
