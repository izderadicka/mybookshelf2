import shutil
import os.path
import asyncio
from app.tests.basecase import TestCase
from engine import dal
from settings import Testing
from settings import BOOKS_CONVERTED_DIR, BOOKS_BASE_DIR, UPLOAD_DIR, THUMBS_DIR
from engine.tasks import CoverTask
import app.model as model
import tempfile

dal.DSN = 'dbname={db} user={user} password={password} host={host}'.format(db=Testing.DB_NAME,
                                                                           host=Testing.DB_HOST,
                                                                           user=Testing.DB_USER,
                                                                           password=Testing.DB_PASSWORD
                                                                           )

cover_file=os.path.join(os.path.dirname(__file__), 'files/cover.jpg')
ebook_cover_file=os.path.join(BOOKS_BASE_DIR, 'Kissinger Henry/Roky v Bilem dome(cs)/cover.jpg')


class TestMeta(TestCase):

    def setUp(self):
        TestCase.setUp(self)
        dal.init()
        self.tmp_dir=tempfile.mkdtemp(dir=UPLOAD_DIR)
        self.tmp_file_full=os.path.join(self.tmp_dir, 'cover_in.jpg')
        self.tmp_file = os.path.join(os.path.basename(self.tmp_dir), 'cover_in.jpg')
        shutil.copy(cover_file, self.tmp_file_full)
        
       
    def tearDown(self):
        TestCase.tearDown(self)
        dal.close()
        shutil.rmtree(self.tmp_dir, ignore_errors=True)
        try:
            os.remove(os.path.join(THUMBS_DIR, '%d.jpg'%61944))
        except IOError:
            pass
        
    def test_cover(self):
        t = CoverTask(user='admin@example.com')
        loop = asyncio.get_event_loop()
        
        book_id = loop.run_until_complete(t.run(self.tmp_file, 61944))
        self.assertEqual(book_id, 61944)
        self.assertTrue(os.path.exists(ebook_cover_file))
        self.assertTrue(os.path.exists(os.path.join(THUMBS_DIR, '%d.jpg'%61944)))
        
        