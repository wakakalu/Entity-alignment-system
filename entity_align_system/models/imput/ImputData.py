# -*- coding:utf-8 -*-
from SPARQLWrapper import SPARQLWrapper, JSON, Wrapper
import logging

__allow_return_formats__ = Wrapper._allowedFormats
__allow_request_method__ = Wrapper._allowedRequests

class DBPediaModel:
    DEFAULT_STATEMENT = ""
    DEFAULT_RETURN_FORMAT = JSON

    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    sparql.setQuery(DEFAULT_STATEMENT)
    sparql.setReturnFormat(DEFAULT_RETURN_FORMAT)

    def set_statement(self, statement):
        self.sparql.setQuery(statement)

    def set_return_format(self, return_format):
        if return_format in self.__allow_return_formats__:
            self.sparql.setReturnFormat(return_format)
        else:
            self.sparql.setReturnFormat(self.DEFAULT_RETURN_FORMAT)

    def imput_data(self):
        try:
            return_value = self.sparql.query().convert()
        except Exception:
            logging
        return return_value

class YAGOModel(object):
    pass

def input_data(self):
    pass