# -*- coding:utf-8 -*-
import logging
import os
import logging.config
import json
from config import config

DEFAULT_CONFIG_FILE = "logging.json"
DEFAULT_ENV_KEY = "LOG_CFG"

class Logging(object):
    def get_logger(self):
        # check whether environment variable has config file name
        env_config_file = os.getenv(DEFAULT_ENV_KEY)
        if env_config_file:
            path = env_config_file
        else:
            path = DEFAULT_CONFIG_FILE

        config_file = config.load_config_file(path)

        return logging.getLogger()