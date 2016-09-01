import unittest
from unittest.mock import Mock
import engine.dal as dal
import shutil
import os.path
import asyncio
from app.tests.basecase import TestCase
from engine import dal
from settings import Testing
from settings import UPLOAD_DIR
from engine.tasks import MetadataTask

dal.DSN = 'dbname={db} user={user} password={password} host={host}'.format(db=Testing.DB_NAME,
                                                                           host=Testing.DB_HOST,
                                                                           user=Testing.DB_USER,
                                                                           password=Testing.DB_PASSWORD
                                                                           )

FILES = ['Adams, Douglas - Stoparuv pruvodce 1 - Stoparuv pruvodce po Galaxii.epub', 
                  'Brown, Eric - Virex 1 - Newyorske noci.epub',
                  'Nix G. - Klice od Kralovstvi 2 - Udesne utery [Triton 2006].doc',
                  'Zweig, Stefan - Netrpelivost srdce.docx']
class TestMeta(TestCase):

    def setUp(self):
        TestCase.setUp(self)
        dal.init()
        self.fname=[]
        for f in FILES:
            fname = os.path.join(os.path.dirname(__file__), 'files', f)
            shutil.copy(fname, UPLOAD_DIR)
            self.fname.append(os.path.split(fname)[1])
       
    def tearDown(self):
        TestCase.tearDown(self)
        dal.close()
        for f in self.fname:
            try:
                os.remove(os.path.join(UPLOAD_DIR, f))
            except IOError:
                pass
            
        try:
            os.remove(os.path.join(UPLOAD_DIR, 'cover.jpg'))
        except IOError:
            pass
        
        try:
            os.remove(os.path.join(UPLOAD_DIR, 'thumbnail.jpg'))
        except IOError:
            pass
    
    def assert_cover(self, cover):
         self.assertEqual(cover, 'cover.jpg')
         self.assertTrue(os.path.exists(os.path.join(UPLOAD_DIR, cover)))
         self.assertTrue(os.stat(os.path.join(UPLOAD_DIR, cover)).st_size > 0)
    
    def test_meta1(self):
        result = []
        upload = Mock(side_effect=lambda *args: result.extend(args) or 1)
        async def dummy(*args, **kwargs):
            return upload(*args, **kwargs)
        dal.add_upload = dummy

        t = MetadataTask(user='ivan')
        loop = asyncio.get_event_loop()
        
        result = []
        res = loop.run_until_complete(t.run(self.fname[2]))
        self.assertEqual(res, 1)
        self.assert_cover(result[1])
        meta = result[2]
        self.assertEqual(meta['title'], 'Nix G. - Klice od Kralovstvi 2 - Udesne utery [Triton 2006]')
        self.assertEqual(len(meta), 1)
        
        result = []
        res = loop.run_until_complete(t.run(self.fname[3]))
        self.assertEqual(res, 1)
        self.assert_cover(result[1])
        meta = result[2]
        self.assertEqual(meta['title'], 'Netrpelivost srdce')
        self.assertEqual(meta['authors'][0], {'first_name':'Stefan', 'last_name':'Zweig'})
        self.assertEqual(
            meta['language'], {'code': 'cs', 'name': 'Czech', 'id': 1})
    
        result = []
        res = loop.run_until_complete(t.run(self.fname[0]))
        self.assertEqual(res, 1)
        self.assert_cover(result[1])
        meta = result[2]
        self.assertEqual(
            meta['authors'], [{'last_name': 'Adams', 'first_name': 'Douglas', 'id': 4879}])
        self.assertEqual(meta['title'], 'Stopařův průvodce po Galaxii')
        self.assertEqual(meta['genres'], [{'id': 9, 'name': 'Fantasy'},
                                          {'id': 14, 'name': 'Humor/Satire'},
                                          {'id': 25, 'name': 'Science Fiction'}])
        self.assertFalse('language' in meta)
        self.assertEqual(result[3], 200134)
        self.assertEqual(result[4], 'f75a07f5ad1da3a27035742eb978868b1a912a1a')
        self.assertEqual(result[5], 'ivan')
        cover = result[1]
        self.assertTrue(cover)
        os.remove(os.path.join(UPLOAD_DIR, cover))

        result = []
        res = loop.run_until_complete(t.run(self.fname[1]))
        self.assertEqual(res, 1)
        self.assert_cover(result[1])
        meta = result[2]

        self.assertEqual(meta['title'], 'Newyorské noci')
        self.assertEqual(
            meta['authors'], [{'first_name': 'Eric', 'last_name': 'Brown'}])
        self.assertEqual(meta['genres'], [
                         {'name': 'Crime/Mystery', 'id': 7, }, {'name': 'Science Fiction', 'id': 25, }])
        self.assertEqual(
            meta['language'], {'code': 'cs', 'name': 'Czech', 'id': 1})
        self.assertEqual(meta['series'], {'title': 'Virex'})
        self.assertEqual(meta['series_index'], 1)
        
        
        
