import argparse
import mysql.connector as mysql
import os.path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import sys
sys.path.append(os.path.join(os.path.dirname(__file__),'..'))

import app.model as model
from app.utils import hash_pwd


lmap = lambda func, *iterable: list(map(func, *iterable))
flat=  lambda l: lmap(lambda r:r[0], l)
                                    
def split_name(name):
    parts=lmap(lambda s: s.strip(), name.split(','))
    if len(parts) ==1:
        f=None
        l=parts[0]
    elif len(parts) == 2:
        f=parts[1]
        l=parts[0]
    else:
        l=parts[0]
        f=' '.join(parts[1:])
        
    return f,l

def get_all_flat(c2, q, id):  # @ReservedAssignment
        c2.execute(q, (id,))
        return flat(c2.fetchall())


def load_model(c,session, q, cls, pmap):
    c.execute(q)   
    for row in c:
        data = dict(zip(c.column_names, row))
        kwargs={k:data[v] for k,v in pmap.items()}
        kwargs['id']=data['id']
        o= cls(**kwargs)
        session.add(o)
    session.commit()
    print('Loaded %s: %d records' % (cls.__name__, session.query(cls).count()))
    
def update_seq(e,table_name):
    e.execute("select setval('{0}_id_seq',(select max(id) from {0}), true);".format(table_name))

