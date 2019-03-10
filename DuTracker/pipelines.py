# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


from DuTracker.db import *
from DuTracker.utils.log import log


class DBSession(object):

    def open_spider(self, spider):
        db.bind(provider='sqlite', filename='../product.sqlite', create_db=True)
        db.generate_mapping(create_tables=True)

    def close_spider(self, spider):
        db.disconnect()


class SaveBrandItem(DBSession):
    @db_session
    def process_item(self, item, spider):
        bid = item.get('id')
        name = item.get('name')
        if not Brand.exists(id=item.get('id')):
            Brand(
                id=bid,
                name=name,
                logo=item.get('logo')
            )
            log.success(f'品牌：{name} 编号：{bid}')
        return item


class SaveSeriesItem(DBSession):
    @db_session
    def process_item(self, item, spider):
        if not Series.exists(id=item.get('id')):
            Series(
                id=item.get('id'),
                name=item.get('name'),
                coverUrl=item.get('coverUrl')
            )
        return item


class SaveProductItem(DBSession):
    @db_session
    def process_item(self, item, spider):
        pid = item.get('id')
        if not Product.exists(id=pid):
            title = item.get('title')
            articleNumber = item.get('articleNumber')
            Product(
                id=pid,
                url=item.get('url'),
                title=title,
                soldNum=item.get('soldNum'),
                logo=item.get('logo'),
                brandId=item.get('brandId'),
                categoryId=item.get('categoryId'),
                images=item.get('images'),
                sellDate=item.get('sellDate'),
                articleNumber=articleNumber,
                authPrice=item.get('authPrice'),
                goodsId=item.get('goodsId'),
                sizeList=item.get('sizeList'),
                imageAndText=item.get('imageAndText'),
                json=item.get('detailJson'),
                brand=Brand[item.get('brandId')]
            )
            log.success(f'商品:{title} 编号：{pid} 货号：{articleNumber}')
        return item
