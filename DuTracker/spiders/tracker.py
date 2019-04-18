# -*- coding: utf-8 -*-
import scrapy
import json

from DuTracker.items import PriceItem
from DuTracker.db import *
from DuTracker.utils.log import log, handle_parse_exception


class TrackerSpider(scrapy.Spider):
    name = 'tracker'
    allowed_domains = ['m.poizon.com']

    custom_settings = {
        'ITEM_PIPELINES': {
            'DuTracker.pipelines.SavePriceItem': 300,
        }
    }

    soldNum_min = 50
    Ids = []

    @db_session
    def start_requests(self):
        log.info(f'选取商品销量高于 {self.soldNum_min} 开始追踪')
        pools = []
        for p in Product.select(lambda p: p.soldNum > self.soldNum_min).order_by(desc(Product.soldNum)):
            pools.append(p)
        for pid in self.Ids:
            if Product.exists(id=pid):
                pools.append(Product[pid])
            else:
                log.fail(f'商品编号:{pid} 不存在数据库')

        for p in pools:
            yield scrapy.Request(p.url, meta={
                'productId': p.id,
                'title': p.title,
                'brand': p.brand,
                'serie': p.serie,
                'articleNumber': p.articleNumber
            })

    @db_session
    @handle_parse_exception
    def parse(self, response):
        title = response.meta.get('title')
        pid = response.meta.get('productId')
        brand = response.meta.get('brand')
        serie = response.meta.get('serie')

        data = json.loads(response.body_as_unicode())['data']
        soldNum = data['detail']['soldNum']
        Product[pid].soldNum = soldNum
        commit()

        sizeList = data['sizeList']
        sizeItem = data['item']
        price = sizeItem['price'] / 100
        formatSize = sizeItem['formatSize']
        log.success(f'商品:{title} 编号：{pid} 价格: {price}/{formatSize} 交易数量: {soldNum}')

        for s in sizeList:
            item = s['item']
            if not item:
                continue
            yield PriceItem(
                id=pid,
                brand=brand,
                serie=serie,
                title=title,
                size=item['size'],
                formatSize=item['formatSize'],
                price=item['price'] / 100,
                soldNum=soldNum,
            )
