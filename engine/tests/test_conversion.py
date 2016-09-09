from unittest.mock import Mock
import shutil
import os.path
import asyncio
from app.tests.basecase import TestCase
from engine import dal
from settings import Testing
from settings import BOOKS_CONVERTED_DIR
from engine.tasks import ConvertTask
import app.model as model

dal.DSN = 'dbname={db} user={user} password={password} host={host}'.format(db=Testing.DB_NAME,
                                                                           host=Testing.DB_HOST,
                                                                           user=Testing.DB_USER,
                                                                           password=Testing.DB_PASSWORD
                                                                           )

class TestMeta(TestCase):

    def setUp(self):
        TestCase.setUp(self)
        dal.init()
        
       
    def tearDown(self):
        TestCase.tearDown(self)
        dal.close()
        shutil.rmtree(os.path.join(BOOKS_CONVERTED_DIR, '1/Kissinger, Henry'), ignore_errors=True)
        
    
    def test_convert(self):
        
       
        t = ConvertTask(user='admin@example.com')
        loop = asyncio.get_event_loop()
        
        book = '1/Kissinger, Henry/Roky v Bilem dome/Kissinger, Henry - Roky v Bilem dome (1).epub'
        conv_id = loop.run_until_complete(t.run(86063, 'epub'))
        self.assertTrue(os.path.exists(os.path.join(BOOKS_CONVERTED_DIR, book)))
        
        c = model.Conversion.query.get(conv_id)
        self.assertEqual(c.location, book )
        self.assertEqual(c.created_by.user_name, 'admin')
        
        
        
