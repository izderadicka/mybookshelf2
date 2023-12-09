'''
Created on Apr 23, 2016

@author: ivan
'''
import unittest
from app import db,app
import app.model as model
from .basecase import TestCase 

class Test(TestCase):

    def test_trigger_exists(self):
        connection = db.engine.raw_connection()
        c=connection.cursor()
        c.execute("select tgname from pg_trigger where tgname like 'ebook_ts_%';")
        res=c.fetchall()
        self.assertTrue(len(res) == 5)
        
    def test_models(self):
        n=model.Format.query.filter().count()
        self.assertEqual(n, 17)
        n=model.Genre.query.filter().count()
        self.assertEqual(n, 57)
        n=model.Language.query.filter().count()
        self.assertEqual(n, 4)
        
        l=model.Language(name='German', code='de')
        db.session.add(l)
        db.session.commit()
        
        n=model.Language.query.filter().count()
        self.assertEqual(n, 5)
        
        ebook=model.Ebook.query.filter(model.Ebook.title=='Legenda').one()
        self.assertEqual(str(ebook),'<Ebook id=34513 title="Legenda">')
        self.assertEqual(ebook.id, 34513)
        authors=ebook.authors
        print()
        self.assertEqual(len(authors),1)
        self.assertEqual(authors[0].last_name, 'Gemmell')
        self.assertEqual(len(ebook.sources),4)
        
        na = model.Author(last_name='Usak', first_name='Kulisak')
        ns = model.Series(title='Voloviny')
        nb = model.Ebook(title='Title', rating=100, 
                         language=model.Language.query.filter_by(name='Czech').one(), base_dir='test')
        db.session.add_all([na,ns, nb])
        nb.authors.extend([na, authors[0]])
        nb.series=ns
        db.session.commit()
        db.session.remove()
        
        with app.app_context():
            b=model.Ebook.query.filter_by(title='Title').one()
            self.assertEqual(b.series.title, 'Voloviny')
            self.assertTrue(len(b.authors),2)
            b.series.title='Kraviny'
            db.session.commit()
            
            db.session.remove()
            db.session.expire_all()
            b=model.Ebook.query.filter_by(title='Title').one()
            self.assertEqual(b.series.title, 'Kraviny')
        
            ft=str(b.full_text)
            self.assertTrue(b.full_text )
            self.assertTrue('gemmel' in ft and 'krav' in ft and 'kulisak' in ft)
            
        u=model.User.query.filter_by(user_name='admin').one()
        self.assertEqual(len(u.all_roles), 5)
        self.assertTrue(u.has_role('admin'))
        self.assertTrue(u.has_role('user'))
        self.assertTrue(u.has_role('xxx', 'superuser'))
        self.assertFalse(u.has_role('xxx'))
        
        series=model.Series.query.get(1633)
        self.assertEqual(series.title, 'Na stopě hrůzy')
        self.assertEqual(len(series.authors),2)
        self.assertTrue(any(map(lambda x: x.last_name =='Dark' and x.first_name =='Jason', series.authors)))
        self.assertTrue(any(map(lambda x: x.last_name =='Tenkrat' and x.first_name =='Friedrich', series.authors)))
        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()