'''
Created on Nov 1, 2016

@author: ivan
'''
import unittest

from common.utils import lev, damlev, remove_diacritics


class Test(unittest.TestCase):


    def test_distance(self):
        self.assertEqual(damlev('abcd', 'abcd'), 0)
        self.assertEqual(lev('abcd', 'abcd'), 0)
        self.assertEqual(damlev('abcd', 'abc'), 1)
        self.assertEqual(lev('abcd', 'abc'), 1)
        self.assertEqual(damlev('abcd', 'abxd'), 1)
        self.assertEqual(lev('abcd', 'abxd'), 1)
        self.assertEqual(damlev('abcd', 'abdc'), 1)
        self.assertEqual(lev('abcd', 'abdc'), 2)
        
        
    def test_dedia(self):
        self.assertEqual(remove_diacritics('ěščřžýáíéúů'), 'escrzyaieuu')
        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_']
    unittest.main()