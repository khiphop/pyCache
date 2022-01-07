# coding: utf-8
import pymysql
from orator import DatabaseManager, Model

from common.readconfig import ReadConfig


class HandleMySql:
    def __init__(self):
        self.data = ReadConfig()

    def mysql_connect(self):
        """连接数据库"""
        host = ""
        user = ""
        password = ""
        database = ""

        conn = pymysql.connect(
            host=host,
            user=user,
            password=password,
            database=database,
            charset="utf8"
        )

        cursor = conn.cursor()

        return {
            'db': conn,
            'cursor': cursor,
        }


if __name__ == '__main__':
    pass
