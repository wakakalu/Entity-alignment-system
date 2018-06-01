# -*- coding:utf-8 -*-
'''
Constuct partial order
'''
from __future__ import division
from numpy import array, zeros, argmax
from entity_align_system import HikeMetaClass
import numpy as np


class PartialOrderConstruct(object):
    __metaclass__ = HikeMetaClass

    def construct_partial_order(self, entity_blocks, pp_blocks):
        partial_orders = []

        for i in range(len(entity_blocks)):
            entity_block = entity_blocks[i]
            pp_block = pp_blocks[i]
            order = self.construct_single_order(entity_block, pp_block)
            partial_orders.append(order)

        return partial_orders

    def construct_single_order(self, entity_block, pp_block):
        pp_weight = self.calc_pp_weight(pp_block)

    def calc_pp_weight(self, pp_block):
        pass
