'''
Created on Apr 21, 2016

@author: ivan
'''
import unittest
from server import app,db
import schema
import model
from basecase import TestCase


class Test(TestCase):


    def test_schema_ebook(self):
        
        ebook_data={'title': 'Sedm lumpu slohlo pumpu'}
        errors=schema.ebook_deserializer_insert.validate(ebook_data)
        self.assertFalse(errors)
        errors=schema.ebook_deserializer_insert.validate({})
        self.assertTrue(errors)
        
        
        ebook_data={'title':'Povidky o nicem', 'language':'cs', 
                    'rating':100,
                    'authors':[{'first_name':'Jan', 'last_name': 'Kan'}],
                    'series':{'id':5, 'title':'Za co'},
                    'series_index':1,
                    'genres':[{'id':1, 'name':'Fantasy'}, {'id':2,'name':'Story'}],
                    'version_id':1
                    }
        errors=schema.ebook_deserializer_update.validate(ebook_data)
        print (errors)
        self.assertFalse(errors)
        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()