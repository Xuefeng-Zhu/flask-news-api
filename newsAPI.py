from flask import request, abort, json
from flask.ext.restful import Resource, reqparse
from model.redis import redis_store
from model.news import News
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)
import boto
import os


SECRET_KEY = 'flask is cool'

def verify_auth_token(token):
    s = Serializer(SECRET_KEY)
    try:
        username = s.loads(token)
    except SignatureExpired:
        return False    # valid token, but expired
    except BadSignature:
        return False    # invalid token
    if redis_store.get(username) == token:
        return True
    else:
        return False


newsParser = reqparse.RequestParser()
newsParser.add_argument('title', type=str)
newsParser.add_argument('abstract', type=str)
newsParser.add_argument('news_pic', type=str)
newsParser.add_argument('content')

def news_serialize(news):
    result = {}
    for key in news:
        if key == 'id' or key == 'comments':
            pass
        elif key == 'date':
            result[key] = news[key].strftime("%B %d, %Y %I:%M%p")
        else:
            result[key] = news[key]
    return result    


class NewsAPI(Resource):
    def options(self):
        pass

    def get(self):
        args = newsParser.parse_args()
        title = args['title']

        if title is None:
            abort(400)

        news = News.objects(title=title).exclude('comments').first()
        if news is None:
            abort(400)
        news.update(inc__news_views=1)

        return news_serialize(news)
        

    def put(self):
        args = newsParser.parse_args()
        title = args['title']
        abstract = args['abstract']
        news_pic = args['news_pic']
        content = args['content']
        tags = request.json['tags']

        if title is None:
            abort(400)

        try:
            news = News(title=title, abstract=abstract, news_pic=news_pic, content=content, tags=tags)
            news.save()
        except:
            print title
            abort(400)

        return news_serialize(news)

class NewsImageAPI(Resource):
    def options(self):
        pass

    def post(self):
        # verify token 
        # if token is None:
        #     abort(400)
        # email = verify_auth_token(token) 
        # if email is None:
        #     abort(400)

        uploaded_file = request.files['file']

        conn = boto.connect_s3(os.environ['S3_KEY'], os.environ['S3_SECRET'])
        bucket = conn.get_bucket('news-pic')
        key = bucket.new_key(uploaded_file.filename)
        key.set_contents_from_file(uploaded_file)

        return {'url': 'https://s3.amazonaws.com/news-pic/%s' %uploaded_file.filename}

def news_list_serialize(news_list):
    result = []
    for news in news_list:
        temp = {}
        for key in news:
            if key == 'id' or key == 'content' or key == 'comments':
                pass
            elif key == 'date':
                temp[key] = news[key].strftime("%B %d, %Y %I:%M%p")
            elif news[key] == None:
                temp[key] = ''
            else:
                temp[key] = news[key]
        temp['news_url'] = "http://xuefeng-zhu.github.io/news-client/user/#/view/%s" %news['title']
        result.append(temp)
    return result


class NewsListAPI(Resource):
    def get(self, tags, page):
        if tags != 'all':
            tags = tags.split('+')
            news_list = News.objects(tags__all = tags).exclude('content', 'comments').order_by('-date')[10*page : 10*(page+1)]
        else:
            news_list = News.objects().exclude('content', 'comments').order_by('-date')[10*page : 10*(page+1)]
        
        return news_list_serialize(news_list)           

searchParser = reqparse.RequestParser()
searchParser.add_argument('search', type=str)
searchParser.add_argument('page', type=int)

class SearchNewsAPI(Resource):
    def get(self):
        args = searchParser.parse_args()
        search = args['search']
        tags = request.json['tags']
        page = args['page']

        if tags is None or tags is []:
            news_list = News.objects().exclude('content', 'comments').order_by('-date')
        else:
            news_list = News.objects(tags__all = tags).exclude('content', 'comments').order_by('-date')

        if search is not None and search is not '':
            news_list = news_list.filter(title__contains =search)

        
        return news_list_serialize(news_list[10*page : 10*(page+1)])  

