from basecase import TestCase
from flask import current_app
import app


class TestViews(TestCase):
    
    def test_login(self):
        with self.client as c:
            res=c.get('/')
            self.assertTrue('Welcome' in str(res.data))
            
            res=c.get('/login')
            self.assertTrue('User Name:' in str(res.data) and 'Password:' in str(res.data))
            
            res=c.post('/login', data={'username':'admin', 'password':'admin'}, 
                       follow_redirects=True)
            self.assert200(res)
            self.assertTrue('Welcome' in str(res.data))
            
            
            