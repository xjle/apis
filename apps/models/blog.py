from apps.ext import db
from datetime import datetime


class Blog(db.Document):
    """
    博客表
    """
    meta = {
        'collection': 'blog',
        'ordering': ['create_time'],
        'strict': False,
    }
    name = db.StringField(required=True)
    category = db.ListField(db.StringField())
    img = db.StringField()
    author = db.StringField(required=True)
    content = db.StringField(required=True)
    status = db.BooleanField(required=True)
    permission = db.BooleanField(required=True)
    is_del = db.IntField(default=1)
    create_time = db.DateTimeField(default=datetime.now)
    update_time = db.DateTimeField(default=datetime.now)
