# -*- coding:utf-8 -*-
from entity_align_system.utils import Logging
import unittest
import config

class TestConfig(unittest.TestCase):
    def test_read(self):
        dbtype = config.get_config_item(item="dbtype")
        self.assertTrue(isinstance(dbtype, basestring))


class TestLogging(unittest.TestCase):
    def test_log(self):
        logger = Logging.get_logger()
        logger.info("This is a info log message")
        logger.error("This is a error log message")
