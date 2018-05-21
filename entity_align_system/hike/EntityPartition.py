# -*- coding:utf-8 -*-
'''
Entity partition by hike method
'''
from entity_align_system.models import DBConnector
from __future__ import division
from numpy import array, zeros, argmax


def partition(self, entity_blocks, data_dict):
    db_connector = DBConnector()
    cursor = db_connector.get_cursor()

    statement = "SELECT DISTINCT predicate FROM DBPedia"
    dbpedia_preds = cursor.execute(statement).fetchall()
    dbpedia_pred_num = len(dbpedia_preds)

    statement = "SELECT DISTINCT predicate FROM YAGO"
    yago_preds = cursor.execute(statement).fetchall()
    yago_pred_num = len(yago_preds)

    sim_matrix_w = array(zeros((dbpedia_pred_num, yago_pred_num)))
    for i in range(dbpedia_pred_num):
        for j in range(yago_pred_num):
            sim_matrix_w[i][j] = pred_sim_cal(dbpedia_preds[i], yago_preds[j], cursor)

    max_sim_pred_indices = argmax(sim_matrix_w)
    pred_pair_list = []
    pred_pair_num = min(dbpedia_pred_num, yago_pred_num)
    for i in range(pred_pair_num):
        dbpedia_pred=dbpedia_preds[i]
        yago_pred_index=max_sim_pred_indices[i]
        yago_pred=yago_preds[yago_pred_index]

        pred_pair_list.append((dbpedia_pred,yago_pred))

    db_connector.close_db()
    return pred_pair_list


def pred_sim_cal(pred1, pred2, cursor):
    # calculate intersection
    statement = """
        SELECT COUNT(subject, object) FROM DBPedia WHERE predicate=%s and (subject, object) in  
        (SELECT (subject, object) FROM YAGO WHERE predicate=%s )
        """ % (pred1, pred2)
    intersection_num = cursor.execute(statement).fetchone()

    # calculate union
    statement = "SELECT COUNT(DISTINCT subject, object) FROM DBPedia, YAGO WHERE predicate=%s or predicate=%s" \
                % (pred1, pred2)

    union_num = cursor.execute(statement).fetchone()

    return intersection_num / union_num
