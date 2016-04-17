from flask import Blueprint, request
from flask_restful import Resource, Api
import model
import schema
from utils import paginated

bp=Blueprint('api', __name__)
api=Api(bp)


@bp.before_request
def test():
    print('API request %s'%request)

class Ebooks(Resource): 
    @paginated(sortings=schema.sortings['ebook'])
    def get(self,page=1, page_size=20, sort=None, **kwargs):
        q=model.Ebook.query
        if sort:
            q=q.order_by(*sort)
        page=q.paginate(page,page_size)
        return schema.ebooks_list_serializer.dump(page.items).data
    
class Ebook(Resource):
    def get(self, id):
        return schema.ebook_serializer.dump(model.Ebook.query.get(id)).data
        
    
api.add_resource(Ebooks, '/ebooks')
api.add_resource(Ebook, '/ebooks/<int:id>')