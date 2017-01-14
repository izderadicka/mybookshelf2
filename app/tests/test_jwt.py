'''
Created on Apr 18, 2016

@author: ivan
'''
import unittest
from common.utils import create_token, verify_token, create_refresh_token
from app.model import User
from .basecase import TestCase


class Test(TestCase):

    def test_jwt(self):
        user = User(id=55, user_name='kulich', email='kulich@example.com')
        secret = 'ZZigIKCHuSNeSHwfU+TAbyNX4nwyMUDRXnv0aZgBlOM'
        token = create_token(user, secret)
        claim = verify_token(token, secret)
        self.assertEqual(user.id, claim['id'])
        self.assertEqual(user.user_name, claim['user_name'])
        self.assertEqual(user.email, claim['email'])
        self.assertTrue(verify_token(token, 'bad secret') is None)
        token2 = create_token(user, secret, -0.5)
        self.assertTrue(verify_token(token2, secret) is None)
        claim = verify_token(token2, secret, validate_expiration=False)
        self.assertEqual(user.id, claim['id'])
        
        token3 = create_refresh_token(user, secret, valid_hours = 24*364)
        claim = verify_token(token3, secret)
        self.assertEqual(user.id, claim['id'])


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.test_jwt']
    unittest.main()
