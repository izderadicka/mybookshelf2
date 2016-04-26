'''
Created on Apr 21, 2016

@author: ivan
'''
import unittest
from app import app,db
import app.schema as schema
import app.model as model
from .basecase import TestCase

#app.config['SQLALCHEMY_ECHO']=True
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
                    'genres':[ {'id':23,'name':'Romance'}, {'id':9, 'name':'Fantasy'}, {'id':13, 'name':'Horror'}],
                    'version_id':1
                    }
        eb,errors=schema.ebook_deserializer_update.load(ebook_data)
        print (errors)
        self.assertFalse(errors)
        
        self.assertEqual(eb.title, ebook_data['title'])
        db.session.flush()
        self.assertFalse(db.session.new)
        self.assertFalse(db.session.dirty)
        db.session.add(eb)
        db.session.commit()
        
        self.assertEqual(eb.authors[0].last_name, ebook_data['authors'][0]['last_name'] )
        self.assertEqual(eb.series.title, ebook_data['series']['title'])
        
        db.session.remove()
        
        eb=model.Ebook.query.filter_by(title='Povidky o nicem').one()
        self.assertEqual(eb.authors[0].last_name, ebook_data['authors'][0]['last_name'] )
        self.assertEqual(eb.series.title, ebook_data['series']['title'])
        
        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()