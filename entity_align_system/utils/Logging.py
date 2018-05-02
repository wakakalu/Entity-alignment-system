# -*- coding:utf-8 -*-
import logging
import os
import logging.config
from config import config

DEFAULT_CONFIG_FILE = "logging.json"
DEFAULT_ENV_KEY = "LOG_CFG"
DEFAULT_LOG_FILE = "/var/log/eas.log"
DEFAULT_LEVEL = logging.INFO

class Logging(object):
    def get_logger(self, name=None):
        # check whether environment variable has config file name
        env_config_file = os.getenv(DEFAULT_ENV_KEY)
        if env_config_file:
            path = env_config_file
        else:
            path = DEFAULT_CONFIG_FILE

        config_file = config.open_config_file(path)

        if config_file:
            logging.config.dictConfig(config_file)
            config_file.close()
        else:
            logging.basicConfig(level=DEFAULT_LEVEL, filename=DEFAULT_LOG_FILE)

        return logging.getLogger(name)