# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
import json
import math
import execjs

from DuTracker.items import ProductItem
from DuTracker.sign.sign import sign
from DuTracker.utils.log import log, handle_parse_exception
from DuTracker.db import *
from DuTracker.utils.urls import get_headers as headers


# def get_product_info_url(productid):
# 	e = '048a9c4943398714b356a696503d2d36'
# 	string = f'productId{productid}sourceshareDetail{e}'
# 	result = sign.getSign(string)
# 	return f'http://m.poizon.com/mapi/product/detail?productId={productid}&' \
# 				 f'source=shareDetail&' \
# 				 f'sign={result}'

def get_product_info_url(productId):
	# 商品详情
	# log.info('商品详情url')
	with open('DuTracker/sign/sign.js', 'r', encoding='utf-8') as f:
		all_ = f.read()
		ctx = execjs.compile(all_)
		sign = ctx.call('getSign',
										'productId{}productSourceNamewx19bc545a393a25177083d4a748807cc0'.format(productId))

		product_detail_url = 'https://app.poizon.com/api/v1/h5/index/fire/flow/product/detail?' \
												 'productId={}&productSourceName=wx&sign={}'.format(productId, sign)
		# log.info(f'商品详情url: {product_detail_url}')
		return product_detail_url


# URL	https://app.poizon.com/api/v1/h5/index/fire/flow/product/detail?productId=26850&productSourceName=wx&sign=0e145c5543d9751497a2e700bbea1e4c
# URL	https://app.poizon.com/api/v1/h5/index/fire/flow/product/detail?productId=65482&productSourceName=wx&sign=091fb148fe96ddbfda383d2dd46fbe67

class ProductSpider(scrapy.Spider):
	name = 'product'
	# allowed_domains = ['m.poizon.com']
	# allowed_domains = ['app.poizon.com']
	custom_settings = {
		'ITEM_PIPELINES': {
			'DuTracker.pipelines.SaveProductItem': 300,
		}

	}

	productIds = []
	fromDB = False

	@db_session
	def start_requests(self):
		log.info('获取商品详情')
		if self.fromDB: [self.productIds.append(p.id) for p in Product.select()]
		for pid in self.productIds:
			log.info(f'获取商品详情request {pid}')
			url = get_product_info_url(pid)
			log.info(f'商品详情request url：{url}')
			log.info("headers ---> {0}".format(headers()))
			yield Request(url, headers=headers())

	@handle_parse_exception
	def parse(self, response):
		# log.info('商品详情response')
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

		# log.info(f'商品详情 response url：{response.url}')

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
