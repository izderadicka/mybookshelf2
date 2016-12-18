from flask import abort, request, current_app, Response, jsonify
from sqlalchemy.sql import text, desc, func
from functools import wraps
from app import db
import app.model as model
import app.schema as schema
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm import aliased
from sqlalchemy import inspect
from common.utils import remove_diacritics, file_hash, copy_cover, mimetype_from_file_name
import os.path
import filelock
import shutil

import logging
import re
logger = logging.getLogger('logic')


def safe_int(v, for_=''):
    if v is None or v == ' ':
        return
    try:
        v = int(v)
        if v <= 0:
            abort(400, 'Not positive number %s' % for_)
        return v
    except ValueError:
        abort(400, 'Invalid number for %s' % for_)


def preprocess_search_query(text):
    text = re.sub(r'\W', ' ', text, re.UNICODE)
    tokens = text.split()
    tokens = map(lambda t: t.strip(), tokens)
    return ' & '.join(['%s:*' % t for t in tokens])


def search_query(q, search):
    # works only for pg backend
    search = preprocess_search_query(search)
    return q.filter(model.Ebook.full_text.match(search))\
        .order_by(desc(func.ts_rank_cd(model.Ebook.full_text, func.to_tsquery(text("'custom'"), search))))


def filter_ebooks(q, filter):
    return q.filter(func.unaccent(model.Ebook.title).ilike(func.unaccent(text("'%%%s%%'" % filter))))

def filter_shelves(q, filter):
    return q.filter(func.unaccent(model.Bookshelf.name).ilike(func.unaccent(text("'%%%s%%'" % filter))))


def create_new_location(source, upload, move=False):
    base_dir = current_app.config['BOOKS_BASE_DIR']
    if isinstance(upload, model.Upload):
        new_file = os.path.join(current_app.config['UPLOAD_DIR'], upload.file)
    else:
        new_file = upload
    new_location = os.path.join(source.ebook.base_dir, os.path.basename(norm_file_name(source)))
    #if source.ebook.base_dir else norm_file_name(source) #TODO: Remove this WA
    ebook_dir = os.path.join(base_dir, os.path.split(new_location)[0])
    if not os.path.exists(ebook_dir):
        os.makedirs(ebook_dir, exist_ok=True)
    lock_file = os.path.join(ebook_dir, '.lock_this_dir')
    index = 1
    with filelock.SoftFileLock(lock_file, timeout=5):
        while os.path.exists(os.path.join(base_dir, new_location)):
            name, ext = os.path.splitext(new_location)
            new_location = name + '(%d)' % index + ext
            index += 1
        if move:
            shutil.move(new_file, os.path.join(base_dir, new_location))
        else:
            shutil.copy(new_file, os.path.join(base_dir, new_location))

    return new_location


def norm_file_name(source, ext=''):
    if isinstance(source, model.Source):
        ebook = source.ebook
        ext = source.format.extension
    elif isinstance(source, model.Ebook):
        ebook = source
    else:
        raise ValueError('Invalid input - sould be either Source or Ebook')
    new_name_rel = norm_file_name_base(ebook)
    for ch in [':', '*', '%', '|', '"', '<', '>', '?', '\\']:
        new_name_rel = new_name_rel.replace(ch, '')
    new_name_rel += '.' + ext

    return new_name_rel

def _safe_file_name(name):
    return name.replace('/', '-')


def norm_file_name_base(ebook):
    config = current_app.config
    data = {'author': _safe_file_name(ebook.authors_str),
            'title': _safe_file_name(ebook.title),
            'language': ebook.language.code,
            }
    if ebook.series:
        data.update({'serie': _safe_file_name(ebook.series.title),
                    'serie_index': ebook.series_index or 0})
    if ebook.series and config.get('BOOKS_FILE_SCHEMA_SERIE'):
        new_name_rel = config.get('BOOKS_FILE_SCHEMA_SERIE') % data
        # TODO: might need to spplit base part
    else:
        new_name_rel = config.get('BOOKS_FILE_SCHEMA') % data
    new_name_rel = remove_diacritics(new_name_rel)
    assert(len(new_name_rel) < 4096)
    return new_name_rel


