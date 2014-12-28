from flask import Flask, request, abort
from flask.ext.restful import Resource, Api
from flask.ext.restful.utils import cors
from model.news import db
from model.redis import redis_store
from newsAPI import NewsAPI, NewsImageAPI, NewsListAPI

app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {
    'db': 'flask-test',
    'host': 'ds027741.mongolab.com',
    'port': 27741,
    'username': 'flask-admin',
    'password': '123123'
}

app.config['REDIS_URL'] = "redis://:123123@pub-redis-17784.us-east-1-2.1.ec2.garantiadata.com:17784/0"

db.init_app(app)
redis_store.init_app(app)

api = Api(app)
api.decorators=[cors.crossdomain(origin='*', headers='my-header, accept, content-type')]

api.add_resource(NewsAPI, '/news')
api.add_resource(NewsImageAPI, '/upload_news_image')
api.add_resource(NewsListAPI, '/news_list')


if __name__ == '__main__':
    app.run(debug=True)


