# -*- coding:utf-8 -*-
import MysqlOperator
import MongoOperator

DBOperatorMap = {
    "mysql" : MysqlOperator(),
    "mongo" : MongoOperator()
}