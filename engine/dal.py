import aiopg
from aiopg.sa import create_engine
import settings
import asyncio
import os
import sys
import app.model as model
from psycopg2.extras import Json
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
    engine = loop.run_until_complete(create_engine(DSN))


def close(wait=False):
    engine.close()
    if wait:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(engine.wait_closed())


async def add_upload(fname, cover, meta, size, hash, user_email):
    async with engine.acquire() as conn:
        format = model.Format.__table__
        ext = os.path.splitext(fname)[1].lower()[1:]
        res = await conn.execute(select([format.c.id]).where(format.c.extension == ext))
        format_id = (await res.fetchone())[0]
        user = model.User.__table__
        res = await conn.execute(select([user.c.id]).where(user.c.email == user_email))
        user_id = (await res.fetchone())[0]
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
        res = await conn.execute(select([series.c.id, series.c.title]).where(series.c.title == ser['title']))
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
