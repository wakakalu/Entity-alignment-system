# -*- coding:utf-8 -*-
'''
This module controls other hike modules.This module makes data flow through other modules.
'''

# use as statement to make refactor easier
from entity_align_system.models.Input import Input
from EntityPartition import EntityPartition
from PartialOrderConstruct import PartialOrderConstruct
import QuestionSelection as QuestionSelection
from entity_align_system import HikeMetaClass

class HikeManager(object):
    __metaclass__ = HikeMetaClass
    def __init__(self, dboperator):
        self.dboperator = dboperator

    def entity_align(self):
        Input().input_data()
        entity_blocks, pp_blocks = EntityPartition().partition()
        partial_orders = PartialOrderConstruct().construct_partial_order(entity_blocks, pp_blocks)
        questions = QuestionSelection(partial_orders) # questions variable is a dict that includes questions and anwsers

        matched_entity_pairs = self.generate_matched_pairs(partial_orders, questions)

        self.dboperator.insert_entity_pairs(matched_entity_pairs)

    def generate_matched_pairs(self, partial_orders, questions):
            pass