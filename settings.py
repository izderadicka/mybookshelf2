import os.path

_base_dir = os.path.dirname(__file__)


DB_NAME = 'ebooks'
DB_HOST = 'localhost'
DB_USER = 'ebooks'
DB_PASSWORD = 'ebooks'

SQLALCHEMY_DATABASE_URI = 'postgresql://{user}:{password}@{host}/{db}'.format(db=DB_NAME,
                                                                              host=DB_HOST,
                                                                              user=DB_USER,
                                                                              password=DB_PASSWORD)
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = 'Pjk5EzGOcCOG5Rf1deqpZAvz17uUdZmWxJa3X/izSns'
MAX_CONTENT_LENGTH = 100 * 1024 * 1024

CACHE_CONTROL = 'max-age=20'
CACHE_EXPIRES = 20

# CORS
CORS_HOSTS = '*'  # or list of hosts ['localhost']
CORS_PORTS = None  # or (lower, upper) or []
CORS_SECURE = False  # if cors is allowed only for https

UPLOAD_DIR = os.path.join(_base_dir, 'app/data/uploads')
BOOKS_BASE_DIR = os.path.join(_base_dir, 'app/data/books')
BOOKS_FILE_SCHEMA = "%(author)s/%(title)s/%(author)s - %(title)s"

BOOKS_FILE_SCHEMA_SERIE = "%(author)s/%(serie)s/%(serie)s %(serie_index)d - %(title)s/%(author)s - %(serie)s %(serie_index)d - %(title)s"
BOOKS_RECON_DIR = "/books/books_recon"
BOOKS_DIR_UMASK = 0  # umask for uploaded files and their directories - consider that it should be RW for both web server and console user
# Conversion related
BOOKS_CONVERTED_DIR = "/books/books_converted"
CONVERSION_FORMATS = ['epub', 'mobi', 'fb2']


IMAGE_MAGIC = '/usr/bin/convert'


class Testing:
    DB_NAME = 'ebooks_test'
    DB_HOST = 'localhost'
    DB_USER = 'ebooks_test'
    DB_PASSWORD = 'ebooks'
    
    SQLALCHEMY_DATABASE_URI = 'postgresql://{user}:{password}@{host}/{db}'.format(db=DB_NAME,
                                                                                  host=DB_HOST,
                                                                                  user=DB_USER,
                                                                                  password=DB_PASSWORD)
    TESTING = True
    DEBUG = True


