# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
import json
import math

from DuTracker.items import ProductItem
from DuTracker.sign.sign import sign
from DuTracker.utils.log import log, handle_parse_exception
from DuTracker.db import *


def get_product_info_url(productid):
    e = '048a9c4943398714b356a696503d2d36'
    string = f'productId{productid}sourceshareDetail{e}'
    result = sign.getSign(string)
    return f'http://m.poizon.com/mapi/product/detail?productId={productid}&' \
           f'source=shareDetail&' \
           f'sign={result}'


class ProductSpider(scrapy.Spider):
    name = 'product'
    allowed_domains = ['m.poizon.com']
    custom_settings = {
        'ITEM_PIPELINES': {
            'DuTracker.pipelines.SaveProductItem': 300,
        }

    }

    productIds = []
    fromDB = False

    @db_session
    def start_requests(self):
        if self.fromDB: [self.productIds.append(p.id) for p in Product.select()]
        for pid in self.productIds:
            yield Request(get_product_info_url(pid))

    @handle_parse_exception
    def parse(self, response):
        data = json.loads(response.body_as_unicode())['data']
        imageAndText = data['imageAndText']
        detail = data['detail']
        productId = detail['productId']
        categoryId = detail['categoryId']
        logoUrl = detail['logoUrl']
        images = [image['url'] for image in detail['images']]
        title = detail['title']
        soldNum = detail['soldNum']
        sellDate = detail['sellDate']
        articleNumber = detail['articleNumber']
        authPrice = detail['authPrice']
        goodsId = detail['goodsId']
        sizeList = detail['sizeList']

        yield ProductItem(
            id=productId,
            url=response.url,
            title=title,
            soldNum=soldNum,
            logo=logoUrl,
            categoryId=categoryId,
            images=images,
            sellDate=sellDate,
            articleNumber=articleNumber,
            authPrice=authPrice,
            goodsId=goodsId,
            sizeList=sizeList,
            imageAndText=imageAndText,
            detailJson=detail
        )
