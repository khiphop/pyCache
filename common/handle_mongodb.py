# coding: utf-8

import pymongo
from common.readconfig import ReadConfig


class HandleMongoDB:
    def __init__(self):
        self.data = ReadConfig()

    def mongodb_connect(self):
        """连接数据库"""
        mongodb_ip = str(self.data.get_db("mongodb_ip"))
        mongodb_port = int(self.data.get_db("mongodb_port"))
        mongodb_auth = str(self.data.get_db("mongodb_auth"))
        mongodb_password = str(self.data.get_db("mongodb_password"))

        client = pymongo.MongoClient(mongodb_ip, mongodb_port)
        self.mongodb = client['erp']
        self.mongodb.authenticate(mongodb_auth, mongodb_password)

        return self.mongodb

    def select_col(self, col):
        return self.mongodb[str(col)]


if __name__ == '__main__':
    pass
