import os.path
import re
import asyncio
from asexor.task import BaseTask, TaskError
from settings import UPLOAD_DIR, IMAGE_MAGIC, THUMBNAIL_SIZE, OOFFICE, CONVERSION_FORMATS, CONVERTABLE_TYPES,\
    BOOKS_CONVERTED_DIR, BOOKS_BASE_DIR
from app.utils import file_hash
import logging
import engine.dal as dal
from .utils import AsyncProxy

aos = AsyncProxy(os)

logger = logging.getLogger('tasks')

#'/usr/bin/soffice --headless --convert-to %(format)s --outdir "%(out_dir)s" "%(in_file)s"'

async def convert_file(fname, format, outdir=None): 
    proc_params = []
    if not outdir:
        outdir=os.path.dirname(fname)
        out_file = os.path.splitext(fname)[0] +'.'+format
    else:
        out_file=os.path.join(outdir, os.path.splitext(os.path.basename(fname))[0]+'.'+format)
    proc = await asyncio.create_subprocess_exec(OOFFICE, '--headless', '--convert-to', 
                                                format,'--outdir', outdir, fname)
    return_code = await proc.wait()
    
    if return_code == 0 and await aos.path.exists(out_file):
        return out_file
    
class MetadataTask(BaseTask):
    NAME = 'metadata'
    COMMAND = 'ebook-meta'
    MAX_TIME = 60

    async def validate_args(self, *args, **kwargs):
        f = args[0]
        fname = os.path.join(UPLOAD_DIR, f)
        ext = os.path.splitext(fname)[1].lower()
        self.file_ext = ext
        self.tmp_name = None
        if ext == '.doc':
            self.tmp_name = await convert_file(fname, 'odt')
        self.base_dir = os.path.split(f)[0]
        self.cover_name = os.path.join(self.base_dir, 'cover_tmp.jpg')
        if not os.access(fname, os.R_OK):
            raise TaskError('File %s does not exists or is not readable')
        self.fname = f
        self.fname_full = fname
        return ('--get-cover=%s' % os.path.join(UPLOAD_DIR, self.cover_name), self.tmp_name or fname)

    AUTHORS_RE = re.compile(
        r'^Author\(s\)\s*:\s*(.+)', re.UNICODE | re.MULTILINE)
    TITLE_RE = re.compile(r'^Title\s*:\s*(.+)', re.UNICODE | re.MULTILINE)
    TAGS_RE = re.compile(r'^Tags\s*:\s*(.+)', re.UNICODE | re.MULTILINE)
    SERIES_RE = re.compile(r'^Series\s*:\s*(.+)', re.UNICODE | re.MULTILINE)
    LANGUAGES_RE = re.compile(
        r'^Languages\s*:\s*(.+)', re.UNICODE | re.MULTILINE)

    async def _parse_data(self, data):
        def strip(l):
            return list(map(lambda x: x.strip(), filter(None, l)))
        meta = {}
        title = self.TITLE_RE.search(data)
        if title:
            meta['title'] = title.group(1).strip()
        authors = self.AUTHORS_RE.search(data)
        if authors:
            def parse_author(author):
                parts = author.split(',')
                if len(parts) > 1:
                    return {'last_name': parts[0], 'first_name': ' '.join(parts[1:])}
                parts = list(
                    filter(lambda i: i, map(lambda i: i.strip(), author.split(' '))))
                a = {'last_name': parts[-1]}
                if len(parts) > 1:
                    a['first_name'] = ' '.join(parts[:-1])
                return a

            authors = re.sub(r'\[[^\]]+\]', '', authors.group(1))
            authors = map(parse_author, strip(authors.split('&')))
            final_authors = []
            for a in authors:
                na = await dal.find_author(a)
                final_authors.append(na or a)
            meta['authors'] = final_authors

        tags = self.TAGS_RE.search(data)
        if tags:
            genres = strip(tags.group(1).split(','))
            final_genres = []
            for g in map(lambda x: {'name': x}, genres):
                ng = await dal.find_genre(g)
                final_genres.append(ng or g)

            meta['genres'] = final_genres

        languages = self.LANGUAGES_RE.search(data)
        if languages:
            l = {'code': languages.group(1).split(',')[0].strip()}
            nl = await dal.find_language(l)
            meta['language'] = nl or l

        series = self.SERIES_RE.search(data)
        if series:
            series_re = re.match(r'(.*) #(\d+)', series.group(1))
            if series_re:
                series = {'title': series_re.group(1)}
                ns = await dal.find_series(series)
                meta['series'] = ns or series
                meta['series_index'] = int(series_re.group(2))

        return meta

    async def parse_result(self, data):

        data = data.decode(self.output_encoding)
        meta = await self._parse_data(data)
        if self.tmp_name:
            await aos.remove(self.tmp_name)
            
        
        #meta for doc files are not reliable - replace them with extracted from file name
        
        if self.file_ext == '.doc':
            meta ={'title' : os.path.splitext(os.path.basename(self.fname))[0]}
        
        
        loop = asyncio.get_event_loop()
        hash = await loop.run_in_executor(None, file_hash, self.fname_full)
        size = await loop.run_in_executor(None, lambda f: os.stat(f).st_size, self.fname_full)
        
        cover_in = os.path.join(UPLOAD_DIR, self.cover_name)
        cover = None
        if await aos.path.exists(cover_in):
            cover_file = os.path.join(self.base_dir, 'cover.jpg')
            cover_file_full = os.path.join(UPLOAD_DIR, cover_file)

            proc = await asyncio.create_subprocess_exec(IMAGE_MAGIC, cover_in, '-fuzz', '7%',
                                                        '-trim', cover_file_full)
            return_code = await proc.wait()

            if return_code == 0 and await aos.path.exists(cover_file_full):
                await aos.remove(cover_in)
            else:
                logger.warn(
                    'Image Magic failed triming file %s with code %d', cover_in, return_code)
                os.rename(cover_in, cover_file_full)
            cover = cover_file
            thumb_out_full = os.path.join(UPLOAD_DIR, self.base_dir, 'thumbnail.jpg')
            proc = await asyncio.create_subprocess_exec(IMAGE_MAGIC, cover_file_full, '-resize', '%dX%d'%THUMBNAIL_SIZE, thumb_out_full)
            return_code = await proc.wait()
            
            if return_code != 0 or not await aos.path.exists(thumb_out_full):
                logger.warn('Error creating thumbnail')
            
        else:
            logger.warn('Cannot get cover image')

        upload_id = await dal.add_upload(self.fname, cover, meta, size, hash, self.user)

        return upload_id

    
