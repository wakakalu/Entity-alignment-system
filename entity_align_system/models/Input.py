# -*- coding:utf-8 -*-
from SPARQLWrapper import SPARQLWrapper
from entity_align_system.utils import Logging
from entity_align_system import HikeMetaClass
import traceback

DBPEDIA = "DBPedia"
YAGO = "YAGO"
DBPEDIA_ENDPOINT = "http://dbpedia.org/sparql"
YAGO_ENDPOINT = "https://linkeddata1.calcul.u-psud.fr/sparql"
DEFAULT_RETURN_FORMAT = "json"

logger = Logging.get_logger()
BATCH_SIZE = 10000


class Input(object):
    __metaclass__ = HikeMetaClass

    def __init__(self, dboperator):
        self.dboperator = dboperator

    def input_single_dataset(self, endpoint, statement, ret_format):
        # check endpoint value
        if endpoint:
            sparql = SPARQLWrapper(endpoint)
        else:
            raise ValueError("Endpoint has not been set")

        # check return format value
        if ret_format:
            sparql.setReturnFormat(ret_format)
        else:
            sparql.setReturnFormat(DEFAULT_RETURN_FORMAT)

        # check statement value
        if not statement:
            raise ValueError("Statement is none")
        sparql.setQuery(statement)

        try:
            return_value = self.sparql.query().convert()
        except Exception:
            logger.error("Exception occurs when retrieving data from DBPedia.\n%s", traceback.format_exc())

        return return_value

    def input_data(self):
        # input dbpedia data
        i = 0
        while True:
            offset = i * BATCH_SIZE
            statement = """
                       SELECT * 
                       where {?s ?p ?o}
                       OFFSET %s
                       LIMIT %s 
                   """ % (offset, BATCH_SIZE)

            dataset = self.input_single_dataset(DBPEDIA_ENDPOINT, statement)
            self.dboperator.insert_kbdata(DBPEDIA, dataset)

            if len(dataset) < BATCH_SIZE:
                break

            i += 1

        # input yago data
        i = 0
        while True:
            offset = i * BATCH_SIZE
            statement = """
                       SELECT * 
                       where {?s ?p ?o}
                       OFFSET %s
                       LIMIT %s 
                   """ % (offset, BATCH_SIZE)

            dataset = self.input_single_dataset(YAGO_ENDPOINT, statement)
            self.dboperator.insert_kbdata(YAGO, dataset)

            if len(dataset) < BATCH_SIZE:
                break

            i += 1

        self.dboperator.close_connection()