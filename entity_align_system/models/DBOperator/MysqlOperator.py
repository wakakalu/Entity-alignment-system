# -*- coding:utf-8 -*-
import entity_align_system.models.MysqlConnector


class MysqlOperator(object):
    db_connector = entity_align_system.models.MysqlConnector()
    cursor = db_connector.get_cursor()

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
        statement = """
        SELECT subject, predicate, object FROM %s WHERE predicate=%s
        INTERSECT
        SELECT subject, predicate, object FROM %s WHERE predicate=%s
        
        """ % (kbname, " or ".join(preds1), kbname, " or ".join(preds2))

        return self.cursor.execute(statement)

    def insert_kbdata(self, dataset):
        pass

    def insert_entity_pairs(self, matched_entity_pairs):
        pass

    def close_connection(self):
        self.db_connector.close()
