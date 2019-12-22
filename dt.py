#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/03/12 21:10
# @Author  : Xu
# @Site    : https://xuccc.github.io/

import click
import logging
import sys
from scrapy.crawler import CrawlerRunner, CrawlerProcess
from scrapy.utils.project import get_project_settings
from twisted.internet import reactor, defer
from apscheduler.schedulers.twisted import TwistedScheduler

from DuTracker.spiders.brand import BrandSpider
from DuTracker.spiders.serie import SerieSpider
from DuTracker.spiders.product import ProductSpider
from DuTracker.spiders.tracker import TrackerSpider
from DuTracker.utils.log import log


@click.group()
def cli():
    pass


@cli.command()
def show():
    settings = get_project_settings()
    log.info('显示远程品牌&系列信息')
    runner = CrawlerRunner(settings)

    @defer.inlineCallbacks
    def crawl():
        yield runner.crawl(BrandSpider, auto=True)
        yield runner.crawl(SerieSpider, auto=True)
        reactor.stop()

    crawl()
    reactor.run()


@cli.command(help='Init Database')
@click.option('--verbose', '-v', is_flag=True, default=False, )
@click.option('--debug', is_flag=True, default=False, help='show scrapy log')
@click.option('--proxy', help='proxy url')
def crawl(verbose, debug, proxy, ):
    settings = get_project_settings()

    if verbose:
        log.setLevel(logging.DEBUG)
    if proxy:
        settings['DOWNLOADER_MIDDLEWARES'].update({
            'DuTracker.middlewares.RandomProxy': 760
        })
        settings['PROXY_URL'] = proxy
    if debug:
        settings['LOG_ENABLED'] = True

    log.info('初始化数据库 product.sqlite')
    runner = CrawlerRunner(settings)

    @defer.inlineCallbacks
    def crawl():
        yield runner.crawl(BrandSpider)
        yield runner.crawl(SerieSpider)
        yield runner.crawl(ProductSpider, fromDB=True)
        reactor.stop()

    crawl()
    reactor.run()


@cli.command(help='add product information by productId')
@click.argument('pid', type=int, nargs=-1)
@click.option('--verbose', '-v', is_flag=True, default=False, )
@click.option('--debug', is_flag=True, default=False, help='show scrapy log')
def addproduct(pid, debug, verbose):
    settings = get_project_settings()

    if verbose: log.setLevel(logging.DEBUG)
    if debug: settings['LOG_ENABLED'] = True

    process = CrawlerProcess(settings)
    process.crawl(ProductSpider, productIds=pid)
    process.start()


@cli.command(help='Monitor products\' price')
@click.option('--verbose', '-v', is_flag=True, default=False, )
@click.option('--debug', is_flag=True, default=False, help='show scrapy log')
@click.option('--proxy', help='proxy url')
# @click.option('--day', type=int, default=1)
@click.option('--min', type=int, default=1000)
@click.option('--product', '-p', multiple=True, type=int, help='product ids')
@click.option('--brand', '-b', multiple=True, type=int, help='brand ids')
@click.option('--serie', '-s', multiple=True, type=int, help='serie ids')
@click.option('--check/--no-check', default=True)
@click.option('--delay', type=float, help='delay between download')
@click.option('--news', is_flag=True, default=False)
@click.option('--days', type=int, default=14,help='save log by days')
def start(verbose, debug, proxy, min, product, brand, serie, check, delay, news, days):
    def check_db():
        from DuTracker.tsdb import influxdb
        try:
            influxdb.ping()
        except  Exception as e:
            log.error(f'InfluxDB 连接错误')
            sys.exit(1)
        else:
            log.success(f'InfluxDB 连接成功')

    if check: check_db()

    # https://stackoverflow.com/questions/44228851/scrapy-on-a-schedule
    settings = get_project_settings()

    if verbose: log.setLevel(logging.DEBUG)
    if proxy:
        settings['DOWNLOADER_MIDDLEWARES'].update({
            'DuTracker.middlewares.RandomProxy': 760
        })
        settings['PROXY_URL'] = proxy
    if debug: settings['LOG_ENABLED'] = True
    if delay: settings['DOWNLOAD_DELAY'] = delay

    process = CrawlerProcess(settings)
    sched = TwistedScheduler()

    if brand:
        sched.add_job(process.crawl, 'interval', args=[BrandSpider], kwargs={'auto': True, 'Ids': brand}, days=1)
        process.crawl(BrandSpider, auto=True, Ids=brand)
    if serie:
        sched.add_job(process.crawl, 'interval', args=[SerieSpider], kwargs={'auto': True, 'Ids': serie}, days=1)
        process.crawl(SerieSpider, auto=True, Ids=serie)
    if brand or serie:
        sched.add_job(process.crawl, 'interval', args=[ProductSpider], kwargs={'fromDB': True}, days=1)
        process.crawl(ProductSpider, fromDB=True)
    process.crawl(TrackerSpider, soldNum_min=min, Ids=product)

    sched.add_job(process.crawl, 'interval', args=[TrackerSpider], kwargs={'soldNum_min': min, 'Ids': product}, hours=6)
    if news:
        sched.add_job(process.crawl, 'interval', args=[TrackerSpider], kwargs={'newItem': True, 'days': days},
                      hours=1)

    sched.add_job(sched.print_jobs, 'interval', hours=6)

    log.info('开始商品价格追踪')
    sched.start()
    process.start(False)


if __name__ == '__main__':
    cli()
