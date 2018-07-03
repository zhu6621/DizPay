# -*- coding: utf-8 -*-
import logging
import logging.handlers


def multiprocessing_file_logger_handler():
    return logging.handlers.SocketHandler('localhost',
                                          logging.handlers.DEFAULT_TCP_LOGGING_PORT + 101)
