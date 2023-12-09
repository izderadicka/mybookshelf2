import argparse
from requests.packages.urllib3.util import Retry
from requests.adapters import HTTPAdapter
from requests import Session as HTTPSession, exceptions
import os.path
from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import sys
import settings
import json
import logging
import tempfile
from urllib.parse import  urlsplit, urlunsplit
from time import sleep
from requests.exceptions import RetryError

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import app.model as model

log=logging.getLogger()
logging.basicConfig(level=logging.DEBUG)

def response_ok(res):
    return res.status_code == 200 and res.headers['Content-type'].startswith('image')

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--delay', default=1, type=float, help="delay between requests")
    opts=p.parse_args()
    
    
    engine = create_engine(settings.SQLALCHEMY_DATABASE_URI)
    Session = sessionmaker(bind=engine)
    session = Session()
    
    http = HTTPSession()
    http.adapters.clear()
    http.mount('http', HTTPAdapter(
    max_retries=Retry(total=5, status_forcelist=[500])
    )
)
    
    ebooks = session.query(model.Ebook).filter(model.Ebook.cover == None).order_by(desc(model.Ebook.id))
    
    for ebook in ebooks:
        print(ebook)
        search_string = ' '.join(map(lambda a: a.first_name + ' ' + a.last_name if a.first_name else a.last_name, 
                                     ebook.authors[:1]))
        search_string += ' ' + ebook.title
        
        try:
            resp=http.get('http://www.databazeknih.cz/suggest_new.php', params={'q': search_string}, timeout=5)
                    
            #print(resp.status_code,resp.headers['Content-type'],resp.text)
            try:
                data = json.loads(resp.text[1:-1])
            except Exception as e:
                log.error('JSON error: %s',e)
                continue
            data = list(filter(lambda x: x['druh'] == 'kniha', data))
            if data:
                picture_url = data[0].get('picture')
                if picture_url:
                    url_parsed = urlsplit(picture_url)
                    path,fname = os.path.split(url_parsed.path)
                    fname='big_'+fname
                    os.path.join(path, fname)
                    big_picture_url =  urlunsplit((url_parsed[0], url_parsed[1], os.path.join(path, fname),
                                                   url_parsed[3], url_parsed[4]))
                    
                    res = http.get(big_picture_url)
                    
                    if not response_ok(res):
                        res = http.get(picture_url)
                        
                    if not response_ok(res):
                        log.warn('Cannot get picture for %s', ebook)
                        continue
                    else:
                        temp_dir = tempfile.mkdtemp(dir=settings.UPLOAD_DIR)
                        image_type=res.headers['Content-type']
                        out_file = os.path.join(temp_dir, 'cover.jpg')
                        with open(out_file, 'wb') as f:
                            f.write(res.content)
                        log.debug('Written cover from %s to %s', res.url, out_file)
        except RetryError:
            log.error('Retry error for ebook %s', ebook)
            continue
        sleep(opts.delay)
    
if __name__=='__main__':
    main()