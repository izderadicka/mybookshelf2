from flask import Blueprint, request,g, abort, current_app
from flask_restful import Resource as BaseResource, Api
import app.model as model
import app.schema as schema
import app.logic as logic
from app.utils import verify_token, success_error
from app import db
from app.cors import add_cors_headers
from functools import wraps




bp=Blueprint('api', __name__)
api=Api(bp)



@bp.before_request
def token_authetication():
    token=request.headers.get('Authorization')
    if token and token.lower().startswith('bearer '):
        token=token[7:].strip()
        claim=verify_token(token, current_app.config['SECRET_KEY'])
        if claim:
            user=model.User.query.get(claim['id'])  # @UndefinedVariable
            if user and user.is_active:
                g.authenticated=True
                g.user=user
                
@bp.after_request
def after_request(response):
    return add_cors_headers(response)

def authenticated(fn):
    @wraps(fn)
    def inner(*args, **kwargs):
        if not hasattr(g, 'authenticated') or not g.authenticated:
            abort(401, 'Access denied')
        return fn(*args, **kwargs)
    return inner  

def has_role(role): 
    def wrapper(fn):
        @wraps(fn)
        def inner(*args,**kwargs):
            if not g.user.has_role(role):
                abort(401, 'Access denied')
            return fn(*args, **kwargs)
        return inner
    return wrapper

class Resource(BaseResource):
    decorators=[authenticated]
    pass

    
class Ebooks(Resource): 
    @logic.paginated(sortings=model.sortings['ebook'])
    def get(self,page=1, page_size=20, sort=None, **kwargs):
        q=model.Ebook.query
        return logic.paginate(q, page, page_size, sort, schema.ebooks_list_serializer())
    
    def post(self):
        pass
    
class Authors(Resource):
    @logic.paginated(sortings=model.sortings['author'])
    def get(self,page=1, page_size=20, sort=None, **kwargs):
        q=model.Author.query
        return logic.paginate(q, page, page_size, sort, schema.authors_list_serializer())
    
class Series(Resource):
    @logic.paginated(sortings=model.sortings['series'])
    def get(self,page=1, page_size=20, sort=None, **kwargs):
        q=model.Series.query
        return logic.paginate(q, page, page_size, sort, schema.series_list_serializer())
    
class Ebook(Resource):
    def get(self, id):
        return schema.ebook_serializer().dump(model.Ebook.query.get(id)).data  # @UndefinedVariable
    
    @has_role('admin')
    @success_error
    def delete(self, id):
        db.session.delete(model.Ebook.query.get(id))  # @UndefinedVariable
        
    def put(self,id):
        pass

class Author(Resource):
    def get(self, id):
        return schema.author_serializer().dump(model.Author.query.get(id)).data
    
class Search(Resource):
    @logic.paginated()
    def get(self, search, page=1, page_size=20, **kwargs):
        q=logic.search_query(model.Ebook.query, search)
        return logic.paginate(q,page, page_size, None, schema.ebooks_list_serializer())
        
        
class AuthorEbooks(Resource): 
    @logic.paginated(sortings=model.sortings['ebook'])
    def get(self, id, page=1, page_size=20, sort=None ):
        q=model.Ebook.query.join(model.Author, model.Ebook.authors).filter(model.Author.id ==id)
        if request.args.get('filter'):
            q=logic.filter_ebooks(q, request.args.get('filter'))
        return logic.paginate(q,page,page_size,sort, schema.ebooks_list_serializer())
        

    
        
    
api.add_resource(Ebooks, '/ebooks')
api.add_resource(Ebook, '/ebooks/<int:id>')
api.add_resource(AuthorEbooks, '/ebooks/author/<int:id>')
api.add_resource(Authors, '/authors')
api.add_resource(Author, '/authors/<int:id>')
api.add_resource(Series, '/series')
api.add_resource(Search, '/search/<string:search>')