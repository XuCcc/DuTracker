#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/03/24 22:02
# @Author  : Xu
# @Site    : https://xuccc.github.io/

def get_brand_page_url(unionid, page=0):
    return f'http://m.poizon.com/search/list?_timestamp=xxxxxxxxxxx&' \
           f'catId=0&lastId=page&limit=20&' \
           f'loginToken=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx&' \
           f'mode=0&newSign=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx&' \
           f'page={page}&' \
           f'platform=iPhone&' \
           f'sign=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx&' \
           f'sortMode=1&' \
           f'sortType=0&' \
           f'token=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx&' \
           f'unionId={unionid}&' \
           f'uuid=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx&' \
           f'v=3.5.5'


def get_serie_page_url(unionId, page=0):
    return f'http://m.poizon.com/search/list?_timestamp=xxxxxxxxxxx&' \
           f'catId=1&' \
           f'lastId=page&limit=20&' \
           f'loginToken=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx&' \
           f'mode=0&newSign=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx&' \
           f'page={page}&' \
           f'platform=iPhone&' \
           f'sign=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx&' \
           f'sortMode=1&sortType=0&' \
           f'token=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx&' \
           f'unionId={unionId}&' \
           f'uuid=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx&' \
           f'v=3.5.5'
