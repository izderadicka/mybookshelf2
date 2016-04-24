'''
Created on Apr 23, 2016

@author: ivan
'''
import unittest
from basecase import BaseTest 
from server import db,app
import model

class Test(BaseTest):

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
        
        self.assertEqual(ebook.id, 34513)
        authors=ebook.authors
        print()
        self.assertEqual(len(authors),1)
        self.assertEqual(authors[0].last_name, 'Gemmell')
        self.assertEqual(len(ebook.sources),4)
        
        na = model.Author(last_name='Usak', first_name='Kulisak')
        ns = model.Series(title='Voloviny')
        nb = model.Ebook(title='Title', rating=100, language=model.Language.query.filter_by(name='Czech').one())
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


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()