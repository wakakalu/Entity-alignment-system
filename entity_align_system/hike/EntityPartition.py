# -*- coding:utf-8 -*-
'''
Entity partition by hike method
'''
from entity_align_system.models.connector import DBConnector
from __future__ import division
from numpy import *

def partition(self, entity_blocks, data_dict):
    db_connector = DBConnector()
    cursor = db_connector.get_cursor()


    statement = "SELECT DISTINCT predicate FROM DBPedia"
    dbpedia_preds = cursor.execute(statement).fetchall()
    dbpedia_pred_num = len(dbpedia_preds)

    statement = "SELECT DISTINCT predicate FROM YAGO"
    yago_preds = cursor.execute(statement).fetchall()
    yago_pred_num = len(yago_preds)

    matrix_w = array(zeros((dbpedia_pred_num,yago_pred_num)))
    for i in range(dbpedia_pred_num):
        for j in range(yago_pred_num):
            matrix_w[i][j] = pred_sim_cal(dbpedia_preds[i],yago_preds[j],cursor)

    pred_pair_list = []
    pred_pair_num = min(dbpedia_pred_num,yago_pred_num)
    for i in range(pred_pair_num):
        max_sim_pred_index=max(m)
        pred_pair_list

    db_connector.close_db()


def pred_sim_cal(pred1,pred2,cursor):

    # calculate intersection
    statement = """
    
    """%(pred1,pred2)
    intersection_num = cursor.execute(statement).fetchone()

    # calculate union
    statement = "SELECT COUNT(DISTINCT subject, object) FROM DBPedia, YAGO WHERE predicate=%s or predicate=%s"\
                %(pred1,pred2)

    union_num = cursor.execute(statement).fetchone()

    return intersection_num/union_num