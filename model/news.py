from flask.ext.mongoengine import MongoEngine
from datetime import datetime

db = MongoEngine()

class News(db.Document):
    title = db.StringField(max_length=120, unique=True)
    date = db.DateTimeField(default=datetime.now)
    abstract = db.StringField()
    news_pic = db.URLField()
    content = db.StringField()
    tags = db.ListField(db.StringField(max_length=30))



