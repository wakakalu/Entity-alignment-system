# -*- coding:utf-8 -*-
from entity_align_system.models.DBOperator import DBOperatorMap
import config

class HikeMetaClass(type):
    def __call__(cls, *args, **kwargs):
        obj = cls.__new__(cls,*args,**kwargs)
        args_list = list(args)

        dbtype = cls.get_dbtype()
        args_list.append(DBOperatorMap[dbtype])
        obj.__init__(*args_list,**kwargs)

        return obj

    def get_dbtype(self):
        return config.get_config_item()