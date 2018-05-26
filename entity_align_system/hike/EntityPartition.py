# -*- coding:utf-8 -*-
'''
Entity partition by hike method
'''
from __future__ import division
from numpy import array, zeros, argmax
from entity_align_system import HikeMetaClass


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
            partition_queue = self.merge_predicate_pairs(partition_queue, sim_matrix_w, cut_level)

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

        pred_pair_sim_matrix = []
        for i in range(pred_pair_list_len):
            pred_pair_sim_matrix += [[]]
            for j in range(i):
                pred_pair_sim = self.pred_pair_sim_calc(pred_pair_list[i], pred_pair_list[j])
                pred_pair_sim_matrix[i].append(pred_pair_sim)

        return pred_pair_sim_matrix

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

    def merge_predicate_pairs(self, partition_queue, sim_matrix_w, cut_level):

        pass

    def generate_entity_blocks(self, partition_queue):
        entity_blocks = []
        for block in partition_queue:
            entity_block1 = self.dboperator.get_entities("DBPedia", block[0])
            entity_block2 = self.dboperator.get_entities("YAGO", block[1])

            entity_blocks.append((entity_block1, entity_block2))

        return entity_blocks
