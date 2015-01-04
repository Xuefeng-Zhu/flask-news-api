from flask.ext.mongoengine import MongoEngine
from flask_redis import Redis

redis_store = Redis()
db = MongoEngine()
