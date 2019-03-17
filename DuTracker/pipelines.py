# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


from DuTracker.db import *
from DuTracker.utils.log import log
from DuTracker.tsdb import influxdb, gen_points


class SaveBrandItem():
    @db_session
    def process_item(self, item, spider):
        bid = item.get('id')
        name = item.get('name')
        logo = item.get('logo')
        if not Brand.exists(id=bid):
            Brand(id=bid, name=name, logo=logo)
            log.success(f'品牌：{name} 编号：{bid}')
        else:
            b = Brand[bid]
            b.name = name
            b.logo = logo
            log.info(f'品牌：{name} 编号：{bid}')
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
        brandId = item.get('brandId')
        categoryId = item.get('categoryId')
        images = item.get('images')
        sellDate = item.get('sellDate')
        articleNumber = articleNumber
        authPrice = item.get('authPrice')
        goodsId = item.get('goodsId')
        sizeList = item.get('sizeList')
        imageAndText = item.get('imageAndText')
        detailJson = item.get('detailJson')
        if not Product.exists(id=pid):
            Product(
                id=pid,
                url=url,
                title=title,
                soldNum=soldNum,
                logo=logo,
                brandId=brandId,
                categoryId=categoryId,
                images=images,
                sellDate=sellDate,
                articleNumber=articleNumber,
                authPrice=authPrice,
                goodsId=goodsId,
                sizeList=sizeList,
                imageAndText=imageAndText,
                json=detailJson,
                brand=Brand[item.get('brandId')]
            )
            log.success(f'商品:{title} 编号：{pid} 货号：{articleNumber} 售出量: {soldNum}')
        else:
            p = Product[pid]
            p.url = url
            p.title = title
            p.soldNum = soldNum
            p.logo = logo
            p.brandId = brandId
            p.categoryId = categoryId
            p.images = images
            p.sellDate = sellDate
            p.articleNumber = articleNumber
            p.authPrice = authPrice
            p.goodsId = goodsId
            p.sizeList = sizeList
            p.imageAndText = imageAndText
            p.json = detailJson
            p.brand = Brand[item.get('brandId')]
            log.info(f'商品:{title} 编号：{pid} 货号：{articleNumber} 售出量: {soldNum}')
        return item


class SavePriceItem(object):
    def process_item(self, item, spider):
        pid = item.get('id')
        brandId = item.get('brandId')
        title = item.get('title')
        size = item.get('size')
        formatSize = item.get('formatSize')
        price = item.get('price')
        points = gen_points(brandId, pid, title, size, formatSize, price)
        result = influxdb.write_points(points)
        if result:
            log.debug(f'商品:{title} 编号：{pid} 尺码: {size} 价格: {price}')
        else:
            log.fail(f'写入数据库失败 | 商品:{title} 编号：{pid} 尺码: {size} 价格: {price}')
        return item
