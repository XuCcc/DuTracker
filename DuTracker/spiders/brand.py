# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
import json

from DuTracker.items import BrandItem


class BrandSpider(scrapy.Spider):
    name = 'brand'
    allowed_domains = ['m.poizon.com']
    start_urls = [
        'http://m.poizon.com/mapi//search/categoryDetail?catId=0&sign=4ff93b98af1253fe192ff1328ed09081'
    ]
    custom_settings = {
        'ITEM_PIPELINES': {
            'DuTracker.pipelines.SaveBrandItem': 300,
        }

    }

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url, dont_filter=True, headers={
                'AppId': 'wxapp',
                'appVersion': '3.5.0',
                'Referer': 'https://servicewechat.com/wx3c12cdd0ae8b1a7b/62/page-frame.html',
            })

    def parse(self, response):
        data = json.loads(response.body_as_unicode())
        for brand in data['data']['list']:
            id = brand['brand']['goodsBrandId']
            name = brand['brand']['brandName']
            logo = brand['brand']['logoUrl']
            yield BrandItem(id=id, name=name, logo=logo)
