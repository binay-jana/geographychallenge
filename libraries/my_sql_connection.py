import MySQLdb
from constants import local_settings


class MySQLConnection(object):
    def __init__(
            self, host=local_settings.mysql_host,
            port=local_settings.mysql_port,
            user=local_settings.mysql_user,
            passwd=local_settings.mysql_password,
            database=local_settings.mysql_database):
        self.db = MySQLdb.connect(host=host, port=port, user=user,
                                  passwd=passwd, db=database)

    def get(self, query, args=None):
        cursor = self.db.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(query, args)
        row = cursor.fetchone()
        return row

    def insert(self, query, args):
        cursor = self.db.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(query, args)
        self.db.commit()
        return cursor.lastrowid

    def query(self, query):
        cursor = self.db.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(query)
