from flask import request, abort, json
from flask.ext.restful import Resource, reqparse
from model.redis import redis_store
from model.news import News
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)
import boto

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
newsParser.add_argument('tags', type=list)

class NewsAPI(Resource):
    def options(self):
        pass

    def get(self):
        args = newsParser.parse_args()
        title = args['title']

        if title is None:
            abort(400)

        news = News.objects(title=title).first()
        if news is None:
            abort(400)

        result = {}
        for key in news:
            if key == 'id':
                pass
            elif key == 'date':
                result[key] = news[key].strftime("%B %d, %Y %I:%M%p")
            else:
                result[key] = news[key]
        return result


    def put(self):
        args = newsParser.parse_args()
        title = args['title']
        abstract = args['abstract']
        news_pic = args['news_pic']
        content = args['content']
        tags = args['tags']

        if title is None:
            abort(400)

        # try:
        news = News(title=title, abstract=abstract, news_pic=news_pic, content=content, tags=tags)
        news.save()
        # except:
            # abort(400)

        result = {}
        for key in news:
            if key == 'id':
                pass
            elif key == 'date':
                result[key] = news[key].strftime("%B %d, %Y %I:%M%p")
            else:
                result[key] = news[key]
        return result

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

        conn = boto.connect_s3('AKIAI6Y5TYNOTCIHK63Q', 'mmIpQx6mX/oFjZC6snQ7anO0yTOhEbpqPf2pcr0E')
        bucket = conn.get_bucket('news-pic')
        key = bucket.new_key(uploaded_file.filename)
        key.set_contents_from_file(uploaded_file)

        return {'url': 'https://s3.amazonaws.com/news-pic/%s' %uploaded_file.filename}

class NewsListAPI(Resource):
    def get(self, page):
        result = []
        newsList = News.objects().exclude('content').order_by('-date')[10*page : 10*(page+1)]
        for news in newsList:
            temp = {}
            for key in news:
                if key == 'id' or key == 'content':
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


