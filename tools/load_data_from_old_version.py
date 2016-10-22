import argparse
import mysql.connector as mysql
import os.path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import sys
import re
import random
import shutil
import tempfile
import subprocess
import traceback
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import app.model as model
import app.logic as logic
from app import app
from common.utils import hash_pwd
import settings


lmap = lambda func, *iterable: list(map(func, *iterable))
flat = lambda l: lmap(lambda r: r[0], l)


def split_name(name):
    parts = lmap(lambda s: s.strip(), name.split(','))
    if len(parts) == 1:
        f = None
        l = parts[0]
    elif len(parts) == 2:
        f = parts[1]
        l = parts[0]
    else:
        l = parts[0]
        f = ' '.join(parts[1:])

    return f, l


def get_all_flat(c2, q, id):  # @ReservedAssignment
    c2.execute(q, (id,))
    return flat(c2.fetchall())


def load_model(c, session, q, cls, pmap):
    c.execute(q)
    for row in c:
        data = dict(zip(c.column_names, row))
        kwargs = {k: data[v] for k, v in pmap.items()}
        kwargs['id'] = data['id']
        o = cls(**kwargs)
        session.add(o)
    session.commit()
    print('Loaded %s: %d records' % (cls.__name__, session.query(cls).count()))


def update_seq(e, table_name):
    e.execute(
        "select setval('{0}_id_seq',(select max(id) from {0}), true);".format(table_name))



def prepare_db(engine):
    SQL_DIR = os.path.join(os.path.dirname(__file__), '../sql')
    
    connection = engine.raw_connection()  # @UndefinedVariable
    try:
        c = connection.cursor()
        for fname in ('create_ts.sql', 'create_functions.sql'):
            script = open(os.path.join(SQL_DIR, fname), 'rt', encoding='utf-8-sig').read()
            # print(script)
            res = c.execute(script)
        connection.commit()
        
        synonyms = open(os.path.join(SQL_DIR, 'dump/basic.sql')).read()
        for cmd in re.finditer('^insert into synonym.*$', synonyms, re.MULTILINE|re.IGNORECASE):
            c.execute(cmd.group(0))
        connection.commit()
    finally:
        connection.close()
    

def export_data(args):
    
# MySql connections
    conn = mysql.connect(host=args.host, port=args.port, user=args.user, password=args.pwd,
                         database=args.db, charset='utf8')
    conn2 = mysql.connect(host=args.host, port=args.port, user=args.user, password=args.pwd,
                          database=args.db,  charset='utf8')
    c = conn.cursor()
#########################################################

# Postgresql - create session and clear and initialize DB
    engine = create_engine(settings.SQLALCHEMY_DATABASE_URI)
    Session = sessionmaker(bind=engine)
    model.Base.metadata.drop_all(bind=engine)  # @UndefinedVariable
    model.Base.metadata.create_all(bind=engine)  # @UndefinedVariable
    prepare_db(engine)
    session = Session(autoflush=False)
#########################################################
    
# Codelists genre, language format
    load_model(c, session, 'select id,name from ebook_subject',
               model.Genre, {'name': 'name'})
    load_model(c, session, 'select id, code, name from ebook_language',
               model.Language, {'code': 'code', 'name': 'name'})

    load_model(c, session, ' select id, mime_type, name, extension from ebook_format',
               model.Format, {'mime_type': 'mime_type', 'name': 'name', 'extension': 'extension'})
    
    #fix fb2 mimetype
    f = model.Format.query.filter_by(extension='fb2').one()
    f.mime_type='application/x-fictionbook+xml'
    # fix pdb mimetype
    f = model.Format.query.filter_by(extension='pdb').one()
    f.mime_type = 'application/x-aportisdoc'
    session.commit()
    print('Created genres, languages and formats')
#############################################################################    

# New user admin and standard roles
    now = datetime.now()
    parent = None
    for r in ['guest', 'user', 'trusted_user', 'superuser', 'admin']:
        role = model.Role(name=r, parent=parent)
        session.add(role)
        session.flush()
        parent = role
    admin = model.User(user_name="admin", password=hash_pwd(
        "admin"), email="admin@example.com", created=now, active=True)
    session.add(admin)
    admin.roles.append(role)
    session.commit()
    print("Created user roles")
###################################################################################

    def auditable_attrs(data):
        return {'created_by': admin, 'modified_by': admin,
                'created': data['created'], 'modified': data['modified'],
                'id': data['id']
                }
        
