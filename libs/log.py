# -*- coding: utf-8 -*-

import os
import logging
from logging import Logger, StreamHandler
from logging import FileHandler

from conf.config import log_conf


def init_logger(logger_name):
    if not os.path.exists(log_conf['log_dir']):
        os.makedirs(log_conf['log_dir'])

    if logger_name not in Logger.manager.loggerDict:
        logger = logging.getLogger(logger_name)
        logger.setLevel(log_conf['level'])

        # file
        fmt = '%(asctime)s - %(filename)s - %(lineno)s - %(levelname)s: - %(message)s'
        formatter = logging.Formatter(fmt)

        # stream
        if log_conf['level'] == logging.DEBUG:
            # set peewee debug mode
            # logger = logging.getLogger('peewee')
            # logger.setLevel(logging.DEBUG)
            # logger.addHandler(logging.StreamHandler())
            # set stream handler
            stream_handler = StreamHandler()
            stream_handler.setFormatter(formatter)
            stream_handler.setLevel(logging.DEBUG)
            logger.addHandler(stream_handler)

        # all file
        log_file = os.path.join(log_conf['log_dir'], logger_name + '.log')
        file_handler = FileHandler(log_file)
        file_handler.setLevel(log_conf['level'])
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        # error file
        log_file = os.path.join(log_conf['log_dir'], logger_name + '.error.log')
        file_handler = FileHandler(log_file)
        file_handler.setFormatter(formatter)
        file_handler.setLevel(logging.ERROR)
        logger.addHandler(file_handler)

    logger = logging.getLogger(logger_name)
    return logger
