'''
Created on Apr 21, 2016

@author: ivan
'''
import unittest
from app import app, db
import app.schema as schema
import app.model as model
from .basecase import TestCase
from copy import deepcopy
from time import sleep
from sqlalchemy import inspect

#app.config['SQLALCHEMY_ECHO'] = True


class Test(TestCase):

    def test_schema_ebook(self):

        ebook_data = {
            'title': 'Sedm lumpu slohlo pumpu', 'language': {'id': 1}}
        errors = schema.ebook_deserializer_insert().validate(ebook_data)
        self.assertFalse(errors)
        errors = schema.ebook_deserializer_insert().validate({})
        self.assertTrue(errors)

        ebook_data = {'title': 'Povidky o nicem', 'language': 'cs',
                      'rating': 100,
                      'authors': [{'first_name': 'Jan', 'last_name': 'Kan'}, {'id': 5222}],
                      'series': {'id': 5, 'title': 'Za co'},
                      'series_index': 1,
                      'genres': [{'id': 23}, {'id': 9, 'name': 'Fantasy'}, {'id': 13, 'name': 'Horror'}],
                      "language": {"id": 1},
                      }

        no_lang = deepcopy(ebook_data)
        del no_lang['language']
        errors = schema.ebook_deserializer_insert().validate(no_lang)
        self.assertTrue(errors)

        no_series = deepcopy(ebook_data)
        no_series['series'] = None
        errors = schema.ebook_deserializer_update().validate(no_series)
        if errors:
            print(errors)
        self.assertFalse(errors)

        eb, errors = schema.ebook_deserializer_insert().load(ebook_data)
        self.assertFalse(errors)

        self.assertEqual(eb.title, ebook_data['title'])
        # db.session.flush()
        self.assertFalse(db.session.new)
        # self.assertFalse(db.session.dirty)
        db.session.add(eb)
        self.assertTrue(db.session.new)
        db.session.commit()

        self.assertEqual(len(eb.authors), 2)

        def has_obj(l, attr, value):
            for o in l:
                if getattr(o, attr) == value:
                    return True

        self.assertTrue(has_obj(eb.authors, 'last_name', 'King'))
        self.assertEqual(eb.series.title, ebook_data['series']['title'])

        db.session.remove()

        eb = model.Ebook.query.filter_by(title='Povidky o nicem').one()
        self.assertTrue(has_obj(eb.authors, 'last_name', 'Kan'))
        self.assertTrue(has_obj(eb.authors, 'last_name', 'King'))
        self.assertTrue(has_obj(eb.genres, 'name', 'Romance'))
        self.assertTrue(has_obj(eb.genres, 'name', 'Fantasy'))
        self.assertEqual(eb.language.name, 'Czech')
        self.assertEqual(eb.series_index, 1)
        self.assertEqual(eb.series.title, ebook_data['series']['title'])

        data = {'title': 'Povidky o necem',
                'id': eb.id, 'version_id': eb.version_id}
        updated_eb, errors = schema.ebook_deserializer_update().load(data)

        self.assertEqual(updated_eb.id, eb.id)
        self.assertFalse(errors)
        self.assertTrue(db.session.dirty)
        db.session.commit()
        ebook_id = updated_eb.id
        myebook_id = updated_eb.id
        db.session.remove()

        eb = model.Ebook.query.get(ebook_id)
        self.assertEqual(eb.title, 'Povidky o necem')
        self.assertEqual(eb.version_id, 2)

        # test version id
        db.session.close()
        db.session.remove()
        data = {'title': 'Povidky o vsem',
                'id': ebook_id, 'version_id': 1}

        # must handle manually if not in one session
        version_id = data.pop('version_id')
        updated_eb, errors = schema.ebook_deserializer_update().load(data)
        self.assertFalse(errors)
        if version_id != updated_eb.version_id:
            db.session.rollback()
        else:
            self.assertTrue(db.session.dirty)
            db.session.commit()
        db.session.close()
        db.session.remove()
        eb = model.Ebook.query.get(ebook_id)
        self.assertEqual(eb.title, 'Povidky o necem')
        self.assertEqual(eb.version_id, 2)

        db.session.remove()

        # test new series
        ns = deepcopy(ebook_data)
        ns['series'] = {'title': 'Maly bojovnik'}
        eb, errors = schema.ebook_deserializer_insert().load(ns)
        self.assertFalse(errors)
        self.assertTrue(inspect(eb.series).transient)
        db.session.add(eb)
        self.assertTrue(inspect(eb.series).pending)
        print(eb.series)
        db.session.commit()
        ebook_id = eb.id
        db.session.close()
        db.session.remove()

        eb = model.Ebook.query.get(ebook_id)
        self.assertEqual(eb.series.title, 'Maly bojovnik')

        # test strange series
        strange = deepcopy(ebook_data)
        strange['series'] = {'pako': 'mako'}
        eb, errors = schema.ebook_deserializer_insert().load(strange)
        self.assertFalse(errors)
        db.session.add(eb)
        try:
            db.session.commit()
            self.fail('Should throw error')
        except:
            pass
        
        db.session.close()
        db.session.remove()
        
        
        # test null series
        ns = deepcopy(ebook_data)
        ns['series'] = None
        eb, errors = schema.ebook_deserializer_insert().load(ns)
        self.assertFalse(errors)
        self.assertTrue(db.session.dirty)
        db.session.add(eb)
        db.session.commit()
        ebook_id = eb.id
        db.session.close()
        db.session.remove()

        eb = model.Ebook.query.get(ebook_id)
        self.assertFalse(eb.series)
        
        # test empty series
        ns = deepcopy(ebook_data)
        ns['series'] = {}
        eb, errors = schema.ebook_deserializer_insert().load(ns)
        self.assertFalse(errors)
        self.assertTrue(db.session.dirty)
        db.session.add(eb)
        try:
            db.session.commit()
            self.fail('Should throw error')
        except:
            pass
        
        db.session.close()
        db.session.remove()
        #test series edit
        eb, errors = schema.ebook_deserializer_update().load({'id':myebook_id, 'series':{'title': "Uplne nova"}})
        self.assertEqual(eb.title, 'Povidky o necem')
        self.assertTrue(inspect(eb).persistent and inspect(eb).modified)
        self.assertTrue(inspect(eb.series).pending)
        self.assertFalse(inspect(eb.series).has_identity)
        db.session.commit()
        
        db.session.close()
        db.session.remove()
        
        eb=model.Ebook.query.get(myebook_id)
        self.assertEqual(eb.series.title, "Uplne nova")
        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