def stream_response(fname, mimetype, headers={}):
    def stream_file(f):
        buf_size = 8192
        try:
            while True:
                data = f.read(buf_size)
                if not data:
                    break
                yield data
        finally:
            f.close()

    try:
        outfile = open(fname, 'rb')
    except IOError as e:
        logger.exception('File %s error %s', fname, e)
        abort(404, 'File not found')

    headers['Content-Length'] = os.stat(fname).st_size
    response = Response(
        stream_file(outfile), mimetype=mimetype, headers=headers)
    return response


def download(id):
    try:
        source = model.Source.query.get(id)
    except NoResultFound:
        abort(404, 'Source not found')
    fname = os.path.join(current_app.config['BOOKS_BASE_DIR'], source.location)

    down_name = norm_file_name(source)
    down_name = os.path.split(down_name)[-1]
    response = stream_response(fname, mimetype=source.format.mime_type,
                               headers={'Content-Disposition': 'attachment; filename="%s"' % down_name})

    return response

def download_converted(conversion):
    
    fname = os.path.join(current_app.config['BOOKS_CONVERTED_DIR'], conversion.location)
    down_name = norm_file_name(conversion.source)
    down_name = os.path.split(fname)[-1]
    down_name = os.path.splitext(down_name)[0]+'.'+conversion.format.extension
    response = stream_response(fname, mimetype=conversion.format.mime_type,
                               headers={'Content-Disposition': 'attachment; filename="%s"' % down_name})

    return response

def download_converted_batch(batch):
    fname = os.path.join(current_app.config['BOOKS_CONVERTED_DIR'], batch.zip_location)
    down_name = batch.name + '.zip'
    return stream_response(fname, mimetype='application/zip', 
                           headers={'Content-Disposition': 'attachment; filename="%s"' % down_name})


def check_file(mime_type, size, hash, extension=None):
    if size > current_app.config['MAX_CONTENT_LENGTH']:
        logger.warn('File too big %d (limit is %d)', size,
                    current_app.config['MAX_CONTENT_LENGTH'])
        return {'error': 'file too big'}
    if not mime_type and extension:
        mime_type = mimetype_from_file_name('x.'+extension) or ''
    t = model.Format.query.filter_by(mime_type=mime_type.lower()).all()
    if not t and extension:
        t = model.Format.query.filter_by(extension=extension).all()
    if not t:
        logger.warn('Unsupported mime type %s ext %s', mime_type, extension)
        return {'error': 'unsupported file type %s, extension %s'%(mime_type, extension)}

    sources = model.Source.query.filter_by(size=size, hash=hash).all()
    if sources:
        logger.warn('File already exists - %s', sources[0])
        return {'error': 'file already exists'}


def check_uploaded_file(mime_type, fname):
    size = os.stat(fname).st_size
    hash = file_hash(fname)
    extension = os.path.splitext(fname)[1]
    if extension:
        extension=extension[1:]
    return check_file(mime_type, size, hash, extension)


def run_query_limited(q):
    return q.count(), q.limit(current_app.config.get('MAX_INDEX_SIZE', 100)).all()


def series_index(start):
    # Need to add authors
    # select distinct series.*, author.id as author_id, author.first_name,
    # author.last_name from series left join ebook on series.id =
    # ebook.series_id join ebook_authors on ebook_authors.ebook_id=ebook.id
    # join author on author.id = ebook_authors.author_id;

    q = model.Series.query
    q = q.filter(func.unaccent(model.Series.title).ilike(
        func.unaccent(start + '%'))).order_by(model.Series.title)
    return run_query_limited(q)


def ebooks_index(start):
    q = model.Ebook.query
    q = q.filter(func.unaccent(model.Ebook.title).ilike(
        func.unaccent(start + '%'))).order_by(model.Ebook.title)
    return run_query_limited(q)

