'''
Created on Apr 18, 2016

@author: ivan
'''
import unittest
from utils import create_token, verify_token


class Test(unittest.TestCase):


    def test_jwt(self):
        id=55
        secret='ZZigIKCHuSNeSHwfU+TAbyNX4nwyMUDRXnv0aZgBlOM'
        token=create_token(id, secret)
        self.assertEqual(id, verify_token(token, secret))
        self.assertTrue(verify_token(token, 'bad secret') is None)
        token2=create_token(id, secret, -30)
        self.assertTrue(verify_token(token2,secret) is None)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_jwt']
    unittest.main()