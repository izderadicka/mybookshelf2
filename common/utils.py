from functools import wraps
import bcrypt
import jwt
from datetime import datetime, timedelta
import unicodedata
import hashlib
import logging
import mimetypes
import os.path
import shutil

logger = logging.getLogger('utils')

def deep_get(d,k, default=None): 
    parts=k.split('.')
    for k in parts:
        if isinstance(d, dict):
            d= d.get(k)
        else:
            return default
        
    return d or default
    
def mimetype_from_file_name(fname):
    return mimetypes.guess_type(fname, False)[0]

def ext_from_mimetype(mimetype):
    return mimetypes.guess_extension(mimetype)


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


def create_token(user, secret, valid_hours=24):
    token = jwt.encode({'id': user.id,
                           'user_name': user.user_name,
                           'email': user.email,
                           'roles':  list(user.all_roles),
                           'exp': datetime.utcnow() + timedelta(hours=valid_hours)}, secret, algorithm='HS256')
    
    return token.decode('ascii')

def create_refresh_token(user, secret, valid_hours=24):
    token = jwt.encode({'id': user.id,
                        'exp': datetime.utcnow() + timedelta(hours=valid_hours)}, secret, algorithm='HS256')
    
    return token.decode('ascii') 


def verify_token(token, secret, validate_expiration=True):
    try:
        token = token.encode('ascii')
    except UnicodeEncodeError:
        logger.exception('Invalid token - char encoding')
        return
    try:
        claim = jwt.decode(token, secret, options={'verify_exp': validate_expiration})
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

def purge_empty_dirs(path, delete_root=True):
    for f in os.listdir(path):
        full_path = os.path.join(path,f)
        if os.path.isdir(full_path):
            purge_empty_dirs(full_path)
    if delete_root and not os.listdir(path):
        os.rmdir(path)
        
def strip(l):
    return list(map(lambda x: x.strip(), filter(None, l)))
        
def parse_author(author):
    parts = author.split(',')
    if len(parts) > 1:
        return {'last_name': parts[0], 'first_name': ' '.join(map(lambda x: x.strip(),parts[1:]))}
    parts = list(
        filter(lambda i: i, map(lambda i: i.strip(), author.split(' '))))
    a = {'last_name': parts[-1]}
    if len(parts) > 1:
        a['first_name'] = ' '.join(parts[:-1])
    return a

def copy_cover(cover_file, dst_dir, ebook_id, config):
    src = os.path.join(config['UPLOAD_DIR'], cover_file)
    cover_out = os.path.join(dst_dir, os.path.split(cover_file)[1])
    dst = os.path.join(
        config['BOOKS_BASE_DIR'], cover_out)
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    shutil.copy(src, dst)
    
    thumb = config['THUMBNAIL_FILE']
    thumb_file = os.path.join(os.path.split(cover_file)[0], thumb)
    src = os.path.join(config['UPLOAD_DIR'], thumb_file)
    if os.access(src, os.R_OK):
        dst = os.path.join(
            config['THUMBS_DIR'], '%d.jpg'%ebook_id)
        shutil.copy(src, dst)
    return cover_out

def lev_i(a,b):
    if a:
        a=a.lower()
    if b:
        b=b.lower()
        
    return lev(a,b)

def lev(a,b):
    """ Calculates edit (Levenshtein) distance between two strings 
    """
    
    n, m = len(a), len(b)
    if n > m:
        # Make sure n <= m, to use O(min(n,m)) space
        a,b = b,a
        n,m = m,n
      
    current = range(n+1)
    for i in range(1,m+1):
        previous, current = current, [i]+[0]*n
        for j in range(1,n+1):
            add, delete = previous[j]+1, current[j-1]+1
            change = previous[j-1]
            if a[j-1] != b[i-1]:
                change = change + 1
            current[j] = min(add, delete, change)
            
    return current[n]

def damlev_i(a,b):
    if a:
        a=a.lower()
    if b:
        b=b.lower()
        
    return damlev(a,b)
    
def damlev(seq1, seq2):
    """Calculate the Damerau-Levenshtein distance between sequences.

    This distance is the number of additions, deletions, substitutions,
    and transpositions needed to transform the first sequence into the
    second. Although generally used with strings, any sequences of
    comparable objects will work.

    Transpositions are exchanges of *consecutive* characters; all other
    operations are self-explanatory.

    This implementation is O(N*M) time and O(M) space, for N and M the
    lengths of the two sequences.

    >>> dameraulevenshtein('ba', 'abc')
    2
    >>> dameraulevenshtein('fee', 'deed')
    2

    It works with arbitrary sequences too:
    >>> dameraulevenshtein('abcd', ['b', 'a', 'c', 'd', 'e'])
    2
    """
    # codesnippet:D0DE4716-B6E6-4161-9219-2903BF8F547F
    # Conceptually, this is based on a len(seq1) + 1 * len(seq2) + 1 matrix.
    # However, only the current and two previous rows are needed at once,
    # so we only store those.
    oneago = None
    thisrow = list(range(1, len(seq2) + 1)) + [0]
    for x in range(len(seq1)):
        # Python lists wrap around for negative indices, so put the
        # leftmost column at the *end* of the list. This matches with
        # the zero-indexed strings and saves extra calculation.
        twoago, oneago, thisrow = oneago, thisrow, [0] * len(seq2) + [x + 1]
        for y in range(len(seq2)):
            delcost = oneago[y] + 1
            addcost = thisrow[y - 1] + 1
            subcost = oneago[y - 1] + (seq1[x] != seq2[y])
            thisrow[y] = min(delcost, addcost, subcost)
            # This block deals with transpositions
            if (x > 0 and y > 0 and seq1[x] == seq2[y - 1]
                and seq1[x-1] == seq2[y] and seq1[x] != seq2[y]):
                thisrow[y] = min(thisrow[y], twoago[y - 2] + 1)
    return thisrow[len(seq2) - 1]

