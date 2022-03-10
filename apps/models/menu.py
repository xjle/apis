from apps.ext import db
from datetime import datetime


class Menu(db.Document):
    """
    菜单表
    """
    meta = {
        'collection': 'menu',
        'ordering': ['create_time'],
        'strict': False,
    }
    mid = db.StringField(required=True, unique=True)
    name = db.StringField(required=True)
    url = db.StringField(required=True)
    icon = db.StringField()
    role = db.IntField(default=1)
    status = db.BooleanField(default=True)
    create_time = db.DateTimeField(default=datetime.now)
    update_time = db.DateTimeField(default=datetime.now)
