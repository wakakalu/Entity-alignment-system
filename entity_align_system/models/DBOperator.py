# -*- coding:utf-8 -*-
from __future__ import division
from entity_align_system.models.MysqlConnector import MysqlConnector
import math

class MysqlOperator(object):
    def connect_db(self):
        self.db_connector = MysqlConnector()
        self.cursor =  self.db_connector.get_cursor()

    def get_predicates(self, kbname):
        statement = "SELECT DISTINCT predicate FROM %s" % kbname
        return self.cursor.execute(statement).fetchall()

    def get_intersection(self, pred1, pred2):
        # calculate intersection
        statement = """
            SELECT COUNT(subject, object) FROM DBPedia WHERE predicate=%s and (subject, object) in  
            (SELECT (subject, object) FROM YAGO WHERE predicate=%s )
            """ % (pred1, pred2)
        return self.cursor.execute(statement).fetchone()

    def get_union(self, pred1, pred2):
        # calculate union
        statement = "SELECT COUNT(DISTINCT subject, object) FROM DBPedia, YAGO WHERE predicate=%s or predicate=%s" \
                    % (pred1, pred2)

        return self.cursor.execute(statement).fetchone()

    def get_ochiai_on_kb(self, kbname, preds1, preds2):
        pred_query_criteria1 = " or ".join(preds1)
        pred_query_criteria2 = " or ".join(preds2)
        statement = """
            SELECT COUNT(subject, predicate, object) FROM (
                SELECT subject, predicate, object FROM %s WHERE predicate=%s
                INTERSECT
                SELECT subject, predicate, object FROM %s WHERE predicate=%s
            )
        """ % (kbname, pred_query_criteria1, kbname, pred_query_criteria2)
        intersection_size = self.cursor.execute(statement)

        statement = "SELECT COUNT(subject, predicate, object) FROM %s WHERE predicate=%s" % (
        kbname, pred_query_criteria1)
        size1 = self.cursor.execute(statement)

        statement = "SELECT COUNT(subject, predicate, object) FROM %s WHERE predicate=%s" % (
        kbname, pred_query_criteria2)
        size2 = self.cursor.execute(statement)

        return intersection_size / math.sqrt(size1 * size2)

    def insert_kbdata(self, dataset):
        pass

    def insert_entity_pairs(self, matched_entity_pairs):
        pass

    def close_connection(self):
        self.db_connector.close()

class MongoOperator(object):
    pass

DBOperatorMap = {
    "mysql" : MysqlOperator(),
    "mongo" : MongoOperator()
}
