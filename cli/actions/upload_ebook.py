from cli.action import Action, ActionError, SoftActionError
from common.utils import file_hash, parse_author
from mimetypes import guess_type
import os
from urllib.parse import urlencode, quote, quote_plus

import logging
import json
from requests.exceptions import HTTPError

log = logging.getLogger('mbs2.upload')


class Upload(Action):
    
    @staticmethod
    def add_arguments(parser):
        parser.add_argument('--file', type=str, required=True, help = "ebook file")
        parser.add_argument('--file-name', help="alternative file name to use for upload")
        parser.add_argument('--title', help='title')
        parser.add_argument('--author', nargs='*', help="author written as Last, First (can have many authors)" )
        parser.add_argument('--series', help='series title')
        parser.add_argument('--series-index', type=int, help='book index in series ')
        parser.add_argument('--genre', nargs='*', help='genre (can have many genres')
        parser.add_argument('--language', help='language code like cs, en ...')
        parser.add_argument('--quality', type=float, help='Quality of file 0 - 100 (spelling, pictures, formating, but not literal quality/popularity of book')
        parser.add_argument('--json', action="store_true", help='Output JSON object representing updated/created ebook after successful upload')
        
    def _get_meta(self):
        meta ={}
        if self.opts.title:
            meta['title'] = self.opts.title
        if self.opts.language:
            meta['language'] = {'code': self.opts.language}
        if self.opts.author:
            meta['authors'] = list(map(parse_author, self.opts.author))
        if self.opts.series and self.opts.series_index is not None:
            meta['series']= {'title': self.opts.series}
            meta['series_index'] = self.opts.series_index
        if self.opts.genre:
            meta['genres'] = list(map(lambda i : {'name': i.strip()}, self.opts.genre))
        
        return meta
        
    def do(self):
        fname = self.opts.file
        alt_name = self.opts.file_name or fname
        if not (os.access(fname, os.R_OK) and os.path.isfile(fname)):
            raise ActionError('File %s does not exists or is not readable'%fname)
        file_info = {'size': os.stat(fname).st_size,
                     'hash': file_hash(fname),
                     'mime_type': guess_type(alt_name)[0] or '',
                     'extension': os.path.splitext(alt_name)[1].lower()[1:] or ''}
        res=self.http.post('/api/upload/check', json=file_info)
        try:
            f= open(fname, 'rb')
            res = self.http.post('/api/upload', files={'file':(os.path.basename(alt_name), f, file_info['mime_type'])})
        finally:
            f.close()
        uploaded_file = res['file']
        log.debug('File uploaded as %s', uploaded_file)
        proposed_meta = self._get_meta()
        res = self.client.call('metadata', uploaded_file, proposed_meta)
        upload_meta_id = res['result']
        
        res = self.http.get('/api/uploads-meta/%d'%upload_meta_id)
        meta = res['meta']
        log.debug('Metadata #%d for ebook - %s', upload_meta_id, meta)
        if not ('title' in meta and meta['title'] and 'language' in meta and meta['language'].get('id')):
            raise ActionError('We need at least title and language')
        search = []
        if meta['authors']:
            search.extend(map(lambda x: x['first_name']+ ' ' + x['last_name'] if 'last_name' in x else x['last_name'], meta['authors']))
        search.append(meta['title'])   
        if 'series' in meta:
            search.append(meta['series']['title'])
            
        search = ' '.join(search)
        
        try:   
            res = self.http.get('/api/search/'+quote_plus(search), params={'page':1, 'page_size':5})
        except HTTPError as e:
            if hasattr(e, 'response') and e.response.status_code == 404:
                res ={}
            else:
                raise e
            
        log.debug('search results %s', res)
        if not res.get('items'):
            res = self.http.get('/api/ebooks/index/'+quote_plus(meta['title']))
            
            
        book_id=None
        
        
        if 'items' in  res and res['items']:
            
            #
            book_id = res['items'][0]['id']
            
            
            
            res = self.http.post('/api/ebooks/%d/add-upload'%(book_id,), json={'upload_id':upload_meta_id, 'quality':self.opts.quality})
            log.info('Added file to existing ebook #%d', book_id)  
        else:
            res = self.http.post('/api/ebooks', json = meta)
            book_id = res['id']
            res = self.http.post('/api/ebooks/%d/add-upload'%(book_id,), json={'upload_id':upload_meta_id, 'quality':self.opts.quality})
            log.info('Added file to new ebook #%d', book_id)  
            
        if self.opts.json:
            res=self.http.get('/api/ebooks/%d'%book_id)
            print(json.dumps(res))
        
        
        
        
         