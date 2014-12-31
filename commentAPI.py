from flask import request, abort
from flask.ext.restful import Resource, reqparse
from model.redis import redis_store
from model.news import News, Comment
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)

commnetParser = reqparse.RequestParser()
commnetParser.add_argument('token', type=str)
commnetParser.add_argument('title', type=str)
commnetParser.add_argument('username', type=str)
commnetParser.add_argument('content', type=str)

class CommentAPI(Resource):
	def put(self):
		args = commnetParser.parse_args()
		# token = args['token']
		title = args['title']
		username = args['username']
		content = args['content']

		if title is None or username is None or content is None:
			abort(400)

		news = News.objects(title=title).first()
		if news is None:
			abort(400)

		comment = Comment(username=username, content=content)
		if news.comments is None:
			news.comments = [comment]
		else:
			news.comments.append(comment)
		news.save()

		return {'status': 'success'}