def shelves_index(start, user):
    q = model.Bookshelf.query
    if user:
        q=q.filter(model.Bookshelf.created_by == user)
    else:
        q=q.filter(model.Bookshelf.public == True, model.Bookshelf.created_by != user)
    q = q.filter(func.unaccent(model.Bookshelf.name).ilike(
        func.unaccent(start + '%'))).order_by(model.Bookshelf.name)
    return run_query_limited(q)


def authors_index(start):
    q = model.Author.query
    q = q.filter(func.unaccent(model.Author.last_name + ', ' + model.Author.first_name)
                 .ilike(func.unaccent(start + '%'))).order_by(model.Author.last_name, model.Author.first_name)
    return run_query_limited(q)


def clear_ebook_data(data):
    '''Because of generality of Marshmallow-SqlAlchemy we have to clear 
    input data to prevent unwanted modifications of other entities'''
    EDITABLE = ['id', 'version_id', 'title', 'series_index',
                'language', 'series', 'genres', 'authors']
    if not isinstance(data, dict):
        raise ValueError('Invalid data type')
    tbd = []
    for key in data:
        if not key in EDITABLE:
            tbd.append(key)
    for key in tbd:
        del data[key]

    def shrink(d, id_mandatory=False):
        if not d:
            return None
        if (d.get('id')):
            return {'id': d['id']}
        elif id_mandatory:
            raise ValueError('This entity %s must have id' % d)
        else:
            if 'id' in d:
                del d['id']
            return d

    def shrink_list(l, id_mandatory=False):
        if l is None:
            return []
        if not isinstance(l, list):
            raise ValueError('Value must be list')
        return list(filter(lambda x: x, map(lambda i: shrink(i, id_mandatory), l)))

    if 'language' in data:
        data['language'] = shrink(data['language'], True)
    if 'series' in data:
        data['series'] = shrink(data['series'])
    if 'authors' in data:
        data['authors'] = shrink_list(data['authors'])
    if 'genres' in data:
        data['genres'] = shrink_list(data['genres'], True)

    return data


def check_ebook_entity(ebook, current_user=None):

    def check_entity(entity, query, replace_cb):
        if not inspect(entity).has_identity:
            with db.session.no_autoflush:
                existing = query.first()
            if existing:
                replace_cb(existing)
                if inspect(entity).pending:
                    db.session.expunge(entity)
            else:
                entity.created_by = current_user
                entity.modified_by = current_user

    def replace_series(other):
        ebook.series = other
    if ebook.series:
        check_entity(ebook.series, model.Series.query.filter_by(
            title=ebook.series.title), replace_series)

    for i, author in enumerate(ebook.authors):

        def replace_author(other):
            ebook.authors[i] = other

        check_entity(author,
                     model.Author.query.filter(model.Author.last_name == author.last_name,
                                               model.Author.first_name == author.first_name),
                     replace_author)

    # deduplicate authors
    if len(ebook.authors)>1: 
        duplicates=set()
        
        for i, author in enumerate(ebook.authors):
            dups = list(filter(lambda a: a.last_name == author.last_name and\
                                      a.first_name == author.first_name, ebook.authors[i+1:] ))
            duplicates.update(dups)
            
        for dup in duplicates:
            ebook.authors.remove(dup)
        
def update_ebook_base_dir(ebook):
    ebook.base_dir= os.path.split(norm_file_name(ebook))[0]

def delete_source(source):
    db.session.delete(source)
    db.session.commit()
    full_path = os.path.join(
        current_app.config['BOOKS_BASE_DIR'], source.location)
    try:
        os.remove(full_path)
    except IOError:
        pass
    # do not delete empty directory because of concurrency - other thread, process may use it
    # purging of empty dirs must be done when system is offline
    

