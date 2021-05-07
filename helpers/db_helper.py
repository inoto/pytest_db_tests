import logging
import sqlite3
from sqlite3 import Error


class DBHelper(object):
    def __init__(self, db_path):
        try:
            self._connection = sqlite3.connect(db_path)
        except Error as e:
            logging.exception(e)

    def close(self):
        self._connection.close()

    @property
    def connection(self):
        return self._connection
