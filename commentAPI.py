from flask import request, abort
from flask.ext.restful import Resource, reqparse
from model import redis_store
from model.news import News
from model.comment import Comment
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)

commnetParser = reqparse.RequestParser()
commnetParser.add_argument('token', type=str)
commnetParser.add_argument('title', type=str)
commnetParser.add_argument('username', type=str)
commnetParser.add_argument('content', type=str)


class CommentAPI(Resource):
	def get(self):
		args = commnetParser.parse_args()
		# token = args['token']
		title = args['title']
		news = News.objects(title=title).only('comments').first()
		if news is None:
			abort(400)
		return comments_serialize(news.comments)

	def put(self):
		args = commnetParser.parse_args()
		# token = args['token']
		title = args['title']
		username = args['username']
		content = args['content']

		if title is None or username is None or content is None:
			abort(400)

		news = News.objects(title=title).only('comments').first()
		if news is None:
			abort(400)

		comment = Comment(username=username, content=content)
		if news.comments is None:
			news.comments = [comment]
		else:
			news.comments.append(comment)
		news.save()

		return {'status': 'success'}






