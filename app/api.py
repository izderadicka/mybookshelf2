from flask import Blueprint, request, abort, current_app, jsonify, json
from flask_restful import Resource as BaseResource, Api
from flask_login import current_user
import app.model as model
import app.schema as schema
import app.logic as logic
from common.utils import success_error, mimetype_from_file_name, ext_from_mimetype
from app import db
from functools import wraps
from app.cors import add_cors_headers
from app.access import role_required, can_change_object
from werkzeug import secure_filename
import os.path
import logging
import tempfile
from time import sleep

logger = logging.getLogger('api')


bp = Blueprint('api', __name__)
api = Api(bp)


@bp.after_request
def after_request(response):
    if current_app.config.get('DISABLE_CORS'):
        return response
    else:
        return add_cors_headers(response)
    
def paginated(default_page_size=10, max_page_size=100, sortings=None):
    def wrapper(fn):
        @wraps(fn)
        def inner(*args, **kwargs):
            page_size = logic.safe_int(
                request.args.get('page_size'), 'page_size') or default_page_size
            if page_size > max_page_size:
                abort(400, 'Page size bigger then maximum')
            kwargs['page_size'] = page_size
            kwargs['page'] = logic.safe_int(request.args.get('page'), 'page') or 1
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


class Resource(BaseResource):
    decorators = [role_required('user')]
    SCHEMA = None
    
    @property
    def model(self):
        return self.SCHEMA.Meta.model

class InsertListMixin():
    
    def clear_insert_data(self):
        return request.json
    
    def modify_insert_object(self, obj):
        pass
    
    def post(self):
        if not request.json:
            abort(400)

        try:
            data = self.clear_insert_data()
        except ValueError as e:
            db.session.rollback()
            return jsonify(error="Invalid data", error_details=str(e))

        deserializer = self.SCHEMA.create_insert_serializer()
        obj, errors = deserializer.load(data)

        if errors:
            db.session.rollback()
            return jsonify(error="Invalid data", error_details=errors)

        obj.created_by = current_user
        obj.modified_by = current_user
        
        self.modify_insert_object(obj)

        db.session.add(obj)

        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return jsonify(error="Database error", error_details=str(e))

        return jsonify(id=obj.id, success=True)
    
    
    def get(self):
        q = self.filter_list(self.model.query)
        serializer = self.SCHEMA.create_list_serializer()
        
        if self.paginated is not None:
            return paginated(**self.paginated)(paginate)(q=q, serializer=serializer)
        else:
            return serializer.dump(q.all()).data
        
    def filter_list(self,q):
        return q
    
class UpdateGetDeleteMixin():
    def get(self, id): 
        b = self.model.query.get_or_404(id)
        return self.SCHEMA.create_entity_serializer().dump(b).data
    
        

#############################################################################################
# API RESOURCES
#############################################################################################

class Ebooks(Resource, InsertListMixin):
    methods=['GET', 'POST']
    SCHEMA =  schema.EbookSchema
    paginated = {'sortings':model.sortings['ebook']}
    
    def filter_list(self, q):
        genres=request.args.get('genres')
        if genres:
            genres=list(map(int,  genres.split(',')))
        if genres:
            q= logic.filter_ebooks_by_genres(q, genres)
            
        return q
    
    # Create post 
    
    def clear_insert_data(self):
        return logic.clear_ebook_data(request.json)
    
    def modify_insert_object(self, ebook):
        logic.check_ebook_entity(ebook, current_user)
        logic.update_ebook_base_dir(ebook)
    # end create post
    

class Authors(Resource):

    @paginated(sortings=model.sortings['author'])
    def get(self, page=1, page_size=20, sort=None, **kwargs):
        q = model.Author.query
        return paginate(q, page, page_size, sort, schema.authors_list_serializer())


class Languages(Resource):

    def get(self):
        q = model.Language.query.order_by(model.Language.name)
        return schema.languages_list_serializer().dump(q.all()).data


