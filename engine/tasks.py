import os.path
import re
import asyncio
from asexor.task import BaseTask, TaskError
from settings import UPLOAD_DIR, IMAGE_MAGIC, THUMBNAIL_SIZE, OOFFICE, CONVERSION_FORMATS, CONVERTABLE_TYPES,\
    BOOKS_CONVERTED_DIR, BOOKS_BASE_DIR, CALIBRE_META_TOOL, CALIBRE_CONVERT_TOOL
from common.utils import file_hash, parse_author
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
    cmd=(OOFFICE, '--headless', '--convert-to', format,'--outdir', outdir, fname)
    proc = await asyncio.create_subprocess_exec(*cmd)
    return_code = await proc.wait()
    #older version of LibreOffice are returning non return code even if file is created
    if await aos.path.exists(out_file):
        return out_file
    else:
        logger.error('Failed %s with code %d',' '.join(cmd), return_code)
    
class MetadataTask(BaseTask):
    NAME = 'metadata'
    COMMAND = CALIBRE_META_TOOL
    MAX_TIME = 60

    async def validate_args(self, *args, **kwargs):
        f = args[0]
        self.proposed_meta = args[1] if len(args)>1 else {}
        fname = os.path.join(UPLOAD_DIR, f)
        ext = os.path.splitext(fname)[1].lower()
        self.file_ext = ext
        self.tmp_name = None
        if ext == '.doc':
            self.tmp_name = await convert_file(fname, 'odt')
        self.base_dir = os.path.split(f)[0]
        self.cover_name = os.path.join(self.base_dir, 'cover_tmp.jpg')
        if not os.access(fname, os.R_OK):
            raise TaskError('File %s does not exists or is not readable', fname)
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
            authors = re.sub(r'\[[^\]]+\]', '', authors.group(1))
            authors = map(parse_author, strip(authors.split('&')))
            meta['authors'] = authors
            

        tags = self.TAGS_RE.search(data)
        if tags:
            genres = strip(tags.group(1).split(','))
            meta['genres'] = list(map(lambda x: {'name': x}, genres))
            

        languages = self.LANGUAGES_RE.search(data)
        if languages:
            meta['language'] = {'code': languages.group(1).split(',')[0].strip()}

        series = self.SERIES_RE.search(data)
        if series:
            series_re = re.match(r'(.*) #(\d+)', series.group(1))
            if series_re:
                meta['series'] = {'title': series_re.group(1)}
                meta['series_index'] = int(series_re.group(2))
                
        #Check against DB
        meta.update(self.proposed_meta)
        
        if 'authors' in meta:
            final_authors = []
            for a in meta['authors']:
                na = await dal.find_author(a)
                final_authors.append(na or a)
            meta['authors'] = final_authors
            
        if 'genres' in meta:
            final_genres = []
            for g in meta['genres']:
                ng = await dal.find_genre(g)
                final_genres.append(ng or g)
            meta['genres'] = final_genres
            
        if 'language' in meta:
            nl = await dal.find_language(meta['language'])
            if nl: meta['language'] = nl
            
        if 'series' in meta:
            ns = await dal.find_series(meta['series'])
            if ns: meta['series'] = ns 
            
        return meta
        

    async def parse_result(self, data):

        data = data.decode(self.output_encoding)
        meta = await self._parse_data(data)
        if self.tmp_name:
            await aos.remove(self.tmp_name)
            
        
        #meta for doc files are not reliable - replace them with extracted from file name
        if self.file_ext == '.doc' and not 'title' in (self.proposed_meta or {}):
            meta ={'title' : os.path.splitext(os.path.basename(self.fname))[0]}
            if self.proposed_meta and 'quality' in self.proposed_meta:
                meta['quality'] = self.proposed_meta['quality']
        
        
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
    COMMAND = CALIBRE_CONVERT_TOOL
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
        
        self.user_id = await dal.get_user_id(self.user)
        
        if not self.user_id:
            raise TaskError('Uknown user')
        
        if format not in CONVERTABLE_TYPES:
            raise TaskError('Cannot convert from format %s' % format)
        
        
        
        if to_format not in CONVERSION_FORMATS:
            raise TaskError('Not supported target format %s', to_format)
        
        conv_id = await dal.get_conversion_id(source_id, self.user_id, to_format)
        if conv_id:
            raise TaskError('This conversion already exists under id %d'%conv_id)
        
        self.out_file =  os.path.splitext(source_file)[0]+'.'+to_format
        self.out_file_full = os.path.join(BOOKS_CONVERTED_DIR, str(self.user_id), self.out_file)
        
#         if await aos.path.exists(self.out_file_full):
#             raise TaskError('File already exists')
        
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
                params.extend(['--'+key, str(meta[key]) ])    
    
    async def parse_result(self, data): 
        if not (await aos.path.exists(self.out_file_full)):
            raise TaskError('Converted file does not exists')
        if self.tmp_file:
            try:
                await aos.remove(self.tmp_file)
            except IOError:
                pass
        
        conversion_id = await dal.add_conversion(os.path.join(str(self.user_id),self.out_file), 
                                                 self.to_format, 
                                                 self.source_id, 
                                                 self.user)
        return conversion_id
        
    
