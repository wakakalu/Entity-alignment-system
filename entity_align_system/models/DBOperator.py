# -*- coding:utf-8 -*-
from __future__ import division
from entity_align_system.utils import Logging
import MySQLdb
import math

logger = Logging.get_logger()

class MysqlOperator(object):
    # constant
    DEFAULT_HOST = "localhost"
    DEFAULT_USER = "root"
    DEFAULT_DB = "hike"

    # variable
    db = None

    def connect_db(self,dbname=None):
        if dbname == None:
            dbname = self.DEFAULT_DB
        if self.db == None:
            self.db = MySQLdb.connect(host=self.DEFAULT_HOST, user=self.DEFAULT_USER, db=dbname, charset='utf8')

        self.cursor = self.db.cursor()

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
        pred_query_criteria1 = " or predicate=".join(preds1)
        pred_query_criteria2 = " or predicate=".join(preds2)
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

    def get_entities(self, kbname, predicates):
        statement = "SELECT subject FROM %s WHERE predicate=%s" % (kbname, " or predicate=".join(predicates))

        return self.cursor.execute(statement)

    def insert_kbdata(self, kbname, dataset):
        statement = "INSERT INTO %s(subject, predicate, object) values" % kbname
        statement += "(%s, %s, %s)"
        # self.cursor.executemany(statement, dataset)
        index = 0
        for data in dataset:
            try:
                self.cursor.execute(statement,data)
                self.db.commit()
                index += 1
            except Exception as e:
                logger.error("Error occurs when inserting data\n%s", e.message)

    def insert_entity_pairs(self, matched_entity_pairs):
        pass

    def close_connection(self):
        self.db.close()
        self.db = None


class MongoOperator(object):
    pass


DBOperatorMap = {
    "mysql": MysqlOperator(),
    "mongo": MongoOperator()
}
