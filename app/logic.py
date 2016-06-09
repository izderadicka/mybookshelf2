from flask import abort, request, current_app, Response, jsonify
from sqlalchemy.sql import text, desc, func
from functools import wraps
import app.model as model
import app.schema as schema
from sqlalchemy.orm.exc import NoResultFound
from app.utils import remove_diacritics, file_hash
import os.path

import logging
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
    tokens = text.split()
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


def norm_file_name(source):
    new_name_rel = norm_file_name_base(source.ebook)
    for ch in [':', '*', '%', '|', '"', '<', '>', '?', '\\']:
        new_name_rel = new_name_rel.replace(ch, '')
    new_name_rel += '.' + source.format.extension

    return new_name_rel


def norm_file_name_base(ebook):
    config = current_app.config
    if ebook.series and config.get('BOOKS_FILE_SCHEMA_SERIE'):
        new_name_rel = config.get('BOOKS_FILE_SCHEMA_SERIE') % {'author': ebook.authors_str,
                                                                'title': ebook.title,
                                                                'serie': ebook.series.title,
                                                                'serie_index': ebook.series_index or 0}
        # TODO: might need to spplit base part
    else:
        new_name_rel = config.get('BOOKS_FILE_SCHEMA') % {'author': ebook.authors_str,
                                                          'title': ebook.title}
    new_name_rel = remove_diacritics(new_name_rel)
    assert(len(new_name_rel) < 4096)
    return new_name_rel


def download(id):
    try:
        source = model.Source.query.get(id)
    except NoResultFound:
        abort(404, 'Source not found')
    try:
        fname = os.path.join(
            current_app.config['BOOKS_BASE_DIR'], source.location)
        outfile = open(fname, 'rb')
    except IOError:
        logger.exception('Source file %s error', fname)
        abort(404, 'Source file not found')
    size = os.stat(fname).st_size

    def stream_file(f):
        buf_size = 8192
        while True:
            data = f.read(buf_size)
            if not data:
                break
            yield data
        f.close()

    fname = norm_file_name(source)
    fname = os.path.split(fname)[-1]
    response = Response(stream_file(outfile), mimetype=source.format.mime_type,
                        headers={'Content-Disposition': 'attachment; filename="%s"' % fname,
                                 'Content-Length': size})

    return response


def check_file(mime_type, size, hash):
    if size > current_app.config['MAX_CONTENT_LENGTH']:
        logger.warn('File too big %d (limit is %d)', size,
                    current_app.config['MAX_CONTENT_LENGTH'])
        return {'error':'file too big'}

    t = model.Format.query.filter_by(mime_type=mime_type.lower()).all()
    if not t:
        logger.warn('Unsupported mime type %s', mime_type)
        return {'error':'unsupported file type'}

    sources = model.Source.query.filter_by(size=size, hash=hash).all()
    if sources:
        logger.warn('File already exists - %s', sources[0])
        return {'error':'file already exists'}


def check_uploaded_file(mime_type, fname):
    size = os.stat(fname).st_size
    hash = file_hash(fname)
    return check_file(mime_type, size, hash)