class Genres(Resource):

    def get(self):
        q = model.Genre.query.order_by(model.Genre.name)
        return schema.languages_list_serializer().dump(q.all()).data


class Series(Resource):

    @paginated(sortings=model.sortings['series'])
    def get(self, page=1, page_size=20, sort=None, **kwargs):
        q = model.Series.query
        return paginate(q, page, page_size, sort, schema.series_list_serializer())


class Serie(Resource):

    def get(self, id):
        s = model.Series.query.get_or_404(id)
        return schema.series_serializer().dump(s).data


class Ebook(Resource):

    def get(self, id):
        b = model.Ebook.query.get_or_404(id)
        return schema.ebook_serializer().dump(b).data  # @UndefinedVariable

    def delete(self, id):
        # check access - superuser or owner
        b = model.Ebook.query.get_or_404(id)
        can_change_object(b)
        logic.delete_ebook(b)
        #TODO: delete sources files!
        return jsonify(id=id, success=True)

    def patch(self, id):
        if not request.json:
            abort(400)

        try:
            data = logic.clear_ebook_data(request.json)
        except ValueError as e:
            db.session.rollback()
            return jsonify(error="Invalid data", error_details=str(e))

        deserializer = schema.ebook_deserializer_update()

        data['id'] = int(id)

        try:
            version_id = int(data.pop('version_id'))
        except (KeyError,ValueError):
            db.session.rollback()
            return jsonify(error="Version_id missing", error_details="")

        ebook, errors = deserializer.load(data)

        if ebook.id != data['id']:
            db.session.rollback()
            return jsonify(error="Unknown record", error_details="Id %d is not in table" % data['id'])

        can_change_object(ebook)

        if version_id != ebook.version_id:
            db.session.rollback()
            return jsonify(error="Stalled record",  error_details="Your version %d, db version %d" %
                           (version_id, ebook.version_id))
        if errors:
            db.session.rollback()
            return jsonify(error="Invalid data", error_details=errors)

        ebook.modified_by = current_user
        logic.check_ebook_entity(ebook, current_user)

        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return jsonify(error="Database error", error_details=str(e))

        return jsonify(id=ebook.id, success=True)


class Author(Resource):

    def get(self, id):
        a = model.Author.query.get_or_404(id)
        return schema.author_serializer().dump(a).data


class Search(Resource):

    @paginated()
    def get(self, search, page=1, page_size=20, **kwargs):
        q = logic.search_query(model.Ebook.query, search)
        return paginate(q, page, page_size, None, schema.EbookSchema.create_list_serializer())


class AuthorEbooks(Resource):

    @paginated(sortings=model.sortings['ebook'])
    def get(self, id, page=1, page_size=20, sort=None):
        q = model.Ebook.query.join(
            model.Author, model.Ebook.authors).filter(model.Author.id == id)
        if request.args.get('filter'):
            q = logic.filter_ebooks(q, request.args.get('filter'))
        return paginate(q, page, page_size, sort, schema.EbookSchema.create_list_serializer())
    
class BookShelves(Resource, InsertListMixin):
    methods=['GET', 'POST']
    SCHEMA =  schema.BookshelfSchema
    paginated = {'sortings': model.sortings['shelf']}
       
    def filter_list(self, q):
        if request.args.get('filter'):
            q = logic.filter_shelves(q, request.args.get('filter'))
        return q 
    
    

    
class BookShelf(Resource, UpdateGetDeleteMixin):
    methods=['GET']
    SCHEMA = schema.BookshelfSchema
    
        

class SeriesEbooks(Resource):
    @paginated(sortings=model.sortings['ebook_in_series'])
    def get(self, id, page=1, page_size=20, sort=None):
        q=model.Ebook.query.filter(model.Ebook.series_id == id)
        return paginate(q, page, page_size, sort, schema.EbookSchema.create_list_serializer())


class UploadMeta(Resource):

    def get(self, id):
        upload = model.Upload.query.get_or_404(id)
        data = schema.upload_serializer().dump(upload).data
        return data
    
