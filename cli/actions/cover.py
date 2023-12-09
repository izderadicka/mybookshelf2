from cli.action import Action, ActionError, SoftActionError
import os.path
import mimetypes


class Cover(Action):
    @staticmethod
    def add_arguments(parser):
        parser.add_argument('--file', type=str, required=True, help = "cover image file")
        parser.add_argument('--ebook-id', type=int, required=True, help='ebook id')
        
    def do(self):
        fname = self.opts.file
        if not (os.access(fname, os.R_OK) and os.path.isfile(fname)):
            raise ActionError('File %s does not exists or is not readable'%fname)
        mime = mimetypes.guess_type(fname)[0]
        if not (mime.startswith('image')):
            raise ActionError('File %s is not image'%fname)
        
        try:
            f= open(fname, 'rb')
            res = self.http.post('/api/upload-cover', files={'file':(os.path.basename(fname), f, mime)})
        finally:
            f.close()
            
        res=self.client.call('cover', res['file'], self.opts.ebook_id)
        ebook_id = res['result']
        
        if ebook_id != self.opts.ebook_id:
            raise ActionError('Something went wrongs - ebook ids differs (%d != %d)'%(ebook_id, self.opts.ebook_id))
        
        res = self.http.get('/api/ebooks/%d'%self.opts.ebook_id)
        if not res.get('cover'):
            raise ActionError('Something went wrongs - cover not updated')
        
        
        