class ConvertTask(BaseTask):
    NAME = 'convert'
    COMMAND = 'ebook-convert'
    MAX_TIME = 300
    
    NEED_PRECONVERSION =['doc']
    PRECONVERSION_FORMAT = 'html'
    
    EXTRA_PARAMS_INPUT = {'pdb':['--input-encoding=windows-1250'],
                    'txt':['--input-encoding=windows-1250'],
                    }
    
    EXTRA_PARAMS_OUTPUT = {
                    'epub':['--no-default-epub-cover', '--remove-paragraph-spacing']}
    
    async def validate_args(self, *args, **kwargs):
        source_id= args[0]
        to_format = args[1]
        self.to_format=to_format
        self.source_id=source_id
        
        source_file, format = await dal.get_source_file(source_id)
        if format not in CONVERTABLE_TYPES:
            raise TaskError('Cannot convert from format %s' % format)
        
        
        
        if to_format not in CONVERSION_FORMATS:
            raise TaskError('Not supported target format %s', to_format)
        
        self.out_file = os.path.splitext(source_file)[0]+'.'+to_format
        self.out_file_full = os.path.join(BOOKS_CONVERTED_DIR, self.out_file)
        out_dir = os.path.dirname(self.out_file_full)
        
        await aos.makedirs(out_dir, exist_ok=True)
        
        
        source_file_full = os.path.join(BOOKS_BASE_DIR, source_file)
        
        self.tmp_file = None
        if format in self.NEED_PRECONVERSION:
            outdir = os.path.dirname(self.out_file_full)
            self.tmp_file = await convert_file(source_file_full, self.PRECONVERSION_FORMAT, outdir)
            if not self.tmp_file or not await aos.path.exists(self.tmp_file):
                raise TaskError('Unsuccessful pre conversion of %s'%format)
            
        params = [self.tmp_file or source_file_full, self.out_file_full]
        if format in self.EXTRA_PARAMS_INPUT:
            params.extend(self.EXTRA_PARAMS_INPUT[format])
        if to_format in self.EXTRA_PARAMS_OUTPUT:
            params.extend(self.EXTRA_PARAMS_OUTPUT[to_format])
            
        await self._update_meta(source_id, params)
        return tuple(params)
    
    async def _update_meta(self, source_id, params):
        meta = await dal.get_meta(source_id)
        if meta:
            for key in meta:
                params.extend(['--'+key, meta[key]])

        
        
    
    async def parse_result(self, data): 
        if not (await aos.path.exists(self.out_file_full)):
            raise TaskError('Converted file does not exists')
        
        conversion_id = await dal.add_conversion(self.out_file, self.to_format, self.source_id, self.user)
        return conversion_id
        
    
