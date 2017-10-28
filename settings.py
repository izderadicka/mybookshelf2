import os.path
import logging

_base_dir = os.path.dirname(__file__)

DEBUG = os.getenv('MBS2_DEBUG', False)

if DEBUG:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)

DB_NAME = os.getenv('MBS2_DB_NAME', 'ebooks')
DB_HOST = os.getenv('MBS2_DB_HOST', 'localhost')
DB_PORT = os.getenv('MBS2_DB_PORT', 5432)
DB_USER = os.getenv('MBS2_DB_USER', 'ebooks')
DB_PASSWORD = os.getenv('MBS2_DB_PASSWORD', 'ebooks')

SQLALCHEMY_DATABASE_URI = os.getenv('MBS2_DB_URI', 'postgresql://{user}:{password}@{host}:{port}/{db}'
                                    .format(db=DB_NAME,
                                            host=DB_HOST,
                                            port=DB_PORT,
                                            user=DB_USER,
                                            password=DB_PASSWORD))
DELEGATED_HOST = os.getenv('MBS2_DELEGATED_HOST','localhost')
DELEGATED_PORT = os.getenv('MBS2_DELEGATED_PORT', 9080)
DELEGATED_URI = os.getenv('MBS2_DELEGATED_URI', 'tcp://{host}:{port}/ws'.\
                     format(host=DELEGATED_HOST, port=DELEGATED_PORT))

SQLALCHEMY_TRACK_MODIFICATIONS = False

SECRET_KEY = 'Pjk5EzGOcCOG5Rf1deqpZAvz17uUdZmWxJa3X/izSns'
SESSION_PROTECTION = 'strong'
REMEMBER_COOKIE_HTTPONLY = True
# REMEMBER_COOKIE_DURATION = 365
#this key is used for refresh token only 
SECRET_KEY2 = 'b7ssYqnBFu3+11NGxPT+lHfAIiTgpMG9EhKC1MRR1VWCN75n1zMhWouem2lPa7VUi7+U7xJKhYvfXjKldo9e2g'
TOKEN_VALIDITY_HOURS = 4
TOKEN_REFRESH_HOURS = 365 * 24 # validity of refresh token


# This is token for delegated connection to backend
# The connection must be over private trusted network, as this is fixed token, so it does not 
# provide much security
DELEGATED_TOKEN = 'SHsfvwv/proj7vie5BnsvhxZWnzga0AFzUjkFfQ27BG3IswYLCHXWhUNbuDO5B3MxTBtUMP7oNgN+QfDQ0uANQ'


MAX_CONTENT_LENGTH = 100 * 1024 * 1024

CACHE_CONTROL = 'max-age=20'
CACHE_EXPIRES = 20

# CORS
DISABLE_CORS=bool(os.getenv('MBS2_DISABLE_CORS', False)) # disable CORS -consider for  production
CORS_HOSTS = '*'  # or list of hosts ['localhost']
CORS_PORTS = None  # or (lower, upper) or []
CORS_SECURE = False  # if cors is allowed only for https


# data directories
DATA_BASE_DIR = os.getenv('MBS2_DATA_DIR', os.path.join(_base_dir, 'data'))

UPLOAD_DIR = os.path.join(DATA_BASE_DIR, 'uploads')
THUMBS_DIR = os.path.join(DATA_BASE_DIR, 'thumbs')
BOOKS_BASE_DIR = os.path.join(DATA_BASE_DIR, 'books')
BOOKS_CONVERTED_DIR = os.path.join(DATA_BASE_DIR, 'converted')

# umask for uploaded files and their directories - consider that it should
# be RW for both web server and console user
BOOKS_DIR_UMASK = 0

BOOKS_FILE_SCHEMA = "%(author)s/%(title)s(%(language)s)/%(author)s - %(title)s"
BOOKS_FILE_SCHEMA_SERIE = "%(author)s/%(serie)s/%(serie)s %(serie_index)d - %(title)s(%(language)s)/%(author)s - %(serie)s %(serie_index)d - %(title)s"

# Conversion related
CONVERSION_FORMATS = ['epub', 'mobi', 'fb2']
# sorted in order of preference of the source
CONVERTABLE_TYPES = ['doc', 'docx', 'odt', 'rtf', 'epub', 'mobi', 'fb2', 'htm', 'html', 'azw3', 'lit',
                     'pdb', 'chm', 'prc', 'txt', 'pdf', ]  # 'djvu' ,

CONVERTED_BATCH_PREFIX = '__batch__'

# these programs are used by engine backend
IMAGE_MAGIC = '/usr/bin/convert'  # IMAGEMAGIC BINARY
OOFFICE = '/usr/bin/soffice'  # OPEN OFFICE BINARY
CALIBRE_META_TOOL = '/usr/bin/ebook-meta'
CALIBRE_CONVERT_TOOL = '/usr/bin/ebook-convert'

THUMBNAIL_FILE="thumbnail.jpg"
THUMBNAIL_SIZE = (100, 140)  # width, height
COVER_SIZE = (320, 452)
MAX_COVER_FILE_SIZE = 10*1024*1024


class Testing:
    DB_NAME = 'ebooks_test'
    DB_HOST = 'localhost'
    DB_USER = 'ebooks_test'
    DB_PASSWORD = 'ebooks'

    SQLALCHEMY_DATABASE_URI = os.getenv('MBS2_TEST_DB_URI', 'postgresql://{user}:{password}@{host}/{db}'\
                                        .format(db=DB_NAME,
                                          host=DB_HOST,
                                          user=DB_USER,
                                          password=DB_PASSWORD))
    TESTING = True
    DEBUG = True
