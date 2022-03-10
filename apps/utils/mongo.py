import pymongo
import motor.motor_asyncio


class XMongo(object):
    """ 封装数据库"""
    def __init__(self, host, port, database=None, username=None, password=None):
        """
        初始化
        :param host:
        :param port:
        :param username:
        :param password:
        :param database:
       """
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.database = database

    def async_mongo_db(self):
        """
        异步返回数据库
        :return:
        """
        if self.username and self.password:
            conn_url = 'mongodb://' + self.username + ':' + self.password + '@' + self.host + ':' + self.port + '/' + self.database
        else:
            conn_url = 'mongodb://' + self.host + ':' + self.port + '/' + self.database
        db = motor.motor_asyncio.AsyncIOMotorClient(conn_url)
        return db

    def mongo_db(self):
        """
        同步返回数据库
        :return:
        """
        conn = pymongo.MongoClient(host=self.host, port=self.port)
        db = conn[self.database]
        return db