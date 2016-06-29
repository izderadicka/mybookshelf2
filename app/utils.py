from functools import wraps
import bcrypt
import jwt
from datetime import datetime, timedelta
import unicodedata
import hashlib
import logging
import mimetypes

logger = logging.getLogger('utils')


def mimetype_from_file_name(fname):
    return mimetypes.guess_type(fname, False)[0]


def success_error(fn):
    @wraps(fn)
    def inner(*args, **kwargs):
        try:
            fn(*args, **kwargs)
            return {'success': True}
        except Exception as e:
            return {'error': str(e)}
    return inner

READ_BLOCK = 8192


def file_hash(fname):
    h = hashlib.sha1()
    with open(fname, 'rb') as f:
        s = f.read(READ_BLOCK)
        if not s:
            raise ValueError("Empty file!")
        while s:
            h.update(s)
            s = f.read(READ_BLOCK)
    return h.hexdigest()


def hash_pwd(p):
    if isinstance(p, str):
        p = p.encode('utf-8')
    return bcrypt.hashpw(p, bcrypt.gensalt()).decode('ascii')


def check_pwd(p, hash):
    if isinstance(p, str):
        p = p.encode('utf-8')
    if isinstance(hash, str):
        hash = hash.encode('ascii')
    return hash == bcrypt.hashpw(p, hash)


def create_token(user, secret, valid_minutes=24 * 60):
    token = jwt.encode({'id': user.id,
                           'user_name': user.user_name,
                           'email': user.email,
                           'roles':  list(user.all_roles),
                           'exp': datetime.utcnow() + timedelta(hours=valid_minutes)}, secret, algorithm='HS256')
    
    return token.decode('ascii')


def verify_token(token, secret):
    try:
        token = token.encode('ascii')
    except UnicodeEncodeError:
        logger.exception('Invalid token - char encoding')
        return
    try:
        claim = jwt.decode(token, secret)
    except jwt.InvalidTokenError:
        logger.exception('Invalid token')
        return None
    return claim


def extract_token(token):
    try:
        return jwt.decode(token, verify=False)
    except jwt.InvalidTokenError as e:
        raise ValueError('Invalid token %s' % e)


def initials(name):
    names = name.split()
    return ' '.join(map(lambda n: n[0].upper(), names))

nd_charmap = {
    u'\N{Latin capital letter AE}': 'AE',
    u'\N{Latin small letter ae}': 'ae',
    u'\N{Latin capital letter Eth}': 'D',
    u'\N{Latin small letter eth}': 'd',
    u'\N{Latin capital letter O with stroke}': 'O',
    u'\N{Latin small letter o with stroke}': 'o',  #
    u'\N{Latin capital letter Thorn}': 'Th',
    u'\N{Latin small letter thorn}': 'th',
    u'\N{Latin small letter sharp s}': 's',
    u'\N{Latin capital letter D with stroke}': 'D',
    u'\N{Latin small letter d with stroke}': 'd',
    u'\N{Latin capital letter H with stroke}': 'H',
    u'\N{Latin small letter h with stroke}': 'h',
    u'\N{Latin small letter dotless i}': 'i',
    u'\N{Latin small letter kra}': 'k',
    u'\N{Latin capital letter L with stroke}': 'L',
    u'\N{Latin small letter l with stroke}': 'l',
    u'\N{Latin capital letter Eng}': 'N',
    u'\N{Latin small letter eng}': 'n',
    u'\N{Latin capital ligature OE}': 'Oe',
    u'\N{Latin small ligature oe}': 'oe',
    u'\N{Latin capital letter T with stroke}': 'T',
    u'\N{Latin small letter t with stroke}': 't',
}


def remove_diacritics(text):
    "Removes diacritics from the string"
    if not text:
        return text
    s = unicodedata.normalize('NFKD', text)
    b = []
    for ch in s:
        if unicodedata.category(ch) != 'Mn':
            if ch in nd_charmap:
                b.append(nd_charmap[ch])
            elif ord(ch) < 128:
                b.append(ch)
            else:
                b.append(' ')
    return ''.join(b)
