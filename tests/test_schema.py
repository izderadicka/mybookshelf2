'''
Created on Apr 21, 2016

@author: ivan
'''
import unittest
from server import app,db
import schema


class Test(unittest.TestCase):


    def setUp(self):
        self.ctx=None


    def tearDown(self):
        pass


    def test_schema_ebook(self):
        
        ebook_data={'title': 'Sedm lumpu slohlo pumpu'}
        errors=schema.EbookSchema().validate(ebook_data, db.session)
        self.assertTrue(not errors)
        errors=schema.EbookSchema().validate({}, db.session)
        self.assertTrue(errors)
        print (errors)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()