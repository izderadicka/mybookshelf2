from urllib.parse import urlsplit
from flask import current_app, request, make_response
from functools import wraps

def check_cors(origin):
    url=urlsplit(origin)
    if current_app.config.get('CORS_SECURE'):
        if url.scheme!='https':
            return False
        
    hp=url.netloc.split(':')
    host=hp[0]
    port=int(hp[1]) if len(hp)>1 else 443 if url.scheme == 'https' else 80
    
    if current_app.config.get('CORS_HOSTS') != '*' and host not in current_app.config.get('CORS_HOSTS', []):
        return False
    allowed_ports=current_app.config.get('CORS_PORTS')
    if allowed_ports and isinstance(allowed_ports, tuple) and (port < allowed_ports[0] or\
        port > allowed_ports[1]):
        return False
    elif allowed_ports and isinstance(allowed_ports, list) and port not in allowed_ports:
        return False
        
    return True

def add_cors_headers(response):
    origin=request.headers.get('Origin')
    if origin and check_cors(origin):
        response.headers.add('Access-Control-Allow-Origin', origin)
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,PATCH')
        response.headers.add('Vary', 'Origin')
    return response


def cors_enabled(fn):
    fn.required_methods = getattr(fn, 'required_methods', set())
    fn.required_methods.add('OPTIONS')
    fn.provide_automatic_options = False
    @wraps(fn)
    def inner(*args, **kwargs):
        if request.method=='OPTIONS':
            resp=current_app.make_default_options_response()
        else:
            resp=fn(*args,**kwargs)
            resp=make_response(resp)
        return add_cors_headers(resp)
    return inner
        
