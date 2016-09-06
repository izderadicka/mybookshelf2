from cli.action import Action, ActionError
from app.utils import file_hash, parse_author
from mimetypes import guess_type
import os


class Upload(Action):
    
    @staticmethod
    def add_arguments(parser):
        parser.add_argument('--file', type=str, required=True, help = "ebook file")
        parser.add_argument('--title', help='title')
        parser.add_argument('--author', nargs='*', help="author written as Last, First (can have many authors)" )
        parser.add_argument('--series', help='series title')
        parser.add_argument('--series-index', type=int, help='book index in series ')
        parser.add_argument('--genre', nargs='*', help='genre (can have many genres')
        parser.add_argument('--language', help='language code like cs, en ...')
        parser.add_argument('--quality', type=float, help='Quality of file 0 - 100 (spelling, pictures, formating, but not literal quality/popularity of book')
        
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
        
        if self.opts.quality:
            meta['quality'] = self.opts.quality
            
        return meta
        
    def do(self):
        def check_response(res):
            res.raise_for_status()
            res = res.json()
            if 'error' in res:
                raise ActionError('Cannot upload file: %s'%res['error'])
            return res
            
        fname = self.opts.file
        if not (os.access(fname, os.R_OK) and os.path.isfile(fname)):
            raise ActionError('File %s does not exists or is not readable'%fname)
        file_info = {'size': os.stat(fname).st_size,
                     'hash': file_hash(fname),
                     'mime_type': guess_type(fname)[0]}
        res=self.http.post('/api/upload/check', json=file_info)
        res = check_response(res)
        
        res = self.http.post('/api/upload', files={'file':(os.path.basename(fname), open(fname, 'rb'), file_info['mime_type'])})
        res = check_response(res)
            
        
        
        uploaded_file = res['file']
        proposed_meta = self._get_meta()
        res = self.client.call('metadata', uploaded_file, proposed_meta)
        upload_meta_id = res['result']
        
        res = self.http.get('/api/uploads-meta/%d'%upload_meta_id)
        res = check_response(res)
        meta = res['meta']
        
        
        print(meta)
        
        
        
         