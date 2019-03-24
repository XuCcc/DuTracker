#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/03/10 13:33
# @Author  : Xu
# @Site    : https://xuccc.github.io/

import sys
from click import style
import logging
import traceback

class ColorfulText(object):
    """Colorful text"""

    @staticmethod
    def blue(msg):
        return style(msg, fg='blue')

    @staticmethod
    def green(msg):
        return style(msg, fg='green')

    @staticmethod
    def red(msg):
        return style(msg, fg='red')

    @staticmethod
    def yellow(msg):
        return style(msg, fg='yellow')

    @staticmethod
    def cyan(msg):
        return style(msg, fg='cyan')


class Logger(object):
    def __init__(self, logger: logging.Logger):
        self._logger = logger

    def info(self, msg):
        self._logger.info(ColorfulText.blue('[*] ') + msg)

    def success(self, msg):
        self._logger.info(ColorfulText.green('[✔] ') + msg)

    def fail(self, msg):
        self._logger.info(ColorfulText.red('[✘] ') + msg)

    def warn(self, msg):
        self._logger.warning(ColorfulText.yellow('[!] ') + msg)

    def error(self, msg):
        self._logger.error(ColorfulText.red('[?] ') + msg)

    def debug(self, msg):
        self._logger.debug(ColorfulText.cyan('[#] ') + msg)

    def setLevel(self, level):
        self._logger.setLevel(level)

    @property
    def level(self):
        return self._logger.level


formatter = logging.Formatter('%(asctime)s: %(message)s')
file_handler = logging.FileHandler('spider.log')
file_handler.setFormatter(formatter)
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(formatter)

_logger = logging.getLogger('spider')
_logger.setLevel(logging.INFO)
_logger.addHandler(file_handler)
_logger.addHandler(console_handler)

log = Logger(_logger)


def handle_parse_exception(func):
    def wrapper(spider, response):
        try:
            for result in func(spider, response):
                yield result
        except Exception as e:
            log.fail(
                f'[Spider:{spider.name}->Function:{func.__name__}] {response.url} {e.__class__.__name__}:{e}')
            log.debug(f'{traceback.format_exc()}')
            yield next(spider.start_requests())

    return wrapper