class Source(Resource): 
    
    def delete(self,id):
        source= model.Source.query.get_or_404(id)
        can_change_object(source)
        logic.delete_source(source)
        return jsonify(id=id, success=True)
        
        


###################################################################################################
# API SPECIAL METHODS
###################################################################################################

@bp.route('/upload', methods=['POST'])
@role_required('user')
def upload():
    file = request.files['file']
    if file:
        filename = secure_filename(file.filename)
        temp_dir = tempfile.mkdtemp(dir=current_app.config['UPLOAD_DIR'])
        tdir = os.path.split(temp_dir)[1]
        full_name = os.path.join(temp_dir, filename)
        file.save(full_name)
        result = logic.check_uploaded_file(file.mimetype, full_name)
        if result:
            os.remove(full_name)
            return jsonify(**result)
        return jsonify(result='ok', file=os.path.join(tdir, filename))
    return jsonify(error='no file')

@bp.route('/upload-cover', methods=['POST'])
@role_required('user')
def upload_cover():
    file=request.files['file']
    if file:
        
        if not file.mimetype.startswith('image/'):
            return jsonify(error='Invalid file type %s'%file.mimetype)
        if file.content_length > current_app.config['MAX_COVER_FILE_SIZE']:
            return jsonify(error='File too big (%d)'%file.content_length)
        filename = 'cover_in'+ext_from_mimetype(file.mimetype)
        temp_dir = tempfile.mkdtemp(dir=current_app.config['UPLOAD_DIR'])
        tdir = os.path.split(temp_dir)[1]
        ext=os.path.split
        full_name = os.path.join(temp_dir, filename)
        file.save(full_name)
        return jsonify(result='ok', file=os.path.join(tdir, filename))
        


@bp.route('/upload/check', methods=['POST'])
@role_required('user')
def check_upload():
    file_info = request.json
    logger.debug('File info %s' % file_info)
    err = schema.FileInfoSchema().validate(file_info)
    #print(err, file_info)
    if err:
        logger.warn('Invalid file info: %s', err)
        abort(400,'Invalid schema')
    r = logic.check_file(**file_info)
    if r:
        return jsonify(**r)
    return jsonify(result='ok')


@bp.route('/download/<int:id>')
@role_required('user')
def download(id):
    return logic.download(id)

@bp.route('/download-converted/<int:id>')
@role_required('user')
def download_converted(id):
    conversion = model.Conversion.query.get_or_404(id)
    if conversion.created_by != current_user:
        abort(403, 'No Access')
    return logic.download_converted(conversion)


@bp.route('/uploads-meta/<int:id>/cover')
@role_required('user')
def cover_meta(id, size='normal'):
    upload = model.Upload.query.get_or_404(id)
    if not upload.cover:
        logger.warn('Upload cover for %d is empty', id)
        abort(404, 'No cover')

    fname = os.path.join(current_app.config['UPLOAD_DIR'], upload.cover)
    mimetype = mimetype_from_file_name(fname)
    if not mimetype:
        abort(500, 'Invalid cover file')

    return logic.stream_response(fname, mimetype)

@bp.route('/ebooks/<int:id>/cover')
@role_required('user')
def cover_ebook(id, size='normal'):
    ebook = model.Ebook.query.get_or_404(id)
    if not ebook.cover:
        abort(404, 'No cover')

    fname = os.path.join(current_app.config['BOOKS_BASE_DIR'], ebook.cover)
    mimetype = mimetype_from_file_name(fname)
    if not mimetype:
        abort(500, 'Invalid cover file')
    return logic.stream_response(fname, mimetype)


@bp.route('/series/index/<string:start>')
@role_required('user')
def series_index(start):
    total, items = logic.series_index(start)
    serializer = schema.series_index_serializer()
    return jsonify(total=total,
                   items=serializer.dump(items).data)


