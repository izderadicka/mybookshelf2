from flask import Blueprint, request,g, abort, current_app
from flask_restful import Resource as BaseResource, Api
import model
import schema
from utils import paginated, paginate, verify_token


bp=Blueprint('api', __name__)
api=Api(bp)



@bp.before_request
def token_authetication():
    token=request.headers.get('Authorization')
    if token and token.lower().startswith('bearer '):
        token=token[7:].strip()
        claim=verify_token(token, current_app.config['SECRET_KEY'])
        if claim:
            user=model.User.query.get(claim.id)
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
    @paginated(sortings=schema.sortings['ebook'])
    def get(self,page=1, page_size=20, sort=None, **kwargs):
        q=model.Ebook.query
        return paginate(q, page, page_size, sort, schema.ebooks_list_serializer)
    
class Ebook(Resource):
    def get(self, id):
        return schema.ebook_serializer.dump(model.Ebook.query.get(id)).data
        
    
api.add_resource(Ebooks, '/ebooks')
api.add_resource(Ebook, '/ebooks/<int:id>')