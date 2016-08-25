import unittest
import asyncio
import engine.dal as dal
from settings import Testing

from app.tests.basecase import TestCase
from app import db
import app.model as model

dal.DSN = 'dbname={db} user={user} password={password} host={host}'.format(db=Testing.DB_NAME,
                                                                           host=Testing.DB_HOST,
                                                                           user=Testing.DB_USER,
                                                                           password=Testing.DB_PASSWORD
                                                                           )


class TestDAL(TestCase):

    def setUp(self):
        TestCase.setUp(self)
        dal.init()

    def tearDown(self):
        TestCase.tearDown(self)
        dal.close()
        db.session.close()

    def test_dal1(self):
        from app.model import Format
        assert dal.engine
        fmt_table = Format.__table__
        formats = []
        async def do():
            async with dal.engine.acquire() as conn:
                async for row in conn.execute(fmt_table.select(fmt_table)):
                    formats.append(row.mime_type)

        loop = asyncio.get_event_loop()
        loop.run_until_complete(do())
        self.assertEqual(len(formats), 17)
        self.assertTrue('application/x-aportisdoc' in formats)

        # ----
        insert = dal.add_upload(fname='ebook.epub', cover='cover.jpg', meta={'authors': ['Douglas Adams'],
                                                                             'title': 'Stoparuv pruvodce'}, size=1233455,
                                hash='12345678901234567890123456789010',
                                user_email='admin@example.com')

        new_id = loop.run_until_complete(insert)
        self.assertEqual(new_id, 1)

        upload = model.Upload.query.get(new_id)

        self.assertEqual(upload.created_by.email, 'admin@example.com')

        self.assertEqual(upload.meta['title'], 'Stoparuv pruvodce')

        # -------

        q = dal.find_series({'title': 'Nekroskop'})
        series = loop.run_until_complete(q)
        self.assertEqual(series['id'], 587)
        self.assertEqual(series['title'], 'Nekroskop')
        q = dal.find_series({'title': 'Neexistuje'})
        series = loop.run_until_complete(q)
        self.assertTrue(series is None)

        q = dal.find_author({'first_name': 'Jules', 'last_name': 'Verne'})
        author = loop.run_until_complete(q)
        self.assertEqual(author['id'], 5521)
        self.assertEqual(author['first_name'], 'Jules')
        self.assertEqual(author['last_name'], 'Verne')
        q = dal.find_author({'first_name': 'Jan', 'last_name': 'Nabouhanec'})
        author = loop.run_until_complete(q)
        self.assertTrue(author is None)

        new_author = model.Author(last_name="Kulisak")
        db.session.add(new_author)
        db.session.commit()

        q = dal.find_author({'last_name': 'Kulisak'})
        author = loop.run_until_complete(q)
        self.assertEqual(author['id'], new_author.id)
        self.assertEqual(author['last_name'], 'Kulisak')
        self.assertFalse('first_name' in author)

        q = dal.find_language({'code': 'en'})
        lang = loop.run_until_complete(q)
        self.assertEqual(lang['name'], 'English')
        self.assertEqual(lang['code'], 'en')
        self.assertEqual(lang['id'], 2)

        q = dal.find_language({'code': 'eng'})
        lang = loop.run_until_complete(q)
        self.assertEqual(lang['name'], 'English')
        self.assertEqual(lang['code'], 'en')
        self.assertEqual(lang['id'], 2)
        
        q = dal.find_language({'code': 'ces'})
        lang = loop.run_until_complete(q)
        self.assertEqual(lang['name'], 'Czech')
        self.assertEqual(lang['code'], 'cs')
        self.assertEqual(lang['id'], 1)

        q = dal.find_language({'code': 'enh'})
        lang = loop.run_until_complete(q)
        self.assertTrue(lang is None)

        q = dal.find_genre({'name': "science fiction"})
        genre = loop.run_until_complete(q)
        self.assertEqual(genre['name'], 'Science Fiction')
        self.assertEqual(genre['id'], 25)

        q = dal.find_genre({'name': "sci-fi"})
        genre = loop.run_until_complete(q)
        self.assertEqual(genre['name'], 'Science Fiction')
        self.assertEqual(genre['id'], 25)

        q = dal.find_genre({'name': "Kulisarna"})
        genre = loop.run_until_complete(q)
        self.assertTrue(genre is None)
