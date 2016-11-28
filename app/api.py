from flask import Blueprint, request, abort, current_app, jsonify, json
from flask_restful import Resource as BaseResource, Api
from flask_login import current_user
import app.model as model
import app.schema as schema
import app.logic as logic
from common.utils import success_error, mimetype_from_file_name, ext_from_mimetype, deep_get
from app import db
from functools import wraps, partial
from app.cors import add_cors_headers
from app.access import role_required, can_change_object
from werkzeug import secure_filename
import os.path
import logging
import tempfile
from time import sleep
import datetime
import numbers

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
    paginated = None
    
    def clear_insert_data(self, data):
        return data
    
    def modify_insert_object(self, obj):
        pass
    
    def post(self):
        if not request.json:
            abort(400)

        try:
            data = self.clear_insert_data(request.json)
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
    user_can_change = False
    
    def get(self, id): 
        b = self.model.query.get_or_404(id)
        return self.SCHEMA.create_entity_serializer().dump(b).data
    
    def before_delete(self, entity):
        pass
    
    def delete(self, id):
        entity = self.model.query.get_or_404(id)
        if self.user_can_change:
            can_change_object(entity)
        else:
            if not current_user.has_role('superuser'):
                abort(403, 'Access denied')
        self.before_delete(entity)
        db.session.delete(entity)
        db.session.commit()
        return jsonify(id=id, success=True)
    
    def clear_update_data(self, data):
        return data
    
    def modify_update_object(self, obj):
        pass
    
    def patch(self, id):
        if not request.json:
            abort(400)

        try:
            data = self.clear_update_data(request.json)
        except ValueError as e:
            db.session.rollback()
            return jsonify(error="Invalid data", error_details=str(e))

        deserializer = self.SCHEMA.create_update_serializer()

        data['id'] = int(id)

        try:
            version_id = int(data.pop('version_id'))
        except (KeyError,ValueError):
            db.session.rollback()
            return jsonify(error="Version_id missing", error_details="")
        
        existing = self.model.query.filter(self.model.id == data['id']).with_for_update(of=self.model).one()
        if not existing:
            db.session.rollback()
            return jsonify(error="Unknown record", error_details="Id %d is not in table" % data['id'])
        
        obj, errors = deserializer.load(data)
        
        assert(existing.id == obj.id)

        can_change_object(obj)

        if version_id != obj.version_id:
            db.session.rollback()
            return jsonify(error="Stalled record",  error_details="Your version %d, db version %d" %
                           (version_id, obj.version_id))
        if errors:
            db.session.rollback()
            return jsonify(error="Invalid data", error_details=errors)

        obj.modified_by = current_user
        self.modify_update_object(obj)

        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return jsonify(error="Database error", error_details=str(e))

        return jsonify(id=obj.id, success=True)

    
        

#############################################################################################
# API RESOURCES
#############################################################################################

class Author(Resource, UpdateGetDeleteMixin):
    methods = ['GET', 'PATCH']
    SCHEMA = schema.AuthorSchema
    user_can_change = False

class Authors(Resource, InsertListMixin):
    methods = ['GET']
    SCHEMA = schema.AuthorSchema
    paginated = {'sortings': model.sortings['author']}

class BookShelf(Resource, UpdateGetDeleteMixin):
    methods=['GET', 'PATCH', 'DELETE']
    SCHEMA = schema.BookshelfSchema
    
    def get(self, id): 
        b = self.model.query.get_or_404(id)
        if not (b.created_by == current_user or b.public):
            abort(403, 'Access denied')
        return self.SCHEMA.create_entity_serializer().dump(b).data
    
class BookShelfItem(Resource, UpdateGetDeleteMixin):
    methods=['PATCH', 'DELETE']
    SCHEMA = schema.BookshelfItemSchema

    def before_delete(self, item):
        item.bookshelf.modified = datetime.datetime.now()
        
class MyBookShelves(Resource, InsertListMixin):
    methods=['GET', 'POST']
    SCHEMA =  schema.BookshelfSchema
    paginated = {'sortings': model.sortings['bookshelf']}
       
    def filter_list(self, q):
        q = q.filter(model.Bookshelf.created_by == current_user)   
        if request.args.get('filter'):
            q = logic.filter_shelves(q, request.args.get('filter'))
        return q 
    
class OthersBookShelves(Resource, InsertListMixin):
    methods=['GET']
    SCHEMA =  schema.BookshelfSchema
    paginated = {'sortings': model.sortings['bookshelf']}
       
    def filter_list(self, q):
        q = q.filter(model.Bookshelf.created_by != current_user, model.Bookshelf.public == True)   
        if request.args.get('filter'):
            q = logic.filter_shelves(q, request.args.get('filter'))
        return q 

class Ebook(Resource, UpdateGetDeleteMixin):
    methods = ['GET', 'PATCH', 'DELETE']
    SCHEMA = schema.EbookSchema
    user_can_change = True

    def delete(self, id):
        # check access - superuser or owner
        b = model.Ebook.query.get_or_404(id)
        can_change_object(b)
        logic.delete_ebook(b)
        #TODO: delete sources files!
        return jsonify(id=id, success=True)

    def clear_update_data(self, data):
        return logic.clear_ebook_data(request.json)
    
    
    def modify_update_object(self, obj):
            logic.check_ebook_entity(obj, current_user)

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
    
    def clear_insert_data(self, data):
        return logic.clear_ebook_data(data)
    
    def modify_insert_object(self, ebook):
        logic.check_ebook_entity(ebook, current_user)
        logic.update_ebook_base_dir(ebook)
    # end create post
    
class Genres(Resource, InsertListMixin):
    methods = ['GET']
    SCHEMA = schema.GenreSchema
    
    def filter_list(self, q):
        return q.order_by(model.Genre.name)
        
        
class Languages(Resource, InsertListMixin):
    methods = ['GET']
    SCHEMA = schema.LanguageSchema

    def filter_list(self,q):
        return q.order_by(model.Language.name)


class Serie(Resource, UpdateGetDeleteMixin):
    methods = ['GET', 'PATCH']
    SCHEMA = schema.SeriesSchema
    user_can_change = False


class Series(Resource, InsertListMixin):
    methods = ['GET']
    SCHEMA = schema.SeriesSchema
    paginated = {'sortings': model.sortings['series']}
    
    
class Source(Resource): 
    
    def delete(self,id):
        source= model.Source.query.get_or_404(id)
        can_change_object(source)
        logic.delete_source(source)
        return jsonify(id=id, success=True)
    
class UploadMeta(Resource, UpdateGetDeleteMixin):
    methods = ['GET']
    SCHEMA = schema.UploadSchema
    user_can_change = True

    
###################################################################################################
# Special Resources 
###################################################################################################

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
    
        

class SeriesEbooks(Resource):
    @paginated(sortings=model.sortings['ebook_in_series'])
    def get(self, id, page=1, page_size=20, sort=None):
        q=model.Ebook.query.filter(model.Ebook.series_id == id)
        return paginate(q, page, page_size, sort, schema.EbookSchema.create_list_serializer())



###################################################################################################
# API SPECIAL METHODS
###################################################################################################


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


def download(id):
    return logic.download(id)


def download_converted(id):
    conversion = model.Conversion.query.get_or_404(id)
    if conversion.created_by != current_user:
        abort(403, 'No Access')
    return logic.download_converted(conversion)



def cover_meta(id):
    upload = model.Upload.query.get_or_404(id)
    if not upload.cover:
        logger.warn('Upload cover for %d is empty', id)
        abort(404, 'No cover')

    fname = os.path.join(current_app.config['UPLOAD_DIR'], upload.cover)
    mimetype = mimetype_from_file_name(fname)
    if not mimetype:
        abort(500, 'Invalid cover file')

    return logic.stream_response(fname, mimetype)


def cover_ebook(id, size='normal'):
    ebook = model.Ebook.query.get_or_404(id)
    if not ebook.cover:
        abort(404, 'No cover')

    fname = os.path.join(current_app.config['BOOKS_BASE_DIR'], ebook.cover)
    mimetype = mimetype_from_file_name(fname)
    if not mimetype:
        abort(500, 'Invalid cover file')
    return logic.stream_response(fname, mimetype)


def series_index(start):
    total, items = logic.series_index(start)
    serializer = schema.SeriesSchema.create_index_serializer()
    return jsonify(total=total,
                   items=serializer.dump(items).data)


def authors_index(start):
    total, items = logic.authors_index(start)
    serializer = schema.AuthorSchema.create_list_serializer()
    return jsonify(total=total,
                   items=serializer.dump(items).data)


def ebooks_index(start):
    total, items = logic.ebooks_index(start)
    serializer = schema.EbookSchema.create_list_serializer()
    return jsonify(total=total,
                   items=serializer.dump(items).data)
    
def shelves_index(start, mine=True):
    total, items = logic.shelves_index(start, current_user if mine else None)
    serializer = schema.BookshelfSchema.create_index_serializer()
    return jsonify(total=total, items=serializer.dump(items).data)


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


def converted_sources(ebook_id):
    q = logic.query_converted_sources_for_ebook(ebook_id, current_user)
    serializer = schema.ConversionSchema.create_list_serializer()
    return jsonify( total=q.count(), items=serializer.dump(q.limit(100).all()).data)


def merge_ebook(ebook_id):
    data=request.json
    if not data['other_ebook']:
        abort(400, 'Invalid Request')
    ebook = model.Ebook.query.get_or_404(ebook_id)
    other = model.Ebook.query.get_or_404(data['other_ebook'])    
    logic.merge_ebook(ebook, other)
    return jsonify(id=ebook_id)

def add_ebook_to_shelf(shelf_id):
    data = request.json
    bookshelf = model.Bookshelf.query.get_or_404(shelf_id)
    if deep_get(data, 'ebook.id'):
        bookshelf.add_ebook(deep_get(data, 'ebook.id'), current_user, data.get('note'), data.get('order'))
    elif deep_get(data, 'series.id'):
        bookshelf.add_series(data['series']['id'], current_user, data.get('note'), data.get('order'))
    else:
        abort(400, 'Invalid request')
        
    db.session.commit()
    
    return jsonify(id=shelf_id)

@paginated(sortings=model.sortings['bookshelf_item'])
def shelf_items(id, page=1, page_size=20, sort=None):
    b = model.Bookshelf.query.get_or_404(id)
    if not (b.created_by == current_user or b.public):
        abort(403, 'Access denied')
    q = model.BookshelfItem.query.filter(model.BookshelfItem.bookshelf_id == id)
    return jsonify(**paginate(q, page, page_size, sort, schema.BookshelfItemSchema.create_list_serializer()))

def shelves_with_ebook(ebook_id):   
    q = model.Bookshelf.query.join(model.BookshelfItem).filter(model.BookshelfItem.ebook_id == ebook_id)\
    .order_by(model.Bookshelf.public, model.Bookshelf.name)
    q = q.limit(100)
    count,data = logic.run_query_limited(q)
    data = schema.BookshelfSchema.create_index_serializer().dump(data).data
    return jsonify(total = count, items = data)

def rate_ebook(ebook_id): 
    data = request.json
    errors=schema.RatingSchema().validate(data)
    if errors:
        logger.error('Invalid rate request %s', errors)
        abort(400,'Invalid request' )
        
    ebook = model.Ebook.query.get_or_404(ebook_id)
    rating = model.EbookRating.query.filter(model.EbookRating.ebook_id==ebook_id, 
                                            model.EbookRating.created_by == current_user).one_or_none()
                                            
    if  data.get('rating') is None:
        if rating:
            db.session.delete(rating)
    else:    
        ts = datetime.datetime.now()                                        
        if not rating:
            rating = model.EbookRating(created_by=current_user, created = ts, ebook_id = ebook_id)
            db.session.add(rating)
            
        rating.modified_by=current_user
        rating.rating = data['rating']
        if 'description' in data: 
            rating.description = data['description']
        rating.modified = ts
        
    ebook.rating, ebook.rating_count = logic.calc_avg_ebook_rating(ebook_id)
    db.session.commit()
    return jsonify(id=ebook_id, rating=float(ebook.rating) if not ebook.rating is None else None, 
                   rating_count=ebook.rating_count)
    
        
#############################################################################################
# URL mapping
#############################################################################################   

def add_url(view_func, url, roles_required=['user'], **kwargs): 
    if roles_required:
        view_func = role_required(*roles_required)(view_func)
        
    bp.add_url_rule(url, view_func=view_func, **kwargs)
    
api.add_resource(Authors, '/authors')
api.add_resource(Author, '/authors/<int:id>')
add_url(authors_index, '/authors/index/<string:start>')


api.add_resource(MyBookShelves, '/bookshelves/mine')
api.add_resource(OthersBookShelves, '/bookshelves/others')
api.add_resource(BookShelf, '/bookshelves/<int:id>')
add_url(add_ebook_to_shelf, '/bookshelves/<int:shelf_id>/add',  methods=['POST'])
add_url(partial(shelves_index, mine=True), '/bookshelves/mine/index/<string:start>')
add_url(shelf_items, '/bookshelves/<int:id>/items')
api.add_resource(BookShelfItem,'/bookshelf-items/<int:id>')
add_url(shelves_with_ebook, '/bookshelves/with-ebook/<int:ebook_id>')

api.add_resource(Ebooks, '/ebooks')
api.add_resource(Ebook, '/ebooks/<int:id>')
api.add_resource(AuthorEbooks, '/ebooks/author/<int:id>')
api.add_resource(SeriesEbooks, '/ebooks/series/<int:id>')
add_url(cover_ebook, '/ebooks/<int:id>/cover')
add_url(ebooks_index, '/ebooks/index/<string:start>')
add_url(add_upload_to_ebook,'/ebooks/<int:id>/add-upload', methods=['POST'])
add_url(converted_sources, '/ebooks/<int:ebook_id>/converted') 
add_url(merge_ebook, '/ebooks/<int:ebook_id>/merge', methods=['POST'])
add_url(rate_ebook, '/ebooks/<int:ebook_id>/rate', methods=['POST'])

api.add_resource(Genres, '/genres')
api.add_resource(Languages, '/languages')

api.add_resource(Series, '/series')
api.add_resource(Serie, '/series/<int:id>')
add_url(series_index, '/series/index/<string:start>')

api.add_resource(Source, '/sources/<int:id>')

api.add_resource(Search, '/search/<string:search>')

api.add_resource(UploadMeta, '/uploads-meta/<int:id>')
add_url(cover_meta,'/uploads-meta/<int:id>/cover')

add_url(upload, '/upload', methods=['POST'])
add_url(upload_cover, '/upload-cover', methods=['POST'])
add_url(check_upload, '/upload/check', methods=['POST'])

add_url(download,'/download/<int:id>')
add_url(download_converted, '/download-converted/<int:id>')

