from apps.ext import db
from datetime import datetime


class User(db.Document):
    """
    用户表
    """
    meta = {
        'collection': 'user',
        'ordering': ['create_time'],
        'strict': False,
    }
    mail = db.StringField(required=True)
    password = db.StringField(required=True)
    phone = db.StringField()
    nickname = db.StringField()
    role = db.IntField(default=1)
    wd = db.IntField(default=0)
    level = db.IntField(default=0)
    is_stop = db.IntField(default=1)
    create_time = db.DateTimeField(default=datetime.now)
    update_time = db.DateTimeField(default=datetime.now)
