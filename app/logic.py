from flask import abort, request
from sqlalchemy.sql import text,desc,func
from functools import wraps
import app.model as model

def safe_int(v, for_=''):
    if v is None or v=='':
        return
    try:
        v= int(v)
        if v<=0:
            abort(400,'Not positive number %s'%for_) 
        return v
    except ValueError:
        abort(400,'Invalid number for %s'%for_)

def preprocess_search_query(text):
    tokens=text.split()
    return ' & '.join(['%s:*'%t for t in tokens])

def search_query(q, search):
    #works only for pg backend
    search=preprocess_search_query(search)
    return q.filter(model.Ebook.full_text.match(search))\
    .order_by(desc(func.ts_rank_cd(model.Ebook.full_text, func.to_tsquery(text("'custom'"), search))))
    
def filter_ebooks(q, filter):
    return q.filter(func.unaccent(model.Ebook.title).ilike(func.unaccent(text("'%%%s%%'"%filter))))
    
def paginated(default_page_size=10, max_page_size=100, sortings=None):
    def wrapper(fn):
        @wraps(fn)
        def inner(*args, **kwargs):
            page_size=safe_int(request.args.get('page_size'),'page_size') or default_page_size
            if page_size>max_page_size:
                abort(400, 'Page size bigger then maximum')
            kwargs['page_size']=page_size
            kwargs['page']=safe_int(request.args.get('page'), 'page') or 1
            sort_in=request.args.get('sort')
            if sortings:
                sort=sortings.get(sort_in)
                if sort_in and not sort:
                    abort(400, 'Invalid sort key %s'%sort_in)
                kwargs['sort']=sortings.get(request.args.get('sort'))
            else:
                if sort_in:
                    abort(400, 'Sorting not supported')
            return fn(*args, **kwargs)
        return inner
    return wrapper

def paginate(q, page, page_size, sort, serializer):
    if sort:
        q=q.order_by(*sort)
    pager=q.paginate(page,page_size)
    return {'page':pager.page,
            'page_size':pager.per_page,
            'total':pager.total,
            'items': serializer.dump(pager.items).data}