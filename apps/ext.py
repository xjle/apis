from flask_mail import Mail
from flask_caching import Cache
from flask_mongoengine import MongoEngine
from flask_pymongo import PyMongo

mail = Mail()
cache = Cache()
db = MongoEngine()  # 用户后台和管理后台需要使用ORM模块：MongoEngine
mongo = PyMongo()


def register_ext(app):
    """
    注册扩展
    :param app:
    :return:
    """
    # 邮箱
    mail.init_app(app)
    # redis缓存
    cache.init_app(app)
    # MongoEngine
    db.init_app(app)
    # pyMongo
    mongo.init_app(app)