# Authors
    no_author_id = None
    q = 'select id, created, modified, name, description from ebook_author'
    c.execute(q)
    for row in c:
        data = dict(zip(c.column_names, row))
        first, last = split_name(data['name'])
        if last == '__NONE__':
            no_author_id = data['id']
            print('No author id is %d' % no_author_id)
            continue
        o = model.Author(
            first_name=first, last_name=last, **auditable_attrs(data))
        session.add(o)

    session.commit()
    print('Loaded Authors: %d records' % session.query(model.Author).count())
##################################################################

# Series
    q = 'select id, created, modified, title, rating from ebook_serie'
    c.execute(q)
    for row in c:
        data = dict(zip(c.column_names, row))

        o = model.Series(
            title=data['title'],  rating=data['rating'], **auditable_attrs(data))
        session.add(o)

    session.commit()
    print('Loaded Series: %d records' % session.query(model.Series).count())
########################################################################

# Ebooks
    q = 'select id, created, modified, title, rating, author_id, description, language_id, serie_id, serie_index from ebook_ebook'
    c.execute(q)
    count = 0
    for row in c:
        if args.sample:
            if   random.randint(1,args.sample) > 1:
                continue
        data = dict(zip(c.column_names, row))
        language = session.query(model.Language).get(data['language_id'])
        series = session.query(model.Series).get(
            data['serie_id']) if data['serie_id'] else None
        primary_author = session.query(model.Author).get(data['author_id']) if data[
            'author_id'] and data['author_id'] != no_author_id else None
        o = model.Ebook(title=data['title'], rating=data['rating'], description=data['description'],
                        language=language, series=series, series_index=data[
            'serie_index'],
            **auditable_attrs(data))
        if primary_author:
            o.authors.append(primary_author)

        c2 = conn2.cursor()
        q2 = 'select author_id from ebook_ebook_other_authors where ebook_id=%s'
        c2.execute(q2, (data['id'],))
        authors = flat(c2.fetchall())
        if authors:
            authors = session.query(model.Author).filter(
                model.Author.id.in_(authors)).all()  # @UndefinedVariable
            o.authors.extend(authors)

        q2 = 'select subject_id from ebook_ebook_subjects where ebook_id=%s'
        c2.execute(q2, (data['id'],))
        genres = flat(c2.fetchall())
        if genres:
            genres = session.query(model.Genre).filter(
                model.Genre.id.in_(genres)).all()  # @UndefinedVariable
            o.genres.extend(genres)
        c2.close()
        #Set base directory
        with app.app_context():
            logic.update_ebook_base_dir(o)
        session.add(o)
        count += 1
        if not count % 1000:
            print('Loaded Ebook %d records\r' % count, end='')
            session.commit()
    session.commit()
    print('Loaded Ebook: %d records' % session.query(model.Ebook).count())
####################################################

# Sources
    q = 'select id, created, modified, ebook_id, location, format_id, size, crc, quality from ebook_source'
    c.execute(q)
    count = 0
    for row in c:
        data = dict(zip(c.column_names, row))
        ebook = session.query(model.Ebook).get(data['ebook_id'])
        if not ebook:
            continue
        format = session.query(model.Format).get(data['format_id'])
        
        o = model.Source(ebook=ebook, format=format, location=data['location'], size=data['size'],
                         hash=data['crc'], quality=data['quality'], **auditable_attrs(data))
        
        #Copy files
        if args.dir:
            fname= os.path.join(args.dir, data['location'])
            with app.app_context():
                location=logic.create_new_location(o, fname)
            o.location=location 
            #Extract cover
            if not o.ebook.cover:
                try:
                    cover=extract_cover(o)
                    ebook.cover=cover
                except Exception:
                    traceback.print_exc()
                    
        session.add(o)
        count += 1
        if not count % 1000:
            print('Loaded Source %d records\r' % count, end='')
            session.commit()

    session.commit()
    print('Loaded Source: %d records' % session.query(model.Source).count())
##########################################################################################

