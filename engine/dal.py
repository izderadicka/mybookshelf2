import aiopg
from aiopg.sa import create_engine
import settings
import asyncio
import os
import sys
import app.model as model
from sqlalchemy.sql import select, or_, and_, func

DSN = 'dbname={db} user={user} password={password} host={host}'.format(db=settings.DB_NAME,
                                                                       host=settings.DB_HOST,
                                                                       user=settings.DB_USER,
                                                                       password=settings.DB_PASSWORD
                                                                       )


engine = None


def init():
    global engine
    loop = asyncio.get_event_loop()
    engine = loop.run_until_complete(create_engine(DSN, echo=settings.DEBUG))


def close(wait=False):
    engine.close()
    if wait:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(engine.wait_closed())


async def get_user_id(user_email):
    async with engine.acquire() as conn:
        user = model.User.__table__
        res = await conn.execute(select([user.c.id]).where(user.c.email == user_email))
        res = await res.fetchone()
        if res:
            return res[0]
        
async def get_format_id(ext):
    async with engine.acquire() as conn:
        format = model.Format.__table__
        res = await conn.execute(select([format.c.id]).where(format.c.extension == ext))
        res = await res.fetchone()
        if res:
            return res[0]

async def add_upload(fname, cover, meta, size, hash, user_email):
    ext = os.path.splitext(fname)[1].lower()[1:]
    format_id = await get_format_id(ext)
    user_id = await get_user_id(user_email)
    async with engine.acquire() as conn:
        upload = model.Upload.__table__
        source_name = os.path.split(fname)[-1]
        res = await conn.execute(upload.insert().values(file=fname, cover=cover,
                                                        load_source=source_name,
                                                        size=size, hash=hash,
                                                        format_id=format_id,
                                                        version_id=1,
                                                        created_by_id=user_id,
                                                        modified_by_id=user_id,
                                                        meta=meta
                                                        ))
        new_id = (await res.fetchone())[0]
        return new_id

    
async def add_conversion(fname, format, source_id, user_email):
    format_id = await get_format_id(format)
    user_id = await get_user_id(user_email)
    async with engine.acquire() as conn:
        conversion = model.Conversion.__table__
        res = await conn.execute(conversion.insert().values(location=fname,
                                                   format_id=format_id,
                                                   source_id=source_id,
                                                   created_by_id=user_id,
                                                   modified_by_id=user_id,
                                                   version_id=1
                                                   ))
        new_id = (await res.fetchone())[0]
        return new_id
    

async def find_author(ain):
    async with engine.acquire() as conn:
        author = model.Author.__table__
        if ain.get('first_name'):
            where = and_(author.c.first_name == ain[
                         'first_name'], author.c.last_name == ain['last_name'])
        else:
            where = and_(
                author.c.last_name == ain['last_name'], author.c.first_name == None)

        res = await conn.execute(select([author.c.id, author.c.first_name, author.c.last_name]).where(where))
        a = await res.fetchone()
        if a:
            ao = {'id': a[0], 'last_name': a[2]}
            if a[1]:
                ao['first_name'] = a[1]

            return ao

async def find_series(ser):
    async with engine.acquire() as conn:
        series = model.Series.__table__
        res = await conn.execute(select([series.c.id, series.c.title]).where(func.lower(series.c.title) == ser['title'].lower()))
        s = await res.fetchone()
        if s:
            return {'id': s[0], 'title': s[1]}

async def find_synonym(name, what):
    async with engine.acquire() as conn:
         synonym = model.Synonym.__table__
         res=await conn.execute(select([synonym.c.our_name]).where(and_(func.lower(synonym.c.other_name) == name.lower(), 
                                                                   synonym.c.category == what)))
         s = await res.fetchone()
         if s: return s[0]
        
async def find_language(lang):
    async with engine.acquire() as conn:
        language = model.Language.__table__
        async def fl(where):
            res = await conn.execute(select([language.c.id, language.c.code, language.c.name]).where(where))
            l= await res.fetchone()
            if l:
                return {'id':l[0], 'code':l[1], 'name':l[2]}
        l=None
        if lang.get('code'):
            l = await fl(language.c.code == lang['code'])
            if not l:
                code = await find_synonym(lang['code'], model.Synonym.LANGUAGE_CODE)
                if code:
                    l = await fl(language.c.code == code)
        
        if not l and lang.get('name'):
            l = await fl(func.lower(language.c.name) == lang['name'].lower())
            if not l:
                name = await find_synonym(lang['name'], model.Synonym.LANGUAGE_NAME)
                if name:
                    l = await fl(language.c.name == name)
                    
        return l
                

async def find_genre(gnr):
    async with engine.acquire() as conn:
        genre = model.Genre.__table__
        async def fg(name):
            res = await conn.execute(select([genre.c.id, genre.c.name]).where(func.lower(genre.c.name) == name.lower()))
            g = await res.fetchone()
            if g:
                return {'id':g[0], 'name':g[1]}
            
        ng =  await fg(gnr['name'])
        if not ng:
            name = await find_synonym(gnr['name'], model.Synonym.GENRE)
            if name:
                ng = await fg(name)
                
        return ng
    

async def get_source_file(id):
    async with engine.acquire() as conn:
        source=model.Source.__table__
        format=model.Format.__table__
        res = await conn.execute(select([source.c.location, format.c.extension]).select_from(source.join(format)).where(source.c.id==id))
        res = await res.fetchone()
        if res:
            return res.as_tuple()
        else:
            return None,None
        
async def get_meta(source_id):
    async with engine.acquire() as conn:
        source = model.Source.__table__
        ebook = model.Ebook.__table__
        author = model.Author.__table__
        genre = model.Genre.__table__
        language = model.Language.__table__
        series = model.Series.__table__
        
        res = await conn.execute(select([source.c.ebook_id]).where(source.c.id==source_id))
        res = await res.fetchone()
        if not res:
            return
        ebook_id=res[0]
        res = await conn.execute(select([ebook.c.title, language.c.code, series.c.title, ebook.c.series_index, ebook.c.cover])\
                           .select_from(ebook.join(language).outerjoin(series)).where(ebook.c.id == ebook_id))

        res = await res.fetchone()
        
        if not res:
            return
        
        meta = {'title': res[0], 'language': res[1]}
        if res [2]:
            meta['series'] = res[2]
            meta['series-index'] = res[3] or 0
        if res[4]:
            meta['cover']= os.path.join(settings.BOOKS_BASE_DIR, res[4])
            
        res = await conn.execute(select([author.c.first_name, author.c.last_name]).select_from(author.join(model.ebook_authors))\
                                 .where(model.ebook_authors.c.ebook_id == ebook_id))
        res = await res.fetchall()
        
        authors = ' & '.join(map(lambda r: r[0]+' '+r[1] if r[0] else r[1], res))
        if authors:
            meta['authors'] = authors
            
        res = await conn.execute(select([genre.c.name]).select_from(genre.join(model.ebook_genres))\
                                 .where(model.ebook_genres.c.ebook_id == ebook_id))
        res = await res.fetchall()
        
        genres = ', '.join(map(lambda r: r[0], res))
        if genres:
            meta['tags'] = genres
            
        return meta
    

        