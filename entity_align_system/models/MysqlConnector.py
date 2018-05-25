# -*- coding:utf-8 -*-
import MySQLdb

DEFAULT_PASS="hikepass"
DEFAULT_HOST="localhost"
DEFAULT_USER="root"
DEFAULT_DB="hike"

class MysqlConnector(object):
    db = None

    def _connect_db(self,dbname=None):
        if dbname == None:
            dbname = DEFAULT_DB

        if self.db == None:
            self.db = MySQLdb.connect(DEFAULT_HOST, DEFAULT_USER, DEFAULT_PASS, dbname, charset='utf8')

    def get_cursor(self):
        self._connect_db()
        return self.db.cursor()

    def close_db(self):
        self.db.close()
        self.db = None