# -*- coding:utf-8 -*-
import os
import json

JSON = "json"
XML = "xml"
PROP = "properties"

def load_json_file(file):
     config_file = json.load(file)
     return config_file

__load_file_method = {
    JSON : load_json_file
}

def load_config_file(file_name):
    if os.path.exists(file_name):
        # open file
        with open(file_name, 'rt') as file:
            # convert file if file type in specific type
            file_type = file_name.split('.')[-1]
            if file_type in __load_file_method:
                config_file = __load_file_method.get(file_type)(file)

        return config_file

    return None

