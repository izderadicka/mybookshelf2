import os

SQLALCHEMY_DATABASE_URI='postgresql://ebooks:ebooks@localhost/ebooks' 
SQLALCHEMY_TRACK_MODIFICATIONS=False

RESOURCE_METHODS = ['GET', 'POST', 'DELETE']
ITEM_METHODS = ['GET', 'PATCH', 'DELETE']

CACHE_CONTROL = 'max-age=20'
CACHE_EXPIRES = 20
#CORS

X_DOMAINS='*'
X_HEADERS=['Authorization', 'Content-type']


