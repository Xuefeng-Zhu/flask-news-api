flask-news-api
==============

Flask News API is built on Flask-restful to provide simple news management functionality. 

Such as

+ Post an article 
+ Edit an article
+ Delete an article 
+ View an article 
+ News list
+ Saerch for specific news
+ Load an article from other sources 
+ Make comments to an article

This api is supposed to be used with [Flask User API](https://github.com/Xuefeng-Zhu/flask-user-api)

## Demo 
The API is currently deployed on Heroku

[Demo](http://lit-everglades-2593.herokuapp.com/)

Please fetch token through [Flask User API](https://github.com/Xuefeng-Zhu/flask-user-api) in order to use this API

## Architecture
Flask News API stores data in mongodb. In order to access the main functionality, users need to use the token from **login** endpoint using [Flask User API](https://github.com/Xuefeng-Zhu/flask-user-api). Each news, news list, and comments are cached in order to minimize the database look up and increast the response time.

This is a list files or directories for flask user api

+ `/api` - scripts implement actual api functions
+ `/model` - define database model
+ `/util` - utilities for sending email, authorization, and serialization 
+ `app.py` - script to bootstrap the app
+ `config.py` - configuration for the app  
+ `Procgile` - heroku server configuration
+ `requirements.txt` - dependency file

## Usage

#### Install dependency 
	pip install -r requirements.txt

#### Config
	change the arguments in config.py	
	
#### Run 
	python app.py
	
#### Manual
```
Create News 
curl localhost:5000/news -X PUT -d "title=new1" -d "abstract=bla bla bla" -d "news_pic=http://www.cnbeta.com" -d "content=bla bla bla"

Edit News 
curl localhost:5000/news -X POST -d "id=54a62c56077d3500077f23c7" -d "title=new1" -d "abstract=bla bla bla" -d "news_pic=http://www.cnbeta.com" -d "content=bla bla bla"

Delete News 
curl localhost:5000/news -X DELETE -d "id=54a62c56077d3500077f23c7"

Upload News Image 
curl --form file=@icon.png --form press=OK localhost:5000/upload_news_image/ -X POST

Get News List
curl localhost:5000/news_list/tagA+tagB/page #

Search News List
curl localhost:5000/search_news -X POST -d "search=test" -d "tags=[]" -d "page=0"

Get News detail
curl localhost:5000/news -X GET -d "title=xxx"

Put Comment:
curl localhost:5000/comment -X PUT --header "token: from login api" -d "title=test" -d "username=test-user" -d "content=bla bla bla"

Get Comment:
curl localhost:5000/comment -X GET --header "token: from login api" -d "title=test" 

Load Article:
curl localhost:5000/load_article/http://www.engadget.com/2015/01/01/us-supreme-court-moving-to-digital-filing-system-in-2016/ -X GET

```
	
#### Deployment on Heroku
Just create a new heroku application, and push the code to heroku

	heroku create
	git push heroku
	heroku ps:scale web=1

## Acknowledgements
This project is built on following libraries

+ [boto](https://github.com/boto/boto)
+ [Flask](https://github.com/mitsuhiko/flask)
+ [flask-mongoengine](https://github.com/MongoEngine/flask-mongoengine)
+ [flask-redis](https://github.com/rhyselsmore/flask-redis)
+ [Flask-RESTful](https://github.com/flask-restful/flask-restful)
+ [gunicorn](https://github.com/benoitc/gunicorn)
