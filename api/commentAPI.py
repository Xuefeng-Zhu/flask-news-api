from flask import request, abort
from flask.ext.restful import Resource, reqparse
from model.news import News
from model.comment import Comment
from util.serialize import comments_serialize
from util.userAuth import auth_required

commnetParser = reqparse.RequestParser()
commnetParser.add_argument('title', type=str)
commnetParser.add_argument('username', type=str)
commnetParser.add_argument('content', type=str)

class CommentAPI(Resource):
	@auth_required
	def get(self):
		args = commnetParser.parse_args()
		title = args['title']
		news = News.objects(title=title).only('comments').first()
		if news is None:
			abort(400)
		return comments_serialize(news.comments)

	@auth_required
	def put(self):
		args = commnetParser.parse_args()
		title = args['title']
		username = args['username']
		content = args['content']

		if title is None or username is None or content is None:
			abort(400)

		comment = Comment(username=username, content=content)
		success = News.objects(title=title).only('comments').update_one(push__comments=comment)
		if success is 0:
			abort(400)

		return {'status': 'success'}






