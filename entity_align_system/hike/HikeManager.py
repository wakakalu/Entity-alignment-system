# -*- coding:utf-8 -*-
'''
This module controls other hike modules.This module makes data flow through other modules.
'''

# use as statement to make refactor easier
from entity_align_system.models import InputData
import MachinePartion as MachinePartion
import EntityPartition as HikePartion
import PartialOrderConstruct as PartialOrderConstruct
import QuestionSelection as QuestionSelection

def entity_align():
    data_dict = InputData.input_data()
    entity_blocks = MachinePartion.partition(data_dict)
    entity_blocks = HikePartion.partition(entity_blocks, data_dict)
    partial_order = PartialOrderConstruct.construct_partial_order()
    questions = QuestionSelection