import os.path

_base_dir=os.path.dirname(__file__)

SQLALCHEMY_DATABASE_URI='postgresql://ebooks:ebooks@localhost/ebooks' 
SQLALCHEMY_TRACK_MODIFICATIONS=False
SECRET_KEY='Pjk5EzGOcCOG5Rf1deqpZAvz17uUdZmWxJa3X/izSns'

CACHE_CONTROL = 'max-age=20'
CACHE_EXPIRES = 20

#CORS
CORS_HOSTS='*' # or list of hosts ['localhost']
CORS_PORTS=None # or (lower, upper) or []
CORS_SECURE=False # if cors is allowed only for https

BOOKS_BASE_DIR=os.path.join(_base_dir, 'app/data/books')
BOOKS_FILE_SCHEMA="%(author)s/%(title)s/%(author)s - %(title)s"

BOOKS_FILE_SCHEMA_SERIE="%(author)s/%(serie)s/%(serie)s %(serie_index)d - %(title)s/%(author)s - %(serie)s %(serie_index)d - %(title)s"
BOOKS_RECON_DIR="/books/books_recon"
BOOKS_DIR_UMASK=0 # umask for uploaded files and their directories - consider that it should be RW for both web server and console user
#Conversion related
BOOKS_CONVERTED_DIR="/books/books_converted"
CONVERSION_FORMATS=['epub', 'mobi', 'fb2']


class Testing:
    SQLALCHEMY_DATABASE_URI='postgresql://ebooks_test:ebooks@localhost/ebooks_test' 
    TESTING=True
    DEBUG=True


