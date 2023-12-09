from .basecase import TestCase
from urllib.parse import quote
import flask
from flask_login import current_user
from common.utils import verify_token
import app
import settings
import os.path
import shutil
import json
import time

test_file = os.path.join(os.path.dirname(__file__),
                         'data/Kissinger, Henry - Roky v Bilem dome.epub')
ebook_file = os.path.join(
    settings.BOOKS_BASE_DIR, 'Kissinger, Henry/Roky v Bilem dome/Kissinger, Henry - Roky v Bilem dome.epub')


class TestApi(TestCase):

    def __init__(self, *args, **kwargs):
        super(TestApi, self).__init__(*args, **kwargs)
        self.headers = {}
        self.token = None

    def setUp(self):
        TestCase.setUp(self)
        os.makedirs(os.path.dirname(ebook_file), exist_ok=True)
        shutil.copy(test_file, ebook_file)

    def tearDown(self):
        TestCase.tearDown(self)
        shutil.rmtree(
            os.path.join(settings.BOOKS_BASE_DIR, 'Kissinger, Henry'), ignore_errors=True)

    def login(self, user='admin', pwd='admin'):
        res = self.client.post('/login', data='{"username":"%s", "password":"%s"}' % (user, pwd),
                               content_type='application/json')
        token = res.json.get('access_token')
        self.assertTrue(token)
        refresh = res.json.get('refresh_token')
        self.assertTrue(refresh)
        self.headers = {'Authorization': 'Bearer %s' % token}
        self.token = token

    def __getattr__(self, name):
        name = name.upper()
        if name in ('GET', 'POST', 'DELETE', 'PUT', 'OPTIONS', 'PATCH'):
            def req(*args, **kwargs):
                kwargs['method'] = name
                if 'headers' in kwargs:
                    kwargs['headers'].update(self.headers)
                else:
                    kwargs['headers'] = self.headers
                failure = kwargs.pop('failure', False)
                not_json = kwargs.pop('not_json', False)
                resp = self.client.open(*args, **kwargs)
                if not failure:
                    self.assert200(resp)
                if not not_json and not failure:
                    return resp.json
                return resp
            return req
        raise AttributeError('Attribute %s not found' % name)
    
    def test_login(self):
        res = self.post('/login', data='{"username":"%s", "password":"%s"}' % ('admin', 'admin'),
                               content_type='application/json')
        token = res.get('access_token')
        self.assertTrue(token)
        refresh = res.get('refresh_token')
        self.assertTrue(refresh)
        cfg = flask.current_app.config
        
        l1 = verify_token(token, cfg['SECRET_KEY'])
        self.assertEqual(l1['id'], 1)
        
        l2 = verify_token(refresh, cfg['SECRET_KEY2'])
        self.assertEqual(l1['id'], l2['id'])
        
        # refresh token
        time.sleep(1)
        
        res = self.post('/login', data = json.dumps({'refresh_token':refresh}),
                               content_type='application/json', 
                               headers={'Authorization': 'Bearer %s'%token})
        self.assertTrue(res['access_token'])
        
        new_token = res['access_token']
        l3=verify_token(new_token, cfg['SECRET_KEY'])
        self.assertEqual(l3['user_name'], 'admin')
        
        old_exp = l1['exp']
        new_exp = l3['exp']
        
        self.assertTrue(int(old_exp) < int(new_exp))
        
        
        
    def test_api(self):
        res = self.get('/api/ebooks', failure=True)
        self.assert401(res)
        self.login()
        res = self.get('/api/ebooks')

        self.assertTrue(len(res['items']) > 5)
        self.assertEqual(res['page'], 1)
        # current user is anonymous outside of request
        self.assertFalse(current_user.is_authenticated)

        for b in res['items']:
            self.assertTrue(b['title'] and b['id'], 'Invalid ebook %s' % b)

        res = self.get(
            '/api/ebooks', query_string={'page': 1, 'page_size': 12, 'sort': 'title'})
        self.assertEqual(res['page'], 1)
        self.assertEqual(res['total'], 100)
        self.assertEqual(res['page_size'], 12)
        self.assertEqual(len(res['items']), 12)
        self.assertEqual(
            res['items'][0]['title'], 'Alenka v říši kvant - Alegorie kvantové fyziky')

        first_book = res['items'][0]

        res = self.get(
            '/api/ebooks', query_string={'page': 9, 'page_size': 12, 'sort': '-title'})
        self.assertEqual(res['page'], 9)
        self.assertEqual(len(res['items']), 4)
        self.assertEqual(res['total'], 100)
        self.assertEqual(res['page_size'], 12)
        self.assertEqual(
            res['items'][-1]['title'], 'Alenka v říši kvant - Alegorie kvantové fyziky')
        last_book = res['items'][-1]

        self.assertEqual(first_book, last_book)

        res = self.get(
            '/api/ebooks', query_string={'page': 9, 'page_size': 12, 'sort': 'blba'}, failure=True)
        self.assert400(res)

        res = self.get(
            '/api/ebooks', query_string={'page': 0, 'page_size': 12, 'sort': '-title'}, failure=True)
        self.assert400(res)

        res = self.get(
            '/api/ebooks', query_string={'page': 1, 'page_size': -1, 'sort': '-title'},  failure=True)
        self.assert400(res)

        res = self.get(
            '/api/ebooks', query_string={'page': 1, 'page_size': 101, 'sort': '-title'},  failure=True)
        self.assert400(res)

        res = self.get(
            '/api/ebooks', query_string={'page': 10, 'page_size': 12, 'sort': 'title'},  failure=True)
        self.assert404(res)

        id = first_book['id']

        res = self.get('/api/ebooks/%s' % id)
        self.assertEqual(res['id'], id)
        self.assertEqual(
            res['title'], 'Alenka v říši kvant - Alegorie kvantové fyziky')

        #------------
        res = self.get(
            '/api/authors', query_string={'page': 1, 'page_size': 50, 'sort': 'name'})
        self.assertEqual(len(res['items']), 50)
        self.assertEqual(res['total'], 103)
        self.assertEqual(res['items'][0]['last_name'], 'Adams')

        res = self.get(
            '/api/series', query_string={'page': 2, 'page_size': 14, 'sort': 'title'})
        self.assertEqual(res['total'], 28)
        self.assertEqual(res['items'][-1]['title'], 'Zář')

        res = self.get('/api/search/%s' % quote('Zápas boh'))
        self.assertEqual(res['total'], 1)
        self.assertEqual(res['items'][0]['title'], 'Podobni bohům')

        res = self.get('/api/search/%s' % quote('prip'))
        self.assertEqual(res['total'], 4)

        res = self.get('/api/search/%s' % quote('henry dome'))
        self.assertEqual(res['total'], 1)
        self.assertEqual(res['items'][0]['title'], 'Roky v Bílém domě')

        res = self.get('/api/ebooks/author/8015')
        self.assertEqual(res['total'], 4)
        self.assertEqual(len(res['items']), 4)

        res = self.get('/api/ebooks?genres=9,16')
        self.assertEqual(res['total'], 2)

        res = self.get('/api/genres')
        self.assertEqual(len(res), 57)

        res = self.get('/api/languages')
        self.assertEqual(len(res), 4)

    def test_api2(self):
        #---------------
        self.login('guest', 'guest')
        res = self.get('/api/ebooks', failure=True)
        self.assert401(res)

        self.login('user', 'user')
        res = self.get('/api/ebooks')

        id = 62241
        res = self.delete('/api/ebooks/%d' % id, failure=True)
        self.assert403(res)

        self.login('superuser', 'superuser')

        res = self.get('/api/ebooks/%s' % id)
        self.assertEqual(len(res['sources']), 1)
        source_id = res['sources'][0]['id']
        res = self.post('/api/sources/%d/move' % source_id,
                        data='{"other_ebook_id":50118}', content_type='application/json')
        res = self.get('/api/ebooks/%s' % id)
        self.assertEqual(len(res['sources']), 0)

        res = self.delete('/api/ebooks/%d' % id)

        res = self.get('/api/ebooks/%s' % id, failure=True)
        print (res.json)
        self.assert404(res)

        res = self.get(
            '/api/download/86060', query_string={'bearer_token': self.token}, not_json=True)
        self.assertEqual(int(res.headers['Content-Length']), 3147900)
        self.assertEqual(res.headers['Content-Type'], 'application/epub+zip')
        self.assertEqual(len(res.data), 3147900)

        res = self.post('/api/upload/check', data='{"mime_type":"application/pdf", "size":10000, "hash":null}',
                        content_type='application/json')
        self.assertEqual(res['result'], 'ok')

        # indexes
        res = self.get('/api/series/index/a')
        self.assertEqual(res['total'], 3)
        self.assertEqual(len(res['items'][0]['authors']), 1)
        print(res)
        res = self.get('/api/series/index/na')
        self.assertEqual(res['total'], 1)
        self.assertEqual(len(res['items'][0]['authors']), 2)

        res = self.get('/api/series/index/á')
        self.assertEqual(res['total'], 3)
        res = self.get('/api/authors/index/c')
        self.assertEqual(res['total'], 4)
        res = self.get('/api/authors/index/č')
        self.assertEqual(res['total'], 4)

        res = self.get('/api/ebooks/index/r')
        self.assertEqual(res['total'], 1)

        res = self.get('/api/ebooks/series/1633')
        self.assertEqual(res['total'], 4)

    def test_merge(self):
        self.login()

        res = self.post('/api/ebooks/%d/merge' % 33837, data='{"other_id":37157}',
                        content_type='application/json')
        self.assertTrue(res['id'])

        res = self.get('/api/authors/index/c')
        a1_id = res['items'][0]['id']
        a2_id = res['items'][1]['id']
        a3_id = res['items'][2]['id']

        res = self.get('/api/ebooks/author/%d' % a1_id)
        num_books1 = res['total']

        res = self.get('/api/ebooks/author/%d' % a2_id)
        num_books2 = res['total']

        self.assertEqual((num_books1, num_books2), (1, 1))

        res = self.post('/api/authors/%d/merge' % a1_id, data='{"other_id":%d}' % a2_id,
                        content_type='application/json')
        self.assertTrue(res['id'])
        res = self.get('/api/ebooks/author/%d' % a1_id)
        self.assertEqual(res['total'], 2)

        res = self.post('/api/authors/%d/merge' % a3_id, data='{"other_id":%d}' % a1_id,
                        content_type='application/json')
        self.assertTrue(res['id'])
        res = self.get('/api/ebooks/author/%d' % a3_id)
        self.assertEqual(res['total'], 3)
        
        series = self.get('/api/series', query_string={'page': 1, 'page_size': 12, 'sort': 'title'})['items']
        s1 = series[0]
        s2 = series[-1]
        self.assertEqual(self.get('api/ebooks/series/%d'%s1['id'])['total'], 1)
        self.assertEqual(self.get('api/ebooks/series/%d'%s2['id'])['total'], 4)
        
        res = self.post('/api/series/%d/merge'%s1['id'], data='{"other_id":%d}' % s2['id'],
                        content_type='application/json')
        
        self.assertTrue(res['id'])
        self.assertEqual(self.get('api/ebooks/series/%d'%s1['id'])['total'], 5)
        res = self.get('/api/series/%d'% s2['id'], failure=True)
        self.assert404(res)
        
        
    def test_api_create_edit(self):
        self.login()
        data = '{"title":"Testovací kniha","authors":[{"id":5222},{"last_name":"Novy","first_name":"Autor"}, {"last_name":"Novy","first_name":"Autor"}],"genres":[{"id":43}],"language":{"id":1},"series":{"title":"Nejaka"},"series_index":"1"}'
        res = self.post(
            '/api/ebooks', data=data, content_type="application/json")

        if res.get('error'):
            print(res.get('error_details'))
            self.fail('Ebook create error: %s' % res['error'])

        id = res['id']

        self.assertTrue(id > 0)

        ebook = self.get('/api/ebooks/%d' % id)

        self.assertEqual(ebook['title'], "Testovací kniha")
        self.assertEqual(len(ebook['authors']), 2)
        self.assertEqual(ebook['series_index'], 1)
        self.assertEqual(ebook['series']['title'], 'Nejaka')

        ser = self.get('/api/series/%d' % ebook['series']['id'])
        self.assertEqual(ser['created_by'], 1)
        self.assertEqual(ser['modified_by'], 1)

        ser_id = ebook['series']['id']

        def has_obj(l, attr, value):
            for o in l:
                if o.get(attr) == value:
                    return True

        self.assertTrue(has_obj(ebook['authors'], 'last_name', 'King'))
        self.assertTrue(has_obj(ebook['authors'], 'last_name', 'Novy'))
        self.assertTrue(has_obj(ebook['genres'], 'name', 'Espionage'))

        self.assertEqual(ebook['created_by'], 1)
        self.assertEqual(ebook['modified_by'], 1)

        res = self.patch('/api/ebooks/%d' % id, data='{"series":{"title": "Jinaci"}, "version_id":1}',
                         content_type='application/json')
        res = self.get('/api/ebooks/%d' % id)
        new_ser_id = res['series']['id']
        self.assertNotEqual(ser_id, new_ser_id)

        res = self.patch('/api/ebooks/%d' % id, data='{"series":{"title": "Nejaka"}, "version_id":2}',
                         content_type='application/json')
        res = self.get('/api/ebooks/%d' % id)
        self.assertEqual(ser_id, res['series']['id'])

        res = self.patch('/api/ebooks/%d' % id, data='{"authors":[{"last_name": "James", "first_name": "Peter"}], "version_id":3}',
                         content_type='application/json')
        res = self.get('/api/ebooks/%d' % id)
        self.assertEqual(res['authors'][0]['id'], 5185)
        self.assertEqual(len(res['authors']), 1)

        res = self.patch('/api/ebooks/35485', data='{"title": "Prokleta vesnice", "version_id":1}',
                         content_type="application/json")
        if res.get('error'):
            print(res.get('error'), res.get('error_details'))
        self.assertFalse(res.get('error'))
        self.assertTrue(res.get('success'))
        print(res)

        res = self.get('/api/ebooks/35485')
        self.assertEqual(res['title'], 'Prokleta vesnice')
        self.assertEqual(res['version_id'], 2)
        # rating

        def rate(x):
            res = self.post('/api/ebooks/35485/rate', data=json.dumps({'rating': x}),
                            content_type="application/json")
            self.assertEqual(res['id'], 35485)

        def get_rating():
            res = self.get('/api/ebooks/35485')
            return res['rating'], res['rating_count']
        rate(100)
        self.assertEqual(get_rating(), (100, 1))
        rate(50)
        self.assertEqual(get_rating(), (50, 1))

        self.login('user', 'user')
        rate(20)
        self.assertEqual(get_rating(), (35, 2))
        res = self.get('/api/ebooks/35485')
        self.assertEqual(res['my_rating'], 20)
        rate(None)
        self.assertEqual(get_rating(), (50, 1))

    def test_bookshelfs(self):
        res = self.post(
            '/api/bookshelves/mine', data='{"name":"test", "description":"bla bla"}',
            content_type="application/json", failure=True)
        self.assert401(res)
        self.login()
        res = self.post(
            '/api/bookshelves/mine', data='{"name":"test", "description":"bla bla"}',
            content_type="application/json")

        if res.get('error'):
            print(res.get('error_details'))
            self.fail('Ebook create error: %s' % res['error'])

        shelf_id = res['id']
        self.assertEqual(shelf_id, 1)

        res = self.get('/api/bookshelves/mine')

        self.assertEqual(res['total'], 1)
        self.assertEqual(res['items'][0]['items_count'], 0)

        ebooks = self.get(
            '/api/ebooks', query_string={'page': 1, 'page_size': 10})['items']

        ebook_id = ebooks[4]['id']

        self.assertEqual(len(ebooks), 10)

        for b in ebooks:
            self.post('/api/bookshelves/%d/add' % shelf_id, data='{"ebook":{"id":%d}, "note":"test"}' % b['id'],
                      content_type="application/json")

        shelf = self.get('/api/bookshelves/%d' % shelf_id)
        self.assertEqual(shelf['items_count'], 10)

        res = self.get('/api/bookshelves/mine/index/t')
        self.assertEqual(res['total'], 1)

        items = self.get(
            '/api/bookshelves/1/items', query_string={'page': 1, 'page_size': 10})
        self.assertEqual(items['total'], 10)

        for i in items['items']:
            print(i)
            self.assertEqual(i.get('note'), 'test')
            self.assertTrue(i['ebook']['title'])

        res = self.delete('/api/bookshelf-items/%d' % 1)
        self.assertEqual(res['id'], 1)

        items = self.get(
            '/api/bookshelves/1/items', query_string={'page': 1, 'page_size': 10})
        self.assertEqual(items['total'], 9)

        res = self.post('/api/bookshelves/%d/add' % shelf_id, data='{"series":{"id":%d}, "note":"test"}' % 1633,
                        content_type="application/json")

        self.assertEqual(res['id'], 1)

        items = self.get('/api/bookshelves/1/items',
                         query_string={'page': 1, 'page_size': 10, 'sort': '-created'})
        self.assertEqual(items['total'], 10)

        items = items['items']
        self.assertEqual(items[0]['series']['id'], 1633)
        self.assertEqual(items[0]['series']['title'], 'Na stopě hrůzy')

        res = self.get('/api/bookshelves/mine')
        self.assertEqual(res['total'], 1)
        self.assertEqual(res['items'][0]['items_count'], 10)

        res = self.get('/api/bookshelves/others')
        self.assertEqual(res['total'], 0)

        print('Shelves with ebook %d' % ebook_id)
        res = self.get('/api/bookshelves/with-ebook/%d' % ebook_id)
        self.assertEqual(res['total'], 1)

        res = self.post(
            '/api/bookshelves/mine', data='{"name":"test2", "description":"temp"}',
            content_type="application/json")

        bs2_id = res['id']
        ebooks = self.get(
            '/api/ebooks', query_string={'page': 3, 'page_size': 10})['items']
        for b in ebooks:
            self.post('/api/bookshelves/%d/add' % bs2_id, data='{"ebook":{"id":%d}, "note":"test2"}' % b['id'],
                      content_type="application/json")

        self.post('/api/bookshelves/%d/add' % bs2_id, data='{"ebook":{"id":%d}, "note":"test2"}' % ebook_id,
                  content_type="application/json")
        items = self.get('/api/bookshelves/%d/items' %
                         bs2_id, query_string={'page': 1, 'page_size': 10})
        self.assertEqual(items['total'], 11)
        res = self.post('/api/bookshelves/1/merge', data=json.dumps({'other_id': bs2_id}),
                        content_type="application/json")

        items = self.get(
            '/api/bookshelves/1/items', query_string={'page': 1, 'page_size': 10})
        self.assertEqual(items['total'], 20)