def delete_ebook(ebook, keep_cover=False):
    files_to_delete=[os.path.join(current_app.config['BOOKS_BASE_DIR'], source.location)
                     for source in ebook.sources]
    r = db.session.delete(ebook)  # @UndefinedVariable
    if ebook.cover and not keep_cover:
        files_to_delete.append(os.path.join(current_app.config['BOOKS_BASE_DIR'], ebook.cover))
    files_to_delete.append(os.path.join(
            current_app.config['THUMBS_DIR'], '%d.jpg'%ebook.id))
    db.session.commit()
    
    for fname in files_to_delete:
        try:
            os.remove(fname)
        except IOError as e:
            logger.warn('Cannot delete file %s',fname)


def delete_upload(upload):
    dir = os.path.join(
        current_app.config['UPLOAD_DIR'], os.path.split(upload.file)[0])
    shutil.rmtree(dir, ignore_errors=True)
    db.session.delete(upload)
    
def delete_conversion(conversion):
    try:
        os.remove(os.path.join(current_app.config['BOOKS_CONVERTED_DIR'], conversion.location))
    except IOError:
        logger.warn('Conversion file %s cannot be deleted', conversion.location)
    db.session.delete(conversion)
    
def delete_conversion_batch(batch):
    for conv in model.Conversion.query.filter(model.Conversion.batch == batch):
        delete_conversion(conv)
        
    if batch.zip_location:
        try:
          os.remove(os.path.join(current_app.config['BOOKS_CONVERTED_DIR'], batch.zip_location))
        except IOError:
            logger.warn('Conversion batch file %s cannot be deleted', batch.zip_location)  
            
    db.session.delete(batch)
    

def update_cover(upload, ebook, config=None):
    if not config:
        config = current_app.config
    dst_dir = ebook.base_dir #if ebook.base_dir else os.path.split(norm_file_name(ebook))[0]
    cover_file = upload.cover
    ebook_id=ebook.id
    cover_out = copy_cover(cover_file, dst_dir, ebook_id, config)
    ebook.cover = cover_out
        
def query_converted_sources_for_ebook(ebook_id, user=None):
    q = model.Conversion.query.join(model.Conversion.source)\
        .join(model.Source.ebook).filter(model.Ebook.id == ebook_id)
        
    if user:
        q = q.filter(model.Conversion.created_by_id == user.id)
        
    return q.order_by(desc(model.Conversion.created))

def filter_ebooks_by_genres(q,genres):
    return q.join(model.Ebook.genres).filter(model.Genre.id.in_(genres)).group_by(model.Ebook.id)\
            .having(func.count(model.Ebook.id) == len(genres))
    

def merge_ebooks(ebook, other):   
    with db.session.no_autoflush:     
        ebook.sources.extend(list(other.sources))
        other.sources.clear()
        keep_cover= ebook.cover == other.cover
        delete_ebook(other, keep_cover)
        
def merge_shelves(shelf, other):   
    with db.session.no_autoflush:   
        for item in other.items.all():
            if not ((item.ebook and shelf.items.filter(model.BookshelfItem.ebook == item.ebook)).one_or_none() \
                or (item.series and shelf.items.filter(model.BookshelfItem.series == item.series).one_or_none())):
                item.bookshelf = shelf
    db.session.flush()
    db.session.delete(other)  
    db.session.commit()
        
def merge_authors(author, other):
    with db.session.no_autoflush:
        for ebook in other.ebooks:
            ebook.authors.append(author)
            
    db.session.delete(other)
    db.session.commit()
    
def merge_series(series, other):
    model.Ebook.query.filter(model.Ebook.series_id==other.id).update({model.Ebook.series_id: series.id}, 
                                                               synchronize_session=False)
    #db.session.flush()
    db.session.delete(other)
    db.session.commit()
                 
            
def calc_avg_ebook_rating(ebook_id):
    return db.session.query(func.avg(model.EbookRating.rating), func.count(model.EbookRating.id))\
                            .filter(model.EbookRating.ebook_id == ebook_id).one()
    
