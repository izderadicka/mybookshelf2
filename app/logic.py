from flask import abort, request, current_app, Response, jsonify
from sqlalchemy.sql import text, desc, func
from functools import wraps
from app import db
import app.model as model
import app.schema as schema
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm import aliased
from sqlalchemy import inspect
from common.utils import remove_diacritics, file_hash, copy_cover
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


def paginated(default_page_size=10, max_page_size=100, sortings=None):
    def wrapper(fn):
        @wraps(fn)
        def inner(*args, **kwargs):
            page_size = safe_int(
                request.args.get('page_size'), 'page_size') or default_page_size
            if page_size > max_page_size:
                abort(400, 'Page size bigger then maximum')
            kwargs['page_size'] = page_size
            kwargs['page'] = safe_int(request.args.get('page'), 'page') or 1
            sort_in = request.args.get('sort')
            if sortings:
                sort = sortings.get(sort_in)
                if sort_in and not sort:
                    abort(400, 'Invalid sort key %s' % sort_in)
                kwargs['sort'] = sortings.get(request.args.get('sort'))
            else:
                if sort_in:
                    abort(400, 'Sorting not supported')
            return fn(*args, **kwargs)
        return inner
    return wrapper


def paginate(q, page, page_size, sort, serializer):
    if sort:
        q = q.order_by(*sort)
    pager = q.paginate(page, page_size)
    return {'page': pager.page,
            'page_size': pager.per_page,
            'total': pager.total,
            'items': serializer.dump(pager.items).data}


def create_new_location(source, upload):
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
        # TODO: consider copy for better safety?
        shutil.move(new_file, os.path.join(base_dir, new_location))

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


def norm_file_name_base(ebook):
    config = current_app.config
    data = {'author': ebook.authors_str,
            'title': ebook.title,
            'language': ebook.language.code,
            }
    if ebook.series:
        data.update({'serie': ebook.series.title,
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
    down_name = os.path.split(fname)[-1]
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


def check_file(mime_type, size, hash):
    if size > current_app.config['MAX_CONTENT_LENGTH']:
        logger.warn('File too big %d (limit is %d)', size,
                    current_app.config['MAX_CONTENT_LENGTH'])
        return {'error': 'file too big'}

    t = model.Format.query.filter_by(mime_type=mime_type.lower()).all()
    if not t:
        logger.warn('Unsupported mime type %s', mime_type)
        return {'error': 'unsupported file type'}

    sources = model.Source.query.filter_by(size=size, hash=hash).all()
    if sources:
        logger.warn('File already exists - %s', sources[0])
        return {'error': 'file already exists'}


def check_uploaded_file(mime_type, fname):
    size = os.stat(fname).st_size
    hash = file_hash(fname)
    return check_file(mime_type, size, hash)


def _run_query(q):
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
    count = q.count()
    q = q.limit(current_app.config.get('MAX_INDEX_SIZE', 100)).subquery(
        'series_view')
    q = aliased(model.Series, q)
    session_author = db.session.query(q, model.Author).outerjoin(model.Ebook).join(
        model.Ebook.authors).order_by(q.title, model.Author.id).all()
    res = []
    current = None
    for series, author in session_author:
        if series == current:
            series.authors.append(author)
        else:
            current = series
            res.append(series)
            series.authors = [author] if author else []
    return count, res


def ebooks_index(start):
    q = model.Ebook.query
    q = q.filter(func.unaccent(model.Ebook.title).ilike(
        func.unaccent(start + '%'))).order_by(model.Ebook.title)
    return _run_query(q)


def authors_index(start):
    q = model.Author.query
    q = q.filter(func.unaccent(model.Author.last_name + ', ' + model.Author.first_name)
                 .ilike(func.unaccent(start + '%'))).order_by(model.Author.last_name, model.Author.first_name)
    return _run_query(q)


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
    

def delete_ebook(ebook):
    files_to_delete=[os.path.join(current_app.config['BOOKS_BASE_DIR'], source.location)
                     for source in ebook.sources]
    r = db.session.delete(ebook)  # @UndefinedVariable
    if ebook.cover:
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
    

def merge_ebook(ebook, other):   
    with db.session.no_autoflush:     
        for s in other.sources:
            other.sources.remove(s)
            ebook.sources.append(s)
            
        delete_ebook(other)
    