def export_data(args):
    conn=mysql.connect(host=args.host, port=args.port, user=args.user, password=args.pwd, 
                       database=args.db, charset='utf8')
    conn2=mysql.connect(host=args.host, port=args.port, user=args.user, password=args.pwd, 
                       database=args.db,  charset='utf8')
    c=conn.cursor()
    
    engine=create_engine(args.pg)
    Session=sessionmaker(bind=engine)
    
    model.Base.metadata.drop_all(bind=engine)  # @UndefinedVariable
    model.Base.metadata.create_all(bind=engine)  # @UndefinedVariable
    
    session=Session()
    load_model(c, session,'select id,name from ebook_subject', model.Genre, {'name':'name'})
    load_model(c, session,'select id, code, name from ebook_language', 
               model.Language, {'code':'code', 'name': 'name'})
    
    load_model(c, session, ' select id, mime_type, name, extension from ebook_format', 
               model.Format, {'mime_type':'mime_type', 'name':'name', 'extension':'extension'})
    
    now=datetime.now()
    parent=None
    for r in ['guest', 'user', 'trusted_user', 'superuser', 'admin']:
        role=model.Role(name=r, parent=parent)
        session.add(role)
        session.flush()
        parent=role
    admin = model.User(user_name="admin", password=hash_pwd("admin"), email="admin@example.com", created=now, active=True)
    session.add(admin)
    admin.roles.append(role)
    session.commit()
    print("Created user roles")
    
    def auditable_attrs(data): 
        return {'created_by':admin, 'modified_by':admin, 
                       'created':data['created'], 'modified':data['modified'],
                       'id':data['id']
                       }
    
    
    no_author_id=None
    q='select id, created, modified, name, description from ebook_author'
    c.execute(q)
    for row in c:
        data = dict(zip(c.column_names, row))
        first,last=split_name(data['name'])
        if last=='__NONE__':
            no_author_id=data['id']
            print('No author id is %d'%no_author_id)
            continue
        o=model.Author(first_name=first, last_name=last, **auditable_attrs(data))
        session.add(o)
        
    session.commit()
    print('Loaded Authors: %d records' % session.query(model.Author).count())
    
    
    q='select id, created, modified, title, rating from ebook_serie'
    c.execute(q)
    for row in c:
        data = dict(zip(c.column_names, row))
        
        o=model.Series(title=data['title'],  rating=data['rating'], **auditable_attrs(data))
        session.add(o)
        
    session.commit()
    print('Loaded Series: %d records' % session.query(model.Series).count())
    
    q='select id, created, modified, title, rating, author_id, description, language_id, serie_id, serie_index from ebook_ebook'
    c.execute(q)
    count=0
    for row in c:
        data = dict(zip(c.column_names, row))
        language=session.query(model.Language).get(data['language_id'])
        series=session.query(model.Series).get(data['serie_id']) if data['serie_id'] else None
        primary_author=session.query(model.Author).get(data['author_id']) if data['author_id'] and data['author_id'] != no_author_id else None
        o=model.Ebook(title=data['title'], rating=data['rating'], description=data['description'],
                      language=language, series=series, series_index=data['serie_index'],
                      **auditable_attrs(data))
        if primary_author:
            o.authors.append(primary_author)
            
        c2=conn2.cursor()
        q2='select author_id from ebook_ebook_other_authors where ebook_id=%s'
        c2.execute(q2, (data['id'],))
        authors=flat(c2.fetchall())
        if authors:
            authors=session.query(model.Author).filter(model.Author.id.in_(authors)).all()  # @UndefinedVariable
            o.authors.extend(authors)
         
        q2='select subject_id from ebook_ebook_subjects where ebook_id=%s'   
        c2.execute(q2, (data['id'],))
        genres=flat(c2.fetchall())
        if genres:
            genres=session.query(model.Genre).filter(model.Genre.id.in_(genres)).all()  # @UndefinedVariable
            o.genres.extend(genres)
        c2.close()    
        session.add(o)
        count+=1
        if not count % 1000:
            print('Loaded Ebook %d records\r'%count, end='')
            session.commit()
    session.commit()
    print('Loaded Ebook: %d records' % session.query(model.Ebook).count())
    
    
    q='select id, created, modified, ebook_id, location, format_id, size, crc, quality from ebook_source'
    c.execute(q)
    count=0
    for row in c:
        data = dict(zip(c.column_names, row))
        format=session.query(model.Format).get(data['format_id'])
        ebook=session.query(model.Ebook).get(data['ebook_id'])
        o=model.Source(ebook=ebook, format=format, location=data['location'], size=data['size'], 
                       hash=data['crc'], quality=data['quality'], **auditable_attrs(data))
        session.add(o)
        count+=1
        if not count % 1000:
            print('Loaded Source %d records\r'%count, end='')
            session.commit()
        
    session.commit() 
    print('Loaded Source: %d records' % session.query(model.Source).count())   
    
    q='select id, created, modified, name, description, public, rating from ebook_bookshelf'
    c.execute(q)
    for row in c:
        data = dict(zip(c.column_names, row))
        o=model.Bookshelf(name=data['name'], description=data['description'], public=bool(data['public']), 
                          rating=data['rating'], **auditable_attrs(data))
        session.add(o)
        
    session.commit()
    print('Loaded Bookshelf: %d records' % session.query(model.Bookshelf).count()) 
    
    q='select id, created, modified, type, bookshelf_id, ebook_id, serie_id, `order`, note from ebook_bookshelfitem'
    c.execute(q)
    for row in c:
        data = dict(zip(c.column_names, row))
        ebook=session.query(model.Ebook).get(data['ebook_id']) if data['ebook_id'] else None
        series=session.query(model.Series).get(data['serie_id']) if data['serie_id'] else None
        bookshelf=session.query(model.Bookshelf).get(data['bookshelf_id'])
        type='EBOOK' if data['type']==1 else 'SERIES' if data['type']==2 else None
        if not type:
            print('Error invalid bookshelfitem type on %s'%row, file=sys.stderr)
            continue
        elif type=='EBOOK' and not ebook:
            print('Error invalid bookshelfitem, type is ebook but no book - %s'%row, file=sys.stderr)
            continue
        elif type=='SERIES' and not series:
            print('Error invalid bookshelfitem, type is series but no series - %s'%row, file=sys.stderr)
            continue
        
        o=model.BookshelfItem(type=type, ebook=ebook, series=series, bookshelf=bookshelf, order=data['order'],
                              note=data['note'], **auditable_attrs(data))    
        
        session.add(o)
        
    session.commit()
    print('Loaded BookshelfItem: %d records' % session.query(model.BookshelfItem).count()) 
    
    
    for t in ['author', 'bookshelf', 'bookshelf_item', 'ebook', 'format', 'genre', 'language', 'series', 'source']:
        update_seq(engine, t)
    
    
    session.close()
    c.close()
    conn.close()
    conn2.close()
    return

    
    
    
def main():
    p=argparse.ArgumentParser()
    p.add_argument('--pg', required=True, help='Postgresql db URI')
    p.add_argument('-H','--host', default='localhost', help='MySQL host')
    p.add_argument('-p', '--port', type=int, default=3306, help='MySQL port')
    p.add_argument('--user', default='ebooks', help='db user')
    p.add_argument('--pwd', default='', help='db user password')
    p.add_argument('--db', default='ebooks', help='db name')
    p.add_argument('--limit', type=int, help='limit number of records to')
    args=p.parse_args()
    export_data(args)
    
    print('Done')
    
if __name__=='__main__':
    main()