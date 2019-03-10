# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BrandItem(scrapy.Item):
    id = scrapy.Field()
    name = scrapy.Field()
    logo = scrapy.Field()


class SerieItem(scrapy.Item):
    id = scrapy.Field()
    name = scrapy.Field()
    coverUrl = scrapy.Field()


class ProductItem(scrapy.Item):
    id = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    soldNum = scrapy.Field()
    logo = scrapy.Field()
    brandId = scrapy.Field()
    categoryId = scrapy.Field()
    images = scrapy.Field()
    sellDate = scrapy.Field()
    articleNumber = scrapy.Field()
    authPrice = scrapy.Field()
    goodsId = scrapy.Field()
    sizeList = scrapy.Field()
    imageAndText = scrapy.Field()
    detailJson = scrapy.Field()
