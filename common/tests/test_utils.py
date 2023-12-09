import unittest
from common.utils import deep_get


class Test(unittest.TestCase):


    def test_deeep_get(self):
        self.assertEqual(deep_get({'ebook':{"id":1}}, 'ebook.id'), 1)
        self.assertEqual(deep_get({'ebook':{"id":1}}, 'ebook'), {'id':1})
        self.assertEqual(deep_get({'ebook':{"id":1}}, 'ebook.x'), None)
        self.assertEqual(deep_get({'ebook':{"id":1}}, 'ebook.x', 'Boo'), 'Boo')
        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_deeep_get']
    unittest.main()