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
@click.option('--verbose', '-v', is_flag=True, default=False, )
@click.option('--debug', is_flag=True, default=False)
@click.option('--proxy', )
def initdb(verbose, debug, proxy, ):
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


@cli.command()
@click.argument('pid', type=int, nargs=-1)
@click.option('--verbose', '-v', is_flag=True, default=False, )
@click.option('--debug', is_flag=True, default=False)
def addproduct(pid, debug, verbose):
    settings = get_project_settings()

    if verbose: log.setLevel(logging.DEBUG)
    if debug: settings['LOG_ENABLED'] = True

    process = CrawlerProcess(settings)
    process.crawl(ProductSpider, productIds=pid)
    process.start()


@cli.command()
@click.option('--verbose', '-v', is_flag=True, default=False, )
@click.option('--debug', is_flag=True, default=False)
@click.option('--proxy', )
# @click.option('--day', type=int, default=1)
@click.option('--min', type=int, default=1000)
@click.option('--brand', '-b', type=int, multiple=True)
@click.option('--serie', '-s', type=int, multiple=True)
def start(verbose, debug, proxy, min, brand, serie):
    # https://stackoverflow.com/questions/44228851/scrapy-on-a-schedule
    settings = get_project_settings()

    if verbose: log.setLevel(logging.DEBUG)
    if proxy:
        settings['DOWNLOADER_MIDDLEWARES'].update({
            'DuTracker.middlewares.RandomProxy': 760
        })
        settings['PROXY_URL'] = proxy
    if debug: settings['LOG_ENABLED'] = True

    process = CrawlerProcess(settings)
    sched = TwistedScheduler()
    sched.add_job(process.crawl, 'interval', args=[TrackerSpider], kwargs={'soldNum_min': min}, hours=6)
    # sched.add_job(process.crawl, 'interval', args=[TrackerSpider], kwargs={'soldNum_min': min}, seconds=30)
    process.crawl(TrackerSpider, soldNum_min=min)

    sched.add_job(sched.print_jobs, 'interval', hours=6)

    if brand:
        sched.add_job(process.crawl, 'interval', args=[BrandSpider], kwargs={'auto': True, 'Ids': brand}, days=1)
    if serie:
        sched.add_job(process.crawl, 'interval', args=[SerieSpider], kwargs={'auto': True, 'Ids': serie}, days=1)

    log.info('开始商品价格追踪')
    sched.start()
    process.start(False)


if __name__ == '__main__':
    cli()