# Bookshelves
    q = 'select id, created, modified, name, description, public, rating from ebook_bookshelf'
    c.execute(q)
    for row in c:
        data = dict(zip(c.column_names, row))
        o = model.Bookshelf(name=data['name'], description=data['description'], public=bool(data['public']),
                            rating=data['rating'], **auditable_attrs(data))
        session.add(o)

    session.commit()
    print('Loaded Bookshelf: %d records' %
          session.query(model.Bookshelf).count())

    q = 'select id, created, modified, type, bookshelf_id, ebook_id, serie_id, `order`, note from ebook_bookshelfitem'
    c.execute(q)
    for row in c:
        data = dict(zip(c.column_names, row))
        ebook = session.query(model.Ebook).get(
            data['ebook_id']) if data['ebook_id'] else None
        series = session.query(model.Series).get(
            data['serie_id']) if data['serie_id'] else None
        bookshelf = session.query(model.Bookshelf).get(data['bookshelf_id'])
        type = 'EBOOK' if data['type'] == 1 else 'SERIES' if data[
            'type'] == 2 else None
        if not type:
            print('Error invalid bookshelfitem type on %s' %
                  str(row), file=sys.stderr)
            continue
        elif type == 'EBOOK' and not ebook:
            print('Error invalid bookshelfitem, type is ebook but no book - %s' %
                  str(row), file=sys.stderr)
            continue
        elif type == 'SERIES' and not series:
            print('Error invalid bookshelfitem, type is series but no series - %s' %
                  str(row), file=sys.stderr)
            continue

        o = model.BookshelfItem(type=type, ebook=ebook, series=series, bookshelf=bookshelf, order=data['order'],
                                note=data['note'], **auditable_attrs(data))

        session.add(o)

    session.commit()
    print('Loaded BookshelfItem: %d records' %
          session.query(model.BookshelfItem).count())
    
############################################################################

    for t in ['author', 'bookshelf', 'bookshelf_item', 'ebook', 'format', 'genre', 'language', 'series', 'source']:
        update_seq(engine, t)

    session.close()
    c.close()
    conn.close()
    conn2.close()
    return

def clear_directories():
    for dir in [settings.UPLOAD_DIR, settings.BOOKS_CONVERTED_DIR, settings.THUMBS_DIR,
                settings.BOOKS_BASE_DIR]:
        shutil.rmtree(dir, ignore_errors=True)
        os.makedirs(dir, exist_ok=True)
        
def extract_cover(source):
    f = os.path.join(settings.BOOKS_BASE_DIR, source.location)
    temp_dir=tempfile.mkdtemp(dir=settings.UPLOAD_DIR)
    if f.endswith('.doc'):
        OOFFICE='soffice'
        proc= subprocess.Popen([OOFFICE, '--headless', '--convert-to', 'odt','--outdir', temp_dir, f])
        retcode=proc.wait(120)
        fname= os.path.basename(f)
        out_file=os.path.splitext(fname)[0]+'.odt'
        out_file=os.path.join(temp_dir, out_file)
        if not os.path.exists(out_file):
            return 
        f= out_file
    
    cover_file = os.path.join(temp_dir, 'cover_in.jpg')
    proc = subprocess.Popen(['ebook-meta', '--get-cover=%s'%cover_file, f])
    retcode = proc.wait(timeout=30)
    if retcode!=0 or not os.path.exists(cover_file):
        return
    IMAGE_MAGIC = 'convert'
    cover_out = os.path.join(temp_dir, 'cover.jpg')
    proc = subprocess.Popen([IMAGE_MAGIC, cover_file, '-fuzz', '7%',
                            '-trim', '-resize', '%dX%d'%settings.COVER_SIZE, cover_out])
    retcode=proc.wait(10)
    if retcode!=0 or not os.path.exists(cover_out):
        return
    thumb_out =  os.path.join(temp_dir, settings.THUMBNAIL_FILE)
    proc = subprocess.Popen([IMAGE_MAGIC, cover_out, '-resize', '%dX%d'%settings.THUMBNAIL_SIZE, thumb_out])
    proc.wait()
    
    ebook_cover = os.path.join(source.ebook.base_dir, 'cover.jpg')
    dst = os.path.join(settings.BOOKS_BASE_DIR, ebook_cover)
    shutil.move(cover_out, dst)
    if os.path.exists(thumb_out):
        shutil.move(thumb_out, os.path.join(settings.THUMBS_DIR, '%d.jpg'%source.ebook.id))
    return ebook_cover
    
    
    
    
    
    
         

def main():
    p = argparse.ArgumentParser()
    
    p.add_argument('-H', '--host', default='localhost', help='MySQL host')
    p.add_argument('-p', '--port', type=int, default=3306, help='MySQL port')
    p.add_argument('--user', default='ebooks', help='db user')
    p.add_argument('--pwd', default='', help='db user password')
    p.add_argument('--db', default='ebooks', help='db name')
    p.add_argument('--dir', help='base directory with ebook files, will copy files to current ebooks directory')
    p.add_argument('--sample', type=int, default=0, help="Sample randomly 1 of n ebooks")
    #p.add_argument('--limit', type=int, help='limit number of records to')
    args = p.parse_args()
    print('This tool will migrate data from Mybookshelf (previous version)')
    print("It'll delete all data from existing DB")
    answer=input('Continue [Y/N]?: ')
    if answer.strip().lower() != 'y':
        return
    clear_directories()
    export_data(args)

    print('Done')

if __name__ == '__main__':
    main()