@bp.route('/authors/index/<string:start>')
@role_required('user')
def authors_index(start):
    total, items = logic.authors_index(start)
    serializer = schema.authors_list_serializer()
    return jsonify(total=total,
                   items=serializer.dump(items).data)


@bp.route('/ebooks/index/<string:start>')
@role_required('user')
def ebooks_index(start):
    total, items = logic.ebooks_index(start)
    serializer = schema.EbookSchema.create_list_serializer()
    return jsonify(total=total,
                   items=serializer.dump(items).data)


@bp.route('/ebooks/<int:id>/add-upload', methods=['POST'])
@role_required('user')
def add_upload_to_ebook(id):
    data = request.json
    if not data.get('upload_id'):
        abort(400, 'Invalid request')
    upload_id = int(data['upload_id'])
    ebook = model.Ebook.query.get_or_404(id)
    upload = model.Upload.query.get_or_404(upload_id)
    quality = data.get('quality')
    quality = float(quality) if quality is not None else None
    existing = model.Source.query.filter_by(
        hash=upload.hash, size=upload.size).first()
    if existing:
        return jsonify(error="File already exists", error_details="Existing source %d in ebook %s(%d)" %
                       (existing.id, existing.ebook.title, existing.ebook.id))

    source = model.Source(ebook=ebook,
                          format=upload.format,
                          size=upload.size,
                          hash=upload.hash,
                          quality=quality,
                          load_source=upload.load_source
                          )
    source.location = logic.create_new_location(source, upload)
    source.created_by= current_user
    source.modified_by = current_user
    db.session.add(source)
     #cover
    if upload.cover and not ebook.cover:
        logic.update_cover(upload, ebook)
        
    logic.delete_upload(upload)
   
        
    db.session.commit()

    return jsonify(id=source.id)

@bp.route('/ebooks/<int:ebook_id>/converted') 
@role_required('user')
def converted_sources(ebook_id):
    q = logic.query_converted_sources_for_ebook(ebook_id, current_user)
    serializer = schema.conversions_list_serializer()
    return jsonify( total=q.count(), items=serializer.dump(q.limit(100).all()).data)

@bp.route('/ebooks/<int:ebook_id>/merge', methods=['POST'])
@role_required('superuser')
def merge_ebook(ebook_id):
    data=request.json
    if not data['other_ebook']:
        abort(400, 'Invalid Request')
    ebook = model.Ebook.query.get_or_404(ebook_id)
    other = model.Ebook.query.get_or_404(data['other_ebook'])    
    logic.merge_ebook(ebook, other)
    return jsonify(id=ebook_id)

@bp.route('/bookshelves/<int:shelf_id>/add', methods=['POST'])
@role_required('user')
def add_ebook_to_shelf(shelf_id):
    data = request.json
    bookshelf = model.Bookshelf.query.get_or_404(shelf_id)
    if 'ebook_id' in data:
        bookshelf.add_ebook(data['ebook_id'], current_user, data.get('note'), data.get('order'))
    elif 'series_id' in data:
        bookshelf.add_series(data['series_id'])
    else:
        abort(400, 'Invalid request')
        
    db.session.commit()
    
    return jsonify(id=shelf_id)
        
    
    
    
    


api.add_resource(Ebooks, '/ebooks')
api.add_resource(BookShelves, '/bookshelves')
api.add_resource(BookShelf, '/bookshelves/<int:id>')
api.add_resource(Ebook, '/ebooks/<int:id>')
api.add_resource(Source, '/sources/<int:id>')
api.add_resource(AuthorEbooks, '/ebooks/author/<int:id>')
api.add_resource(SeriesEbooks, '/ebooks/series/<int:id>')
api.add_resource(Authors, '/authors')
api.add_resource(Author, '/authors/<int:id>')
api.add_resource(Series, '/series')
api.add_resource(Serie, '/series/<int:id>')
api.add_resource(Search, '/search/<string:search>')
api.add_resource(UploadMeta, '/uploads-meta/<int:id>')
api.add_resource(Languages, '/languages')
api.add_resource(Genres, '/genres')
