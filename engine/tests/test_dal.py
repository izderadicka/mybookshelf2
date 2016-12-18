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
        insert = dal.add_conversion(fname='converted.epub', format='epub', source_id=43290, user_email='admin@example.com')
        new_id =  loop.run_until_complete(insert)
        self.assertEqual(new_id, 1)
        
        conv = model.Conversion.query.get(new_id)
        self.assertEqual(conv.format.extension, 'epub')
        
        #-------

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
        
# -----------------------------------
        
        q = dal.get_source_file(1)
        source, format = loop.run_until_complete(q)
        self.assertEqual((source, format), (None,None))
        
        q = dal.get_source_file(42448)
        source, format = loop.run_until_complete(q)
        self.assertEqual((source, format), ('Crichton, Michael/Let cislo TPA 545/Crichton, Michael - Let cislo TPA 545.doc','doc'))
        
        q = dal.get_meta(43290)
        meta = loop.run_until_complete(q)
        self.assertEqual(meta['title'], 'Legenda')
        self.assertEqual(meta['authors'], 'David Gemmell')
        self.assertEqual(meta['language'], 'cs')
        self.assertEqual(meta['series'], 'Drenajská sága')
        self.assertEqual(meta['series-index'], 1)
        self.assertEqual(meta['tags'], 'Fantasy')
        
        q = dal.get_conversion_id(2, 1, 'epub')
        conv_id = loop.run_until_complete(q)
        self.assertTrue(conv_id is None)
        q = dal.get_ebook_dir(61944)
        base_dir = loop.run_until_complete(q)
        self. assertEqual(base_dir, 'Kissinger Henry/Roky v Bilem dome(cs)')
        q =dal.update_ebook_cover(61944, 'Kissinger Henry/Roky v Bilem dome(cs)/cover.jpg')
        loop.run_until_complete(q)
        
        eb = model.Ebook.query.get(61944)
        self.assertEqual(eb.cover, 'Kissinger Henry/Roky v Bilem dome(cs)/cover.jpg')
        
        shelf = model.Bookshelf(name='Testovaci')
        db.session.add(shelf)
        db.session.commit()
        
        q = dal.get_ebooks_ids_for_object('author', 8015 )
        ebooks_ids = loop.run_until_complete(q)
        self.assertEqual(len(ebooks_ids), 4)
        
        q = dal.get_ebooks_ids_for_object('series', 1633 )
        ebooks_ids = loop.run_until_complete(q)
        self.assertEqual(len(ebooks_ids), 4)
        
        q = dal.get_ebooks_ids_for_object('bookshelf', 1 )
        ebooks_ids = loop.run_until_complete(q)
        self.assertEqual(len(ebooks_ids), 0)
        
        q = dal.get_conversion_candidate(58694, 'epub')
        res = loop.run_until_complete(q)
        self.assertEqual(res, (54463, 'epub')) 
        
        q = dal.get_conversion_candidate(58694, 'mobi')
        res = loop.run_until_complete(q)
        self.assertEqual(res, (54463, 'epub')) 
        
        
        for entity_name, entity_id, name in (('author', 8015, 'Jason Dark'), 
                                       ('series', 1633, 'Na stopě hrůzy'), 
                                       ('bookshelf', 1, 'Testovaci')):
            q = dal.create_conversion_batch(entity_name, entity_id, 'epub', 1)
            batch_id = loop.run_until_complete(q)
            self.assertTrue(batch_id)
            
            batch = model.ConversionBatch.query.get(batch_id)
            self.assertTrue(batch.name.find(name) >=0, 'Contains %s'%name)
            
            q = dal.get_conversion_batch(entity_name, entity_id, 'epub', 1)
            rb_id = loop.run_until_complete(q)
            self.assertEqual(rb_id, batch_id)
            
        q = dal.add_zip_to_batch(batch_id, '1/mybatch.zip')
        loop.run_until_complete(q)
        db.session.expire(batch)
        batch = model.ConversionBatch.query.get(batch_id)
        self.assertEqual(batch.zip_location, '1/mybatch.zip')
        
        q = dal.get_existing_conversion(58694, 1, 'epub')
        conv_id = loop.run_until_complete(q)
        self.assertTrue(conv_id is None)
        
        
