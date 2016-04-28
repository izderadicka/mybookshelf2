from flask import request, abort
from functools import wraps
import bcrypt
import jwt
from datetime import datetime, timedelta

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

def success_error(fn):
    @wraps(fn)
    def inner(*args,**kwargs):
        try:
            fn(*args, **kwargs)
            return {'success':True}
        except Exception as e:
            return {'error':str(e)}
    return inner

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
            sort=sortings.get(sort_in)
            if sort_in and not sort:
                abort(400, 'Invalid sort key %s'%sort_in)
            kwargs['sort']=sortings.get(request.args.get('sort'))
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
    
def hash_pwd(p):
    if isinstance(p, str):
        p=p.encode('utf-8')
    return bcrypt.hashpw(p, bcrypt.gensalt()).decode('ascii')

def check_pwd(p, hash):
    if isinstance(p, str):
        p=p.encode('utf-8')
    if isinstance(hash, str):
        hash=hash.encode('ascii')
    return hash == bcrypt.hashpw(p, hash)

def create_token(user, secret, valid_minutes=24*60): 
    return jwt.encode({'id': user.id,
                       'user_name' : user.user_name,
                       'email': user.email,
                       'roles': list(map(lambda r: r.name, user.roles)),
                       'exp': datetime.utcnow()+timedelta(hours=valid_minutes)}, secret, algorithm='HS256')

def verify_token(token, secret):
    try:
        claim=jwt.decode(token, secret)
    except jwt.InvalidTokenError:
        return None
    return claim

        
    
    