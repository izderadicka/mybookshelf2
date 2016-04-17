from flask import request
from functools import wraps

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