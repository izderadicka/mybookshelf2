import unittest
import asyncio
import engine.dal as dal
from settings import Testing

from app.tests.basecase import TestCase
import app.model as model

dal.DSN = 'dbname={db} user={user} password={password} host={host}'.format(db=Testing.DB_NAME,
                                                                           host=Testing.DB_HOST,
                                                                           user=Testing.DB_USER,
                                                                           password=Testing.DB_PASSWORD
                                                                           )


class TestDAL(TestCase):

    def test_dal1(self):
        from app.model import Format
        dal.init()
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
        dal.close()

        upload = model.Upload.query.get(new_id)

        self.assertEqual(upload.created_by.email, 'admin@example.com')

        self.assertEqual(upload.meta['title'], 'Stoparuv pruvodce')
