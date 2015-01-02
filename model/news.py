from flask.ext.mongoengine import MongoEngine
from datetime import datetime

db = MongoEngine()

class Comment(db.EmbeddedDocument):
	username = db.StringField(required=True)
	content = db.StringField(required=True)
	date = db.DateTimeField(default=datetime.now)

class News(db.Document):
    title = db.StringField(max_length=120, unique=True)
    date = db.DateTimeField(default=datetime.now)
    abstract = db.StringField(max_length=200)
    news_pic = db.URLField()
    content = db.StringField()
    comments = db.ListField(db.EmbeddedDocumentField(Comment))
    tags = db.ListField(db.StringField(max_length=30))
    news_views = db.IntField(default=0)




