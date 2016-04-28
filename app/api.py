from flask import Blueprint, request,g, abort, current_app
from flask_restful import Resource as BaseResource, Api
import app.model as model
import app.schema as schema
from app.utils import paginated, paginate, verify_token, success_error


bp=Blueprint('api', __name__)
api=Api(bp)
schema


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

def authenticated(fn):
    def inner(*args, **kwargs):
        if not hasattr(g, 'authenticated') or not g.authenticated:
            abort(401, 'Access denied')
        return fn(*args, **kwargs)
    return inner    

class Resource(BaseResource):
    decorators=[authenticated]
    pass

    
class Ebooks(Resource): 
    @paginated(sortings=model.sortings['ebook'])
    def get(self,page=1, page_size=20, sort=None, **kwargs):
        q=model.Ebook.query
        return paginate(q, page, page_size, sort, schema.ebooks_list_serializer())
    
    def post(self):
        pass
    
class Authors(Resource):
    @paginated(sortings=model.sortings['author'])
    def get(self,page=1, page_size=20, sort=None, **kwargs):
        q=model.Author.query
        return paginate(q, page, page_size, sort, schema.authors_list_serializer())
    
class Ebook(Resource):
    def get(self, id):
        return schema.ebook_serializer().dump(model.Ebook.query.get(id)).data  # @UndefinedVariable
    
    @success_error
    def delete(self, id):
        model.Ebook.delete(id)
        
    def put(self,id):
        pass
    
        
    
api.add_resource(Ebooks, '/ebooks')
api.add_resource(Ebook, '/ebooks/<int:id>')