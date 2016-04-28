from functools import wraps
import bcrypt
import jwt
from datetime import datetime, timedelta

def success_error(fn):
    @wraps(fn)
    def inner(*args,**kwargs):
        try:
            fn(*args, **kwargs)
            return {'success':True}
        except Exception as e:
            return {'error':str(e)}
    return inner

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

        
    
    