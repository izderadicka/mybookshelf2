import aiopg
from aiopg.sa import create_engine
import settings
import asyncio
import os
import sys
import app.model as model
from psycopg2.extras import Json
from sqlalchemy.sql import select, or_

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
        user =  model.User.__table__
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
