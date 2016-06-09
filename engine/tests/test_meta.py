import unittest
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
        t = MetadataTask()
        loop = asyncio.get_event_loop()
        res = loop.run_until_complete(t.run(self.fname))
        self.assertTrue(res)
        print (res)
        
        self.assertEqual(res['metadata']['authors'], ['Douglas Adams'])
        self.assertEqual(res['metadata']['title'], 'Stopařův průvodce po Galaxii')
        self.assertEqual(res['metadata']['tags'], ['Fantasy', 'Humor', 'Sci-fi'])
        self.assertTrue(res['cover'])
        os.remove(os.path.join(UPLOAD_DIR, res['cover']))
        
        
