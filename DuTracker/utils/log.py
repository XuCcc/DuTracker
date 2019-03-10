#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/03/10 13:33
# @Author  : Xu
# @Site    : https://xuccc.github.io/


from click import style
import logging
from DuTracker import settings


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

default_level = getattr(settings, 'LOG_LEVEL', 'DEBUG')
level = getattr(logging, default_level)

_logger = logging.getLogger('spider')
_logger.setLevel(level)
_logger.addHandler(file_handler)

log = Logger(_logger)
