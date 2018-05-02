# -*- coding:utf-8 -*-
import traceback

from SPARQLWrapper import SPARQLWrapper
import logging

DBPEDIA = "DBPedia"
YAGO = "YAGO"
DBPEDIA_ENDPOINT = "http://dbpedia.org/sparql"
YAGO_ENDPOINT = "https://linkeddata1.calcul.u-psud.fr/sparql"
DEFAULT_RETURN_FORMAT = "json"

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
        logging.error("Exception occurs when retrieving data from DBPedia.\n%s", traceback.format_exc())

    return return_value


def input_data():
    statement = ""
    
    # Compose data dict
    data_dict = {}
    data_dict[DBPEDIA] = input_single_dataset(DBPEDIA_ENDPOINT, statement)
    data_dict[YAGO] = input_single_dataset(YAGO_ENDPOINT, statement)

    return data_dict