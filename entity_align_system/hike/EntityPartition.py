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

    def partition(self,merge_threshold):
        dbpedia_preds = self.dboperator.get_predicates("DBPedia")
        yago_preds = self.dboperator.get_predicates("YAGO")

        pred_pair_list = self.get_pred_pars(dbpedia_preds, yago_preds)

        if merge_threshold == None:
            merge_threshold = 0

        partition_queue = self.generate_queue(pred_pair_list)
        gap = 0.1
        cut_level = 1
        while cut_level >= merge_threshold:
            sim_matrix_w = self.refresh_sim_matrix(partition_queue)
            partition_queue = self.merge_predicate_pairs(sim_matrix_w)

            cut_level = cut_level - gap

        entity_pair_blocks = self.generate_entity_blocks(partition_queue)

        return entity_pair_blocks

    def get_pred_pars(self, dbpedia_preds, yago_preds):
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

    def generate_queue(self, pred_pair_list):
        pass

    def refresh_sim_matrix(self,pred_pair_list):
        pass

    def generate_entity_blocks(self,partition_queue):
        pass