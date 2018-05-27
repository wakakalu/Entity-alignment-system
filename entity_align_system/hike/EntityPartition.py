# -*- coding:utf-8 -*-
'''
Entity partition by hike method
'''
from __future__ import division
from numpy import array, zeros, argmax
from entity_align_system import HikeMetaClass
import numpy as np


class EntityPartion(object):
    __metaclass__ = HikeMetaClass

    def __init__(self, dboperator):
        self.dboperator = dboperator

    def partition(self, merge_threshold):
        # TODO:decoupling kb,replace DBPedia & YAGO with abstract KB type
        # predicate list of predicates from dbpedia and yago
        dbpedia_preds = self.dboperator.get_predicates("DBPedia")
        yago_preds = self.dboperator.get_predicates("YAGO")

        # predicate pairs calculated from predicate similar matrix W
        pred_pair_list = self.get_pred_pairs(dbpedia_preds, yago_preds)

        # Queue merge similarity threshold
        if merge_threshold == None:
            merge_threshold = 0

        partition_queue = self.generate_queue(pred_pair_list)
        gap = 0.1
        cut_level = 1
        while cut_level >= merge_threshold:
            sim_matrix_w = self.refresh_sim_matrix(partition_queue)
            pp_num_blocks = self.calc_pp_num_blocks(sim_matrix_w, cut_level)
            partition_queue = self.merge_predicate_pairs(partition_queue, pp_num_blocks)
            cut_level = cut_level - gap

        entity_pair_blocks = self.generate_entity_blocks(partition_queue)

        self.dboperator.close_connection()

        return entity_pair_blocks

    def get_pred_pairs(self, dbpedia_preds, yago_preds):
        dbpedia_pred_num = len(dbpedia_preds)
        yago_pred_num = len(yago_preds)

        sim_matrix_w = array(zeros((dbpedia_pred_num, yago_pred_num)))
        for i in range(dbpedia_pred_num):
            for j in range(yago_pred_num):
                sim_matrix_w[i][j] = self.pred_sim_cal(dbpedia_preds[i], yago_preds[j])

        max_sim_pred_indices = argmax(sim_matrix_w)
        pred_pair_list = []
        pred_pair_num = min(dbpedia_pred_num, yago_pred_num)
        for i in range(pred_pair_num):
            dbpedia_pred = dbpedia_preds[i]
            yago_pred_index = max_sim_pred_indices[i]
            yago_pred = yago_preds[yago_pred_index]

            pred_pair_list.append((dbpedia_pred, yago_pred))

        return pred_pair_list

    def pred_sim_cal(self, pred1, pred2):
        intersection_num = self.dboperator.get_intersection(pred1, pred2)
        union_num = self.dboperator.get_intersection(pred1, pred2)

        return intersection_num / union_num

    def refresh_sim_matrix(self, pred_pair_list):
        pred_pair_list_len = len(pred_pair_list)
        pred_pair_sim_matrix = array(zeros(pred_pair_list_len, pred_pair_list_len))

        # pred_pair_sim_matrix = []
        for i in range(pred_pair_list_len):
            for j in range(i):
                pred_pair_sim_matrix[i][j] = self.pred_pair_sim_calc(pred_pair_list[i], pred_pair_list[j])

        return pred_pair_sim_matrix + pred_pair_sim_matrix.T

    def pred_pair_sim_calc(self, pred_pair1, pred_pair2):
        cosine_sim_on_dbpedia = self.dboperator.get_ochiai_on_kb("DBPedia", pred_pair1[0], pred_pair2[0])
        cosine_sim_on_yago = self.dboperator.get_ochiai_on_kb("YAGO", pred_pair1[1], pred_pair2[1])

        return (cosine_sim_on_dbpedia + cosine_sim_on_yago) / 2

    def generate_queue(self, pred_pair_list):
        queue = []
        for pred_pair in pred_pair_list:
            pred_list1 = [pred_pair[0]]
            pred_list2 = [pred_pair[1]]

            queue.append((pred_list1, pred_list2))

        return queue

    def calc_pp_num_blocks(self, sim_matrix_w, cut_level):
        checked_node = []
        pp_blocks = []

        # get index array which contains indices that beyond the cut level
        beyond_threshold_indices = np.argwhere(sim_matrix_w > cut_level)
        sim_matrix_w_len = len(sim_matrix_w)
        # accelerate GC
        sim_matrix_w = None

        for i in range(sim_matrix_w_len):
            if i in checked_node:
                continue

            block = [i]
            while set(block) - set(checked_node):
                different_set = set(block) - set(checked_node)

                for ep in different_set:
                    similar_ep_list = np.argwhere(beyond_threshold_indices[:, 0] == ep)
                    block += beyond_threshold_indices[similar_ep_list[:, 0].tolist()][:, 1].tolist()
                    beyond_threshold_indices = np.delete(beyond_threshold_indices, similar_ep_list, 0)

                checked_node += list(different_set)

            # each block contains the sequence number of a predicate pair partion in partition_queue
            # e.g. pp_blocks = [[1,2,3],[4,5,6],[7,8,9]] means the first block contains the partitions
            # whose sequence numbers are 1 ,2 and 3.
            pp_blocks += [list(set(block))]

        return pp_blocks

    def merge_predicate_pairs(self, partition_queue, pp_num_blocks):
        new_partion_queue = []
        for block in pp_num_blocks:
            pp_list_on_kb1 = []
            pp_list_on_kb2 = []
            for i in block:
                pp_list_on_kb1 += partition_queue[i][0]
                pp_list_on_kb2 += partition_queue[i][2]

            new_partion_queue.append((pp_list_on_kb1, pp_list_on_kb2))

        return new_partion_queue

    def generate_entity_blocks(self, partition_queue):
        entity_blocks = []
        for block in partition_queue:
            entity_block1 = self.dboperator.get_entities("DBPedia", block[0])
            entity_block2 = self.dboperator.get_entities("YAGO", block[1])

            entity_blocks.append((entity_block1, entity_block2))

        return entity_blocks
