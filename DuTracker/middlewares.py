# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

import random
import json
from scrapy.exceptions import IgnoreRequest
from scrapy.downloadermiddlewares.retry import RetryMiddleware

from DuTracker.utils.log import log
from DuTracker.db import *


def checkJson(string):
    try:
        json.loads(string)
    except  Exception as e:
        return False
    else:
        return True


class RandomUserAgent(object):
    def __init__(self, user_agent):
        super(RandomUserAgent, self).__init__()
        self.user_agent = user_agent

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings.get('RANDOM_USER_AGENT'))

    def process_request(self, request, spider):
        request.headers['User-Agent'] = random.choice(self.user_agent)


class RandomProxy(object):
    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        return cls(settings.ge('PROXY_URL'))

    def __init__(self, proxy):
        self.proxy = proxy

    def process_request(self, request, spider):
        request.meta['proxy'] = self.proxy


class RetryException(RetryMiddleware):
    def process_response(self, request, response, spider):
        if request.meta.get('dont_retry', False):
            return response
        data = response.body_as_unicode()
        if not checkJson(data):
            log.warn(f'返回Json格式错误无法解析 目标页面 {request.url} 返回数据 {response.body_as_unicode()} 开始重试')
            return self._retry(request, 'Json Format Error', spider) or response
        json_data = json.loads(data)
        msg = json_data['msg']
        status = json_data['status']
        if status == 403:
            log.warn(f'目标页面{request.url} 拒绝访问 提示信息 忽略请求')
            return IgnoreRequest()
        if status != 200:
            log.warn(f'返回Json状态错误 目标页面 {request.url} 提示信息 {msg} 开始重试')
            return self._retry(request, 'Json Status Error', spider) or response
        return response

    def process_exception(self, request, exception, spider):
        if isinstance(exception, self.EXCEPTIONS_TO_RETRY) \
                and not request.meta.get('dont_retry', False):
            return self._retry(request, exception, spider)

    def _retry(self, request, reason, spider):
        retries = request.meta.get('retry_times', 0) + 1

        retry_times = self.max_retry_times

        if 'max_retry_times' in request.meta:
            retry_times = request.meta['max_retry_times']

        stats = spider.crawler.stats

        if retries <= retry_times:
            retryreq = request.copy()
            retryreq.meta['retry_times'] = retries
            retryreq.dont_filter = True
            retryreq.priority = request.priority + self.priority_adjust


            stats.inc_value('retry/count')
            stats.inc_value('retry/reason_count/%s' % reason)
            log.debug(f'第 [{retries}] 次重试请求 目标页面 {request.url} ')
            return retryreq
        else:
            stats.inc_value('retry/max_reached')
            log.error(f'重试请求达最大次数 目标页面 {request.url} 已放弃')
            with db_session:
                RetryUrl(
                    url=request.url,
                    reason=str(reason),
                    callback=request.meta['callback']
                )
