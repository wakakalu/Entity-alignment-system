# -*- coding:utf-8 -*-
import os
import json
import logging
import traceback

class constant:
    DEFAULT_LOG_DIR = "/var/log/"
    JSON = "json"
    XML = "xml"
    PROP = "properties"

# file convert function dictionary
def load_json_file(file):
     config_file = json.load(file)
     return config_file

__load_file_method = {
    constant.JSON : load_json_file
}

# get logger
def get_logger():
    DEFAULT_LOG_FILE = constant.DEFAULT_LOG_DIR + "setup.log"
    DEFAULT_LEVEL = logging.INFO

    logging.basicConfig(level=DEFAULT_LEVEL, filename=DEFAULT_LOG_FILE)
    return logging.getLogger()

# core function
# config file entry, used to get a config file
def open_config_file(file_name):
    logger = get_logger()

    if os.path.exists(file_name):
        # open file
        try:
            with open(file_name, 'rt') as file:
                # convert file if file type in specific type
                file_type = file_name.split('.')[-1]
                if file_type in __load_file_method:
                    config_file = __load_file_method.get(file_type)(file)

            return config_file
        except Exception:
            logger.error("Expection occured when opening configuration file.\n%s", traceback.format_exc())
            file.close()

    return None

