#!/usr/bin/env python
"""
A log that wraps at a specified size.
"""

import logging
from logging.handlers import RotatingFileHandler


def initialize(filename, size=5, default=logging.INFO, backup=1):
    """ Initializes logging to file and console
    :param filename the name of the file
    :param size the max size of the file in megabytes, before wrapping occurs
    :param default logging level
    :param backup how many backup files are maintained
    :return log object
    """

    log_formatter = logging.Formatter(fmt='%(asctime)s.%(msecs)03d,(%(threadName)-10s),' \
                                          '[%(levelname)s],%(funcName)s(%(lineno)d),%(message)s',
                                      datefmt='%Y-%m-%d %H:%M:%S')
    log_handler = RotatingFileHandler(filename, mode='a', maxBytes=size * 1024 * 1024,
                                      backupCount=backup, encoding=None, delay=0)
    log_handler.setFormatter(log_formatter)
    log_handler.setLevel(default)
    log_object = logging.getLogger(filename)
    log_object.setLevel(log_handler.level)
    log_object.addHandler(log_handler)
    console = logging.StreamHandler()
    console.setFormatter(log_formatter)
    console.setLevel(logging.DEBUG)
    log_object.addHandler(console)
    return log_object
