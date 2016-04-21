from flask import request
from functools import wraps
import bcrypt
import jwt
from datetime import datetime, timedelta

def safe_int(v):
    if v is None or v=='':
        return
    try:
        return int(v)
    except ValueError:
        pass

def paginated(default_page_size=10, max_page_size=100, sortings=None):
    def wrapper(fn):
        @wraps(fn)
        def inner(*args, **kwargs):
            kwargs['page_size']=min(safe_int(request.args.get('page_size')) or default_page_size, max_page_size)
            kwargs['page']=safe_int(request.args.get('page')) or 1
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

        
    
    