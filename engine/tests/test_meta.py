import unittest
from unittest.mock import Mock
import engine.dal as dal
import shutil
import os.path
import asyncio

from settings import UPLOAD_DIR
from engine.tasks import MetadataTask


class TestMeta(unittest.TestCase):

    def setUp(self):
        fname = os.path.join(os.path.dirname(__file__),
                             '../../app/data/books/Adams, Douglas/Stoparuv pruvodce/Stoparuv pruvodce 1 - Stoparuv pruvodce po Galaxii/Adams, Douglas - Stoparuv pruvodce 1 - Stoparuv pruvodce po Galaxii.epub'
                             )
        shutil.copy(fname, UPLOAD_DIR)
        self.fname = os.path.split(fname)[1]

    def tearDown(self):
        try:
            os.remove(os.path.join(UPLOAD_DIR, self.fname))
        except IOError:
            pass

    def test_meta1(self):
        result=[]
        upload = Mock(side_effect=lambda *args: result.extend(args) or 1)
        async def dummy(*args, **kwargs):
            return upload(*args, **kwargs)
        dal.add_upload = dummy
        
        t = MetadataTask(user='ivan')
        loop = asyncio.get_event_loop()
        res = loop.run_until_complete(t.run(self.fname))
        self.assertEqual(res, 1)
        
        
        meta = result[2]
        self.assertEqual(meta['authors'], ['Douglas Adams'])
        self.assertEqual(meta['title'], 'Stopařův průvodce po Galaxii')
        self.assertEqual(meta['tags'], ['Fantasy', 'Humor', 'Sci-fi'])
        self.assertEqual(result[3], 200134)
        self.assertEqual(result[4], 'f75a07f5ad1da3a27035742eb978868b1a912a1a')
        self.assertEqual(result[5], 'ivan')
        cover = result[1]
        self.assertTrue(cover)
        os.remove(os.path.join(UPLOAD_DIR, cover))
        
        
