'''
Created on Apr 18, 2016

@author: ivan
'''
import unittest
from app.utils import hash_pwd, check_pwd

class Test(unittest.TestCase):


    def test_hash(self):
        p='my secret password'
        h=hash_pwd(p)
        self.assertTrue(check_pwd(p, h))
        self.assertTrue(check_pwd(p, h.encode('utf-8')))


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_hash']
    unittest.main()