from unittest.mock import Mock
import shutil
import os.path
import asyncio
from app.tests.basecase import TestCase
from engine import dal
from settings import Testing
from settings import BOOKS_CONVERTED_DIR, BOOKS_BASE_DIR
from engine.tasks import ConvertTask, ConvertManyTask
import app.model as model

dal.DSN = 'dbname={db} user={user} password={password} host={host}'.format(db=Testing.DB_NAME,
                                                                           host=Testing.DB_HOST,
                                                                           user=Testing.DB_USER,
                                                                           password=Testing.DB_PASSWORD
                                                                           )

ebook_file=os.path.join(BOOKS_BASE_DIR, 'Kissinger, Henry/Roky v Bilem dome/Kissinger, Henry - Roky v Bilem dome (1).docx')

class TestConversion(TestCase):

    def setUp(self):
        TestCase.setUp(self)
        dal.init()
        os.makedirs(os.path.dirname(ebook_file), exist_ok=True)
        shutil.copy(os.path.join(os.path.dirname(__file__), 'files/Kissinger, Henry - Roky v Bilem dome (1).docx'), ebook_file)
        
       
    def tearDown(self):
        TestCase.tearDown(self)
        dal.close()
        shutil.rmtree(os.path.join(BOOKS_CONVERTED_DIR, '1/Kissinger, Henry'), ignore_errors=True)
        shutil.rmtree(os.path.join(BOOKS_BASE_DIR, 'Kissinger, Henry'), ignore_errors=True)
        
    
    def test_convert(self):
        
       
        t = ConvertTask(user='admin@example.com')
        loop = asyncio.get_event_loop()
        
        book = '1/Kissinger, Henry/Roky v Bilem dome/Kissinger, Henry - Roky v Bilem dome (1).epub'
        conv_id = loop.run_until_complete(t.run(86063, 'epub'))
        self.assertTrue(os.path.exists(os.path.join(BOOKS_CONVERTED_DIR, book)))
        
        c = model.Conversion.query.get(conv_id)
        self.assertEqual(c.location, book )
        self.assertEqual(c.created_by.user_name, 'admin')
        
        
    def test_multi(self):
        t = ConvertManyTask(user='admin@example.com')
        loop = asyncio.get_event_loop()
        run= loop.run_until_complete
        run(t.start('author', 8015, 'epub'))
        
        self.assertEqual(len(t.tasks)+len(t.ready_sources), 4)
        self.assertEqual(len(t.tasks),4)
        self.assertEqual(t.tasks, ['convert']*4)
        tasks=[72201, 73674, 74027, 74100]
        self.assertEqual(list(map(lambda x: x[0][0], t.tasks_args)), tasks)
        
        
        for i in range(4):
            st = run(t.next_task())
            self.assertEqual(st.task_args[0], tasks[i])
            self.assertEqual(st.task_args[1], 'epub')
            
        st = run(t.next_task())
        self.assertTrue(st is None)
        
        
        
        
