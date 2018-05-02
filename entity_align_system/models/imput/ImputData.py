# -*- coding:utf-8 -*-
import traceback

from SPARQLWrapper import SPARQLWrapper, JSON, Wrapper
import logging

__allow_return_formats__ = Wrapper._allowedFormats
__allow_request_method__ = Wrapper._allowedRequests

DBPEDIA = "DBPedia"
YAGO = "YAGO"

class DBPediaModel:
    DEFAULT_STATEMENT = ""
    DEFAULT_RETURN_FORMAT = JSON

    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    sparql.setQuery(DEFAULT_STATEMENT)
    sparql.setReturnFormat(DEFAULT_RETURN_FORMAT)

    def set_statement(self, statement):
        self.sparql.setQuery(statement)

    def set_return_format(self, return_format=None):
        if return_format in self.__allow_return_formats__:
            self.sparql.setReturnFormat(return_format)
        else:
            self.sparql.setReturnFormat(self.DEFAULT_RETURN_FORMAT)

    def imput_data(self):
        try:
            return_value = self.sparql.query().convert()
        except Exception:
            logging.error("Exception occurs when retrieving data from DBPedia.\n%s", traceback.format_exc())

        return return_value

class YAGOModel(object):
    def imput_data(self):
        pass

def input_data(self, dict=None):
    dbpedia = DBPediaModel()
    yago = YAGOModel()

    data_dict = {}
    data_dict[DBPEDIA] = dbpedia.imput_data()
    data_dict[YAGO] = yago.imput_data()

    return data_dict