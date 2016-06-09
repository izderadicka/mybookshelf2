from flask import Blueprint, request, abort, current_app, jsonify
from flask_restful import Resource as BaseResource, Api
import app.model as model
import app.schema as schema
import app.logic as logic
from app.utils import success_error
from app import db
from app.cors import add_cors_headers
from app.access import role_required
from werkzeug import secure_filename
import os.path
import logging
import tempfile

logger = logging.getLogger('api')


bp = Blueprint('api', __name__)
api = Api(bp)


@bp.after_request
def after_request(response):
    return add_cors_headers(response)


class Resource(BaseResource):
    decorators = [role_required('user')]
    pass


class Ebooks(Resource):

    @logic.paginated(sortings=model.sortings['ebook'])
    def get(self, page=1, page_size=20, sort=None, **kwargs):
        q = model.Ebook.query
        return logic.paginate(q, page, page_size, sort, schema.ebooks_list_serializer())

    def post(self):
        pass


class Authors(Resource):

    @logic.paginated(sortings=model.sortings['author'])
    def get(self, page=1, page_size=20, sort=None, **kwargs):
        q = model.Author.query
        return logic.paginate(q, page, page_size, sort, schema.authors_list_serializer())


class Series(Resource):

    @logic.paginated(sortings=model.sortings['series'])
    def get(self, page=1, page_size=20, sort=None, **kwargs):
        q = model.Series.query
        return logic.paginate(q, page, page_size, sort, schema.series_list_serializer())


class Ebook(Resource):

    def get(self, id):
        b = model.Ebook.query.get_or_404(id)
        return schema.ebook_serializer().dump(b).data  # @UndefinedVariable

    @role_required('superuser')
    def delete(self, id):
        b = model.Ebook.query.get_or_404(id)
        r = db.session.delete(b)  # @UndefinedVariable
        db.session.commit()

    def put(self, id):
        pass


class Author(Resource):

    def get(self, id):
        a = model.Author.query.get_or_404(id)
        return schema.author_serializer().dump(a).data


class Search(Resource):

    @logic.paginated()
    def get(self, search, page=1, page_size=20, **kwargs):
        q = logic.search_query(model.Ebook.query, search)
        return logic.paginate(q, page, page_size, None, schema.ebooks_list_serializer())


class AuthorEbooks(Resource):

    @logic.paginated(sortings=model.sortings['ebook'])
    def get(self, id, page=1, page_size=20, sort=None):
        q = model.Ebook.query.join(
            model.Author, model.Ebook.authors).filter(model.Author.id == id)
        if request.args.get('filter'):
            q = logic.filter_ebooks(q, request.args.get('filter'))
        return logic.paginate(q, page, page_size, sort, schema.ebooks_list_serializer())


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


@bp.route('/upload/check', methods=['POST'])
@role_required('user')
def check_upload():
    file_info = request.json
    logger.debug('File info %s' % file_info)
    err = schema.FileInfoSchema().validate(file_info)
    print(err, file_info)
    if err:
        logger.warn('Invalid file info: %s', err)
        return jsonify(error='Invalid schema')
    r = logic.check_file(**file_info)
    if r:
        return jsonify(**r)
    return jsonify(result='ok')


@bp.route('/download/<int:id>')
@role_required('user')
def download(id):
    return logic.download(id)

api.add_resource(Ebooks, '/ebooks')
api.add_resource(Ebook, '/ebooks/<int:id>')
api.add_resource(AuthorEbooks, '/ebooks/author/<int:id>')
api.add_resource(Authors, '/authors')
api.add_resource(Author, '/authors/<int:id>')
api.add_resource(Series, '/series')
api.add_resource(Search, '/search/<string:search>')
