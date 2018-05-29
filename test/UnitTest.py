# -*- coding:utf-8 -*-
from entity_align_system.utils import Logging
from entity_align_system.hike.EntityPartition import EntityPartion
from numpy import zeros, array
import unittest
import config


class UnitTest(unittest.TestCase):
    def test_read_config(self):
        dbtype = config.get_config_item(item="dbtype")
        self.assertTrue(isinstance(dbtype, basestring))

    def test_log(self):
        logger = Logging.get_logger()
        logger.info("This is a info log message")
        logger.error("This is a error log message")

    def test_calc_pp_num_blocks(self):
        sim_mat = array(zeros((10, 10)))
        # [1 3 4 6] for a block
        sim_mat[0][2] = 1
        sim_mat[2][5] = 1
        sim_mat[3][5] = 1
        # [2 7 9] for a block
        sim_mat[1][6] = 1
        sim_mat[8][6] = 1
        # [5 8 10] for a block
        sim_mat[9][7] = 1
        sim_mat[7][4] = 1

        sim_mat += sim_mat.T

        assume_blocks = [set([0, 2, 3, 5]), set([1, 6, 8]), set([4, 7, 9])]
        blocks = EntityPartion().calc_pp_num_blocks(sim_mat, 0.5)

        self.assertTrue(len(assume_blocks) == len(blocks))
        blocks_len = len(assume_blocks)
        block_sets = []
        for block in blocks:
            block_sets.append(set(block))
        for i in range(blocks_len):
            self.assertTrue(set(assume_blocks[i]) in block_sets)
