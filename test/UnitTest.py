# -*- coding:utf-8 -*-
import unittest
import config

class TestConfig(unittest.TestCase):
    def test_read(self):
        dbtype = config.get_config_item(item="dbtype")
        self.assertTrue(isinstance(dbtype, basestring))
