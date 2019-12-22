# -*- coding: utf-8 -*-
import scrapy
import json
import arrow
from DuTracker.utils.urls import get_headers as headers


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
	newItem = False  # 适用于商品发售初期
	days = 14

	@db_session
	def get_items(self):
		pools = []
		if not self.newItem:
			for p in Product.select(lambda p: p.soldNum > self.soldNum_min).order_by(desc(Product.soldNum)):
				pools.append(p)
			for pid in self.Ids:
				if Product.exists(id=pid):
					pools.append(Product[pid])
				else:
					log.fail(f'商品编号:{pid} 不存在数据库')
		else:
			for p in Product.select():
				delay = arrow.now() - arrow.get(p.datetime, 'YYYY-MM-DD HH:mm:ss')
				if delay.days < self.days: pools.append(p)

		return pools

	def start_requests(self):
		log.info(f'选取商品销量高于 {self.soldNum_min} 开始追踪')
		pools = self.get_items()

		for p in pools:
			# log.info(f'production url: {p.url}')
			yield scrapy.Request(p.url, meta={
				'productId': p.id,
				'title': p.title,
				'brand': p.brand,
				'serie': p.serie,
				'articleNumber': p.articleNumber
			}, headers=headers())

	@db_session
	@handle_parse_exception
	def parse(self, response):
		title = response.meta.get('title')
		pid = response.meta.get('productId')
		brand = response.meta.get('brand')
		serie = response.meta.get('serie')

		data = json.loads(response.body_as_unicode())['data']
		# log.info(f'data {data}')
		soldNum = data['detail']['soldNum']
		Product[pid].soldNum = soldNum
		commit()

		sizeList = data['sizeList']
		sizeItem = data['item']
		price = sizeItem['price'] / 100
		# formatSize = sizeItem['formatSize']
		# log.success(f'商品:{title} 编号：{pid} 价格: {price}/{formatSize} 交易数量: {soldNum}')
		log.success(f'商品:{title} 编号：{pid} 价格: {price} 交易数量: {soldNum}')

		for s in sizeList:
			item = s['item']
			if not item:
				continue
			yield PriceItem(
				id=pid,
				brand=brand,
				serie=serie,
				title=title,
				size=s['size'],
				formatSize=s['formatSize'],
				price=item['price'] / 100,
				soldNum=soldNum,
			)

# if __name__ == '__main__':
#     with db_session:
#         for p in Product.select():
#             delay = arrow.now() - arrow.get(p.datetime, 'YYYY-MM-DD HH:mm:ss')
#             if delay.days < 60:
#                 print(p.title, p.datetime)
