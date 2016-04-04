import os

MONGO_HOST = os.environ.get('MONGO_HOST', 'localhost')
MONGO_PORT = os.environ.get('MONGO_PORT', 27017)
MONGO_USERNAME = os.environ.get('MONGO_USERNAME', 'ebooks')
MONGO_PASSWORD = os.environ.get('MONGO_PASSWORD', 'ebooks')
MONGO_DBNAME = os.environ.get('MONGO_DBNAME', 'ebooks')

RESOURCE_METHODS = ['GET', 'POST', 'DELETE']
ITEM_METHODS = ['GET', 'PATCH', 'DELETE']

CACHE_CONTROL = 'max-age=20'
CACHE_EXPIRES = 20
#CORS

X_DOMAINS='*'
X_HEADERS=['Authorization']

LANGUAGES={'cs':'Czech',
           'en': 'English',
           'ru': 'Russian',
           'sk': 'Slovak',
           }
FORMATS={
    'pdf':('application/pdf', 'PDF document'),
    'txt':('text/plain', 'Plain text document'),
    'pdb':('application/vnd.palm', 'Palm Document'),
    'rtf':('application/rtf', 'RTF Document'),
    'doc':('application/msword', 'MS Word Document'),
    'mobi':('application/x-mobipocket-ebook', 'Mobipocket Ebook'),
    'prc':('application/vnd.palm ', 'Palm/Mobipocket Document'),
    'epub':('application/epub+zip', 'Open Publication Structure eBook'),
    'odt':('application/vnd.oasis.opendocument.text ', 'OpenOffice Document'),
    'djvu':('image/vnd.djvu', 'DJVU Document'),
    'html':('text/html', 'HTML File'),
    'htm':('text/html', 'HTML'),
    'chm':('application/octet-stream', 'Compiled HTML'),
    'lit':('application/x-ms-reader ', 'MS Reader Ebook'),
    'fb2':('text/xml', 'Fiction Book 2'),
    'docx':('application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'MS Word XML document'),
    'azw3':('application/x-mobi8-ebook', 'Amazon KF8 eBook File'),
    }

source={'type':'dict',
        'schema':{
            '_id': {
                'type':'objectid',
                'required':True
                },
            'format': {
                'type':'string',
                'minlength':1,
                'maxlength':20,
                'allowed':list(FORMATS.keys()),
                'required':True,
                },
            'size': {
                'type': 'integer',
                'required':True,
                },
            'hash': {
                'type':'string',
                'maxlength':64,
                'minlength':4,
                'required':True
                  },
            'location': {
                'type':'string',
                'maxlength':1024,
                'minlength':4,
                'required': True
                },
            'original_name': {
                'type':'string',
                'maxlength':1024,
                'minlength':4,
                'required': True
                },
            'quality': {
                'type':'number',
                'min':0,
                'max':100,
                'nullable':True
                }
            }
        }
author={'type': 'dict',
       'schema': {
            'lastname': {
                'type':'string',
                'minlength':1,
                'maxlength':255,
                'required':True 
                },
            'firstname': {
                'type':'string',
                'maxlength': 255,
                'required':False,
                },
            }
        }

ebooks={
        'item_title':'ebook',
        #'allow_unknown': True,
        'schema': {
                   'title': {
                       'type':'string',
                       'minlength':1,
                       'maxlength':255,
                       'required':True,
                       },
                   'authors': {
                        'type':'list',
                        'schema': author,
                        'maxlength':100
                    },
                    'series': {
                        'type':'string',
                        'maxlength':255,
                        'nullable': True
                        },
                    'series_index':{
                        'type':'integer',
                        'max':999,
                        'nullable': True
                        },
                    'rating': {
                        'type':'number',
                        'min':0,
                        'max':100,
                        'nullable': True,
                        },
                    'language': {
                        'type':'string',
                        'minlength':2,
                        'maxlength':2,
                        'allowed': list(LANGUAGES.keys()),
                        'required':True
                        },
                    'genres' : {
                        'type':'list',
                        'maxlength':20,
                        'schema': {
                            'type':'string',
                            'minlength':1,
                            'maxlength':64,
                            },
                        },
                    'sources': {
                        'type':'list',
                        'schema': source,
                        'maxlength':100
                        }
            }
        }

authors={
         'datasource': {
         'source':'ebooks',
         'aggregation': {
            'pipeline':[{'$project':{'authors':True, '_id':False}},{'$unwind':'$authors'}, {'$group':{'_id':'$authors','count':{'$sum':1}}}, {'$sort':{'_id.lastname':1,'_id.first_name':1}},  {'$project':{'_id':0, 'count':1, 'lastname':'$_id.lastname', 'firstname':'$_id.firstname'}}]
        }
    }
    }

series={
        'datasource': {
            'source':'ebooks',
            'aggregation': {
                'pipeline': [{'$project':{'series':1, 'authors':1, '_id':0}}, {'$unwind':'$authors'}, {'$group':{'_id':'$series', 'authors':{'$addToSet':'$authors'}}}, {'$project':{'_id':0,'authors':1,'series':'$_id'}}, {'$sort':{'series':1}}]
                }
            }
        }
        
DOMAIN={'ebooks': ebooks,
        'authors': authors,
        'series': series}
