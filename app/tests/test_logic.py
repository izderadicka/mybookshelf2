from app import db, app
import app.model as model
import app.logic as logic
import common.utils as utils
from .basecase import TestCase
import os.path
import shutil
import settings


ebook_file = os.path.join(os.path.dirname(__file__),
                          'data/Kissinger, Henry - Roky v Bilem dome.epub')

downloaded_file = os.path.join(settings.UPLOAD_DIR, 'kissinger.epub')


class TestLogic(TestCase):

    def setUp(self):
        TestCase.setUp(self)
        shutil.copy(ebook_file, downloaded_file)

    def tearDown(self):
        TestCase.tearDown(self)
        shutil.rmtree(downloaded_file, ignore_errors=True)
        shutil.rmtree(os.path.join(settings.BOOKS_BASE_DIR, 'Kissinger Henry'))

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
            name, 'Strugackij A N, Strugackij B N/Noc na Marse(sk)/Strugackij A N, Strugackij B N - Noc na Marse.doc')

        source = model.Source.query.get(63546)
        name = logic.norm_file_name(source)
        self.assertEqual(
            name, 'Monroe Lucy/Nevesty od Stredozemniho more/Nevesty od Stredozemniho more 2 - Spanelova milenka(cs)/Monroe Lucy - Nevesty od Stredozemniho more 2 - Spanelova milenka.doc')

        res = logic.check_uploaded_file('application/epub+zip', ebook_file)
        self.assertEqual(res['error'], 'file already exists')

        size = os.stat(downloaded_file).st_size
        hash = utils.file_hash(downloaded_file)

        s = model.Source.query.get(86060)

        new_loc = logic.create_new_location(s, downloaded_file)
        self.assertEqual(
            new_loc, 'Kissinger Henry/Roky v Bilem dome(cs)/Kissinger Henry - Roky v Bilem dome.epub')

        shutil.copy(ebook_file, downloaded_file)
        new_loc = logic.create_new_location(s, downloaded_file)
        self.assertEqual(
            new_loc, 'Kissinger Henry/Roky v Bilem dome(cs)/Kissinger Henry - Roky v Bilem dome(1).epub')

        admin = model.User.query.get(1)
        conv = model.Conversion(source=source, format=model.Format.query.filter_by(extension='epub').one(),
                                location='bla.epub', created_by=admin, modified_by=admin)
        db.session.add(conv)
        db.session.commit()

        res = logic.query_converted_sources_for_ebook(
            source.ebook.id, admin).all()
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0].location, 'bla.epub')

        b1 = model.Ebook.query.get(33837)
        b2 = model.Ebook.query.get(37157)
        tot = len(b1.sources) + len(b2.sources)
        logic.merge_ebook(b1, b2)
        self.assertEqual(len(b1.sources), tot)
