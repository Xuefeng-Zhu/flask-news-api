from flask import request, abort, json
from flask.ext.restful import Resource, reqparse
from newspaper import Article
import urlparse


def article_serialize(article):
	result = {
		'title': article.title,
		'news_pic': article.top_image,
		'content': article.text
	}
	return result


class ArticleAPI(Resource):
	def get(self, link):
		if urlparse.urlparse(link).scheme not in ('http', 'https'):
			abort(400)

		article = Article(link)
		article.download()
		article.parse()

		return article_serialize(article)