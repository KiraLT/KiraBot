from __future__ import unicode_literals

from time import sleep
import logging
from logging import Formatter
from logging import StreamHandler
from logging.handlers import SysLogHandler
from logging.handlers import RotatingFileHandler


from . import settings
from .plugins import PluginsManager


class App(object):

    def __init__(self):
        self.config = None
        self.logger = None
        self.debug = None
        self.load_config()
        self.load_logger()

    def load_config(self):
        self.config = {}
        for var in dir(settings):
            if not var.startswith("__") and var == var.upper():
                self.config[var] = getattr(settings, var)
        self.debug = self.config['DEBUG']

    def load_logger(self):
        logger = logging.getLogger(self.config['LOGGER_NAME'])
        logger.setLevel(getattr(logging, self.config['LOG_LEVEL']))
        if self.debug:
            stream_handler = StreamHandler()
            stream_handler.setFormatter(Formatter(
                    self.config['CONSOLE_LOG_FORMAT']))
            logger.addHandler(stream_handler)
        else:
            syslog_handler = SysLogHandler(address='/dev/log')
            syslog_handler.setFormatter(Formatter(
                    self.config['SYSLOG_LOG_FORMAT']))
            logger.addHandler(syslog_handler)

            file_handler = RotatingFileHandler(
                    self.config['FILE_LOG_FILE'],
                    maxBytes=self.config['FILE_LOG_MAX_SIZE'],
                    backupCount=self.config['FILE_LOG_COUNT'])
            file_handler.setFormatter(Formatter(
                    self.config['FILE_LOG_FORMAT']))
            logger.addHandler(file_handler)
        self.logger = logger

    def run(self):
        PluginsManager(self).run_all_plugins()
        while True:
            sleep(1)
