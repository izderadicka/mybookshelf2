'''
Created on Mar 21, 2016

@author: ivan
'''
import unittest
from eve.io.mongo import Validator as BaseValidator
import settings
import os.path
import json
from bson import ObjectId

class Validator(BaseValidator):
    def _validate_type_objectid(self, field, value):
        """ Enables validation for `objectid` data type.

        :param field: field name.
        :param value: field value.

        .. versionchanged:: 0.3
           Support for new 'self._error' signature introduced with Cerberus
           v0.5.

        .. versionchanged:: 0.1.1
           regex check replaced with proper type check.
        """
        if isinstance(value, ObjectId):
            pass
        if isinstance(value, dict) and len(value)==1:
            try:
                ObjectId(value['$oid'])
            except Exception as e:
                self._error(field, 'value %s conversion error %s' % (value, e))
        else:
            self._error(field, "value '%s' cannot be converted to a ObjectId"
                        % value)

doc=os.path.join(os.path.dirname(__file__), '../data/test-ebooks.json')
class Test(unittest.TestCase):


    def test_schemes(self):
        v=Validator(settings.ebooks['schema'])
        v.validate_schema(settings.author['schema'])
        
    def test_validation(self):
        v=Validator(settings.ebooks['schema'])
        data=json.load(open(doc))
        i=0
        for b in data:
            res=v.validate(b)
            if not res:
                print(v.errors)
            self.assertTrue(res, 'item %d invalid'%i)
            i+=1
        self.assertEqual(i, 10)
        
    def test_validation_error(self):
        v=Validator(settings.ebooks['schema'])
        self.assertFalse(v.validate({}))
    

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_schemes']
    unittest.main()