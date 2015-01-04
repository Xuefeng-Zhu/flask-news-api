from flask import request, abort, json
from flask.ext.restful import Resource, reqparse
from newspaper import Article
import urlparse
from serialize import article_serialize


class ArticleAPI(Resource):
	def get(self, link):
		if urlparse.urlparse(link).scheme not in ('http', 'https'):
			abort(400)

		article = Article(link, keep_article_html=True)
		article.download()
		article.parse()

		return article_serialize(article)
