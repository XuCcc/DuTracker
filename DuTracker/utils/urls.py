#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/03/24 22:02
# @Author  : Xu
# @Site    : https://xuccc.github.io/
import execjs
import requests


def get_headers():
	headers = {
		'Host': "app.poizon.com",
		'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)"
									" Chrome/53.0.2785.143 Safari/537.36 MicroMessenger/7.0.4.501 NetType/WIFI "
									"MiniProgramEnv/Windows WindowsWechat",
		'appid': "wxapp",
		'appversion': "4.4.0",
		'content-type': "application/x-www-form-urlencoded",
		'Accept-Encoding': "gzip, deflate",
		'Accept': "*/*",
	}
	return headers


def get_brand_page_url(unionId, page=0):
	sortType = 0
	sortMode = 1
	with open('DuTracker/sign/sign.js', 'r', encoding='utf-8')as f:
		all_ = f.read()
		ctx = execjs.compile(all_)
		# 53489
		sign = ctx.call('getSign',
										'catId{}limit20page{}sortMode{}sortType{}titleunionId{}19bc545a393a25177083d4a748807cc0'
										.format(0, page, sortMode, sortType, unionId))

		return 'https://app.poizon.com/api/v1/h5/search/fire/search/list?title=&page={}&sortType={}&sortMode={}&limit=20&catId=0&unionId={}&sign={}' \
			.format(page, sortType, sortMode, unionId, sign)


def get_serie_page_url(unionId, page=0):
	sortType = 0
	sortMode = 1
	with open('DuTracker/sign/sign.js', 'r', encoding='utf-8')as f:
		all_ = f.read()
		ctx = execjs.compile(all_)

		sign = ctx.call('getSign',
										'catId{}limit20page{}sortMode{}sortType{}titleunionId{}19bc545a393a25177083d4a748807cc0'
										.format(1, page, sortMode, sortType, unionId))
		#https://app.poizon.com/api/v1/h5/search/fire/search/list?title=&page=0&sortType=0&sortMode=1&limit=20&catId=1&unionId=1&sign=63531b2336752bc5e22fa71854f4f448
		return 'https://app.poizon.com/api/v1/h5/search/fire/search/list?title=&page={}&sortType={}&sortMode={}&limit=20&catId=1&unionId={}&sign={}' \
			.format(page, sortType, sortMode, unionId, sign)
