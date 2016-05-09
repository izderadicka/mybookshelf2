from .basecase import TestCase
from flask import current_app
import app
import app.model as model
from app.utils import hash_pwd


class TestViews(TestCase):
    
    def test_login(self):
        with self.client as c:
            res=c.get('/')
            self.assertTrue('Welcome' in str(res.data))
            
            def test_login(user, pwd, check=[]):
                res=c.post('/login', data={'username':user, 'password':pwd}, 
                       follow_redirects=True)
                self.assert200(res)
                if isinstance(check, str):
                    check=[check] 
                for phrase in check:
                    self.assertTrue(phrase.lower() in str(res.data).lower(), 'Result should contain %s'%phrase)
            
            res=c.get('/login')
            self.assertTrue('User Name:' in str(res.data) and 'Password:' in str(res.data))
            test_login('admin', 'admin', 'Welcome')
            
            
            res=c.get('/logoff', follow_redirects=True)
            self.assert200(res)
            self.assertTrue('User Name:' in str(res.data) and 'Password:' in str(res.data))
            
            test_login('admin', 'wrong', 'Invalid user name or password')
            test_login('usak', 'wrong', 'Invalid user name or password')
            
            def test_login_json(user, pwd, success=True, failure=False, email=None):
                if email:
                    res=c.post('/login', data='{"email":"%s", "password":"%s"}'%(email,pwd), 
                           content_type='application/json' )
                else:
                    res=c.post('/login', data='{"username":"%s", "password":"%s"}'%(user,pwd), 
                           content_type='application/json' )
                if success:
                    self.assert200(res)
                    self.assertTrue(res.json.get('access_token') and len(res.json.get('access_token'))>60)
                elif not failure:
                    self.assert200(res)
                    self.assertEqual(res.json, { "error": "Invalid Login" } )
                else:
                    self.assert400(res)
                    
            test_login_json('admin', 'admin', success=True)
            test_login_json(None, 'admin', email='admin@example.com', success=True)
            test_login_json('admin', 'xxx', success=False)
            test_login_json('pakomako', 'admin', success=False)
            test_login_json('admin', '', success=False, failure=True)
            test_login_json('', '', success=False, failure=True)
            
            new_user=model.User(user_name='test', email='test@example.com', password=hash_pwd('test'), active=True)
            app.db.session.add(new_user)
            app.db.session.commit()
            
            test_login_json('test', 'test', success=True)
            new_user.active=False
            app.db.session.commit()
            test_login_json('test', 'test', success=False)
            
            
    def test_views(self):
        with self.client as c:
            res=c.post('/login', data={'username':'admin', 'password':'admin'}, 
                       follow_redirects=True)
            self.assert200(res)
            
            res=c.get('/')
            self.assert200(res)
            
            res=c.get('/search')
            self.assert200(res)
            self.assertTrue('Search:' in str(res.data))
            
            res=c.get('/search?search=kissinger+bilem')
            self.assert200(res)
            self.assertTrue('Roky v Bílém domě' in str(res.data, encoding='utf-8'))
            
            res=c.get('/ebooks/61944')
            self.assert200(res)
            self.assertTrue('docx' in str(res.data))
            
            res=c.get('/download/86060')
            self.assert200(res)
            self.assertEqual(int (res.headers['Content-Length']), 3147900)
            self.assertEqual(res.headers['Content-Type'], 'application/epub+zip')
            self.assertEqual(len(res.data), 3147900)
            
        
            
            
                    
                
            
            
            
            
            