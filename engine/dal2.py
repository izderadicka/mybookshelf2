import aiopg
import aiopg.sa
import settings
import asyncio
import os
import sys

DSN = 'dbname={db} user={user} password={password} host={host}'.format(db=settings.DB_NAME,
                                                                       host=settings.DB_HOST,
                                                                       user=settings.DB_USER,
                                                                       password=settings.DB_PASSWORD
                                                                       )


pool = None


def init():
    global pool
    loop = asyncio.get_event_loop()
    pool = loop.run_until_complete(aiopg.create_pool(DSN))


def close(wait=False):
    pool.terminate()
    if wait:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(pool.wait_closed())


if __name__ == '__main__':
    print (sys.version)
    init()
    assert pool
    async def do():
        async with pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute('select * from format')
                async for row in cur:
                    print(row)
                
    loop=asyncio.get_event_loop()
    loop.run_until_complete(do())
    
    close()