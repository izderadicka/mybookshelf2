from app import db, app
import app.model as model
import app.logic as logic
from .basecase import TestCase
import os.path


ebook_file = os.path.join(os.path.dirname(
    __file__), '../data/books/Kissinger, Henry/Roky v Bilem dome/Kissinger, Henry - Roky v Bilem dome.epub')


class TestLogic(TestCase):

    def test_logic(self):

        b1 = model.Ebook.query.get(33837)
        self.assertEqual(b1.authors_str, 'Crichton Michael')

        b2 = model.Ebook.query.get(37157)
        self.assertEqual(b2.authors_str, 'Strugackij A N, Strugackij B N')

        b3 = model.Ebook.query.get(62546)
        self.assertEqual(b3.authors_str, 'Wilkins G, Dalton M, Young K')
        b3.authors.append(b1.authors[0])

        self.assertEqual(
            b3.authors_str, 'Wilkins G, Dalton M, Young K and others')

        b1.authors = []
        self.assertEqual(b1.authors_str, 'No Authors')

        source = model.Source.query.get(46519)
        name = logic.norm_file_name(source)
        self.assertEqual(
            name, 'Strugackij A N, Strugackij B N/Noc na Marse/Strugackij A N, Strugackij B N - Noc na Marse.doc')

        source = model.Source.query.get(63546)
        name = logic.norm_file_name(source)
        self.assertEqual(
            name, 'Monroe Lucy/Nevesty od Stredozemniho more/Nevesty od Stredozemniho more 2 - Spanelova milenka/Monroe Lucy - Nevesty od Stredozemniho more 2 - Spanelova milenka.doc')

        res = logic.check_uploaded_file('application/epub+zip', ebook_file)
        self.assertEqual(res['error'], 'file already exists')
