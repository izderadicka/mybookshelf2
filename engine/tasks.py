import os.path
import re
import asyncio
from asexor.task import BaseTask, TaskError
from settings import UPLOAD_DIR, IMAGE_MAGIC
from app.utils import file_hash
import logging
import engine.dal as dal

logger = logging.getLogger('tasks')


class MetadataTask(BaseTask):
    NAME = 'metadata'
    COMMAND = 'ebook-meta'
    MAX_TIME = 60

    async def validate_args(self, *args, **kwargs):
        f = args[0]
        fname = os.path.join(UPLOAD_DIR, f)
        base_name = os.path.splitext(f)[0]
        self.cover_name = base_name + '_tmp.jpg'
        if not os.access(fname, os.R_OK):
            raise TaskError('File %s does not exists or is not readable')
        self.fname = f
        self.fname_full = fname
        return ('--get-cover=%s' % os.path.join(UPLOAD_DIR, self.cover_name), fname)

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
            meta['authors'] = strip(authors.split('&'))

        tags = self.TAGS_RE.search(data)
        if tags:
            meta['tags'] = strip(tags.group(1).split(','))

        languages = self.LANGUAGES_RE.search(data)
        if languages:
            meta['language'] = languages.group(1).split(',')[0].strip()

        series = self.SERIES_RE.search(data)
        if series:
            series = re.match(r'(.*) #(\d+)', series.group(1))
            if series:
                meta['series'] = series.group(1)
                meta['series_index'] = int(series.group(2))

        return meta

    async def parse_result(self, data):

        data = data.decode(self.output_encoding)
        meta = await self._parse_data(data)
        
        cover_in = os.path.join(UPLOAD_DIR, self.cover_name)
        loop = asyncio.get_event_loop()
        hash = await loop.run_in_executor(None, file_hash, self.fname_full)
        size = await loop.run_in_executor(None, lambda f: os.stat(f).st_size, self.fname_full)
        cover = None
        if os.path.exists(cover_in):
            cover_file = self.cover_name[:-8] + '_cover.jpg'
            cover_file_full = os.path.join(UPLOAD_DIR, cover_file)

            proc = await asyncio.create_subprocess_exec(IMAGE_MAGIC, cover_in, '-fuzz', '7%',
                                                        '-trim', cover_file_full)
            return_code = await proc.wait()

            if return_code == 0 and os.path.exists(cover_file_full):
                os.remove(cover_in)
            else:
                logger.warn(
                    'Image Magic failed triming file %s with code %d', cover_in, return_code)
                os.rename(cover_in, cover_file_full)
            cover = cover_file
        else:
            logger.warn('Cannot get cover image')
        
        upload_id = await dal.add_upload(self.fname, cover, meta, size, hash, self.user)
        
        return upload_id
