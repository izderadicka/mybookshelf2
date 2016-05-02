import os

SQLALCHEMY_DATABASE_URI='postgresql://ebooks:ebooks@localhost/ebooks' 
SQLALCHEMY_TRACK_MODIFICATIONS=False
SECRET_KEY='Pjk5EzGOcCOG5Rf1deqpZAvz17uUdZmWxJa3X/izSns'

CACHE_CONTROL = 'max-age=20'
CACHE_EXPIRES = 20

#CORS
CORS_HOSTS='*' # or list of hosts ['localhost']
CORS_PORTS=None # or (lower, upper) or []
CORS_SECURE=False # if cors is allowed only for https



class Testing:
    SQLALCHEMY_DATABASE_URI='postgresql://ebooks_test:ebooks@localhost/ebooks_test' 
    TESTING=True
    DEBUG=True


