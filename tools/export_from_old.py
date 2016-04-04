import argparse
import mysql.connector as mysql
import json
from collections import OrderedDict
from bson.objectid import ObjectId
import os.path

EBOOKS_FILE='ebooks.json'

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
def map_authors(l):
    return [OrderedDict((('lastname',l),('firstname',f))) for f,l in map(split_name,l)]


def get_all_flat(c2, q, id):  # @ReservedAssignment
        c2.execute(q, (id,))
        return flat(c2.fetchall())

def export_data(args):
    conn=mysql.connect(host=args.host, port=args.port, user=args.user, password=args.pwd, 
                       database=args.db, charset='utf8')
    conn2=mysql.connect(host=args.host, port=args.port, user=args.user, password=args.pwd, 
                       database=args.db,  charset='utf8')
    c=conn.cursor()
    q="""select b.id, b.title, b.rating, b.serie_index, a.name as author_name, 
    s.title as serie_title, l.code as language_code
    from ebook_ebook b left outer join ebook_serie s on (s.id=b.serie_id) , 
    ebook_author a,  ebook_language l 
    where b.author_id=a.id and  b.language_id=l.id"""
    if args.limit:
        q+=" limit %d" % args.limit
    c.execute(q)
    first=True
    with open(os.path.join(args.directory, EBOOKS_FILE), 'w') as f:
        f.write('[')
        for row in c:
            data = dict(zip(c.column_names, row))
            c2=conn2.cursor()
            q="""select a.name from ebook_author a, ebook_ebook_other_authors r, ebook_ebook b
            where a.id=r.author_id and b.id=r.ebook_id and b.id=%s"""
            
            authors = get_all_flat(c2, q, data['id'])
            q="""select a.name from ebook_subject a, ebook_ebook_subjects r, ebook_ebook b
            where a.id=r.subject_id and b.id=r.ebook_id and b.id=%s"""
            genres=get_all_flat(c2, q, data['id'])
            q="""select s.location, s.size, s.crc, s.quality, s.load_source, f.extension 
            from ebook_source s, ebook_format f where s.format_id=f.id and s.ebook_id=%s
            """
            c2.execute(q, (data['id'], ))
            sources=[]
            for line in c2:
                src=dict(zip(c2.column_names, line))
                sources.append(OrderedDict((
                                ('_id', {'$oid': str(ObjectId())}),
                                ('format', src['extension']),
                                ('size', src['size']),
                                ('hash', src['crc']),
                                ('location', src['location']),
                                ('original_name', src['load_source']),
                                ('quality', src['quality'])
                                )))
            c2.close()
            
            ebook=OrderedDict((
                    ('title',data['title']), 
                   ('authors', map_authors([data['author_name']]+authors)),
                   ('series', data['serie_title']),
                   ('series_index', data['serie_index']),
                   ('rating', data['rating']),
                   ('language', data['language_code']),
                   ('genres', genres),
                   ('sources', sources)
                   ))
            #print (json.dumps(ebook))
            if not first:
                f.write(',\n')
            first=False
            t=json.dumps(ebook, ensure_ascii=False)
            #print(t)
            f.write(t)
        
        f.write(']')    
    c.close()
    conn.close()
    conn2.close()
    
def main():
    p=argparse.ArgumentParser()
    p.add_argument('directory', help='output directory')
    p.add_argument('-H','--host', default='localhost', help='MySQL host')
    p.add_argument('-p', '--port', type=int, default=3306, help='MySQL port')
    p.add_argument('--user', default='ebooks', help='db user')
    p.add_argument('--pwd', default='', help='db user password')
    p.add_argument('--db', default='ebooks', help='db name')
    p.add_argument('--limit', type=int, help='limit number of records to')
    args=p.parse_args()
    export_data(args)
    
if __name__=='__main__':
    main()
    
    