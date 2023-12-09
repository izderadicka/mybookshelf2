import logging
import sys
import os
import asyncio
from asyncio import get_event_loop, set_event_loop
import threading
from asexor.ws_client import AsexorClient
from asexor.raw_client import DelegatedRawSocketAsexorClient
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

log = logging.getLogger('client')

MAX_TIMEOUT = 300
WAIT_TIMEOUT = 10


client_thread = None
def run_loop_in_thread(loop):
    global client_thread
    def _run_loop(loop):
        set_event_loop(loop)
        loop.run_forever()
        
    client_thread = threading.Thread(
            target= _run_loop , name='WAMP Thread', args=(loop,))
    client_thread.daemon = True
    client_thread.start()
    
def join_loop(timeout=None):
        client_thread.join(timeout)
        
def stop_loop(loop=None):
    if loop is None:
        loop = get_event_loop()
    loop.call_soon_threadsafe(lambda l: l.stop(), loop)
    
    
class Ignore:
    pass
    
class DelegatedClient():
    def __init__(self, token, url, loop, no_wait=False):
        log.debug("Starting delegated client")
        self.loop = loop or get_event_loop()
        
        async def run_client(loop):
            self.session = DelegatedRawSocketAsexorClient(url, token, loop)
            try:
                await self.session.start()
            except Exception:
                log.exception("Cannot start client")
                await self.session.stop()
                raise
            
        fut = asyncio.run_coroutine_threadsafe(run_client(self.loop), self.loop)
        if not no_wait:
            fut.result(WAIT_TIMEOUT)
        
    def close(self):
        #leave session
        async def leave():
            await self.session.stop()
        fut = asyncio.run_coroutine_threadsafe(leave(), self.loop)
        fut.result(WAIT_TIMEOUT)
        
    def is_active(self):
        return self.session and self.session.active
        
    def call_no_wait(self, user, role, method, *args, **kwargs):
        if not self.is_active():
            raise Exception('Missing or inactive sesssion')
        async def do_call():
            return await self.session.execute(user, role, method, *args, **kwargs)
        future = asyncio.run_coroutine_threadsafe(do_call(), self.loop)
        return future.result(MAX_TIMEOUT)
        

class WSClient():

    def __init__(self, token, ws_url, session_id=None,loop=None):
        self.loop = loop or get_event_loop()
        self._pending_tasks = {}
        log.info('Starting client')
        self.session = None
        self.session_id = session_id

        async def run_client(loop):
            self.session = AsexorClient(ws_url, token, session_id=self.session_id, loop=loop)
            self.session.subscribe(self.task_callback)
            try:
                await self.session.start()
            except Exception:
                await self.session.stop()
                raise

        fut = asyncio.run_coroutine_threadsafe(run_client(self.loop), self.loop)
        fut.result(WAIT_TIMEOUT)
            
    def close(self):
        #leave session
        async def leave():
            await self.session.stop()
            self._pending_tasks.clear()
        fut = asyncio.run_coroutine_threadsafe(leave(), self.loop)
        fut.result(WAIT_TIMEOUT)

    async def task_callback(self, task_id, status=None, **kwargs):
        future = self._pending_tasks.get(task_id)
        if not future:
            log.error('Update %s for task %s not matched', status, task_id)
            return
        elif future is Ignore:
            if status=="success" or status=="error":
                del self._pending_tasks[task_id]
        if status == "success":
            del self._pending_tasks[task_id]
            future.set_result(kwargs)
        if status == "error":
            del self._pending_tasks[task_id]
            future.set_exception(
                Exception('Remote error: {error}'.format(**kwargs)))

    def call(self, method, *args, **kwargs):
        """Blocks until remote task finishes, returns task results"""
        if not self.session or not self.session.active:
            raise Exception('Missing or inactive sesssion')

        async def do_call():
            future = asyncio.Future()
            task_id = await self.session.execute(method, *args, **kwargs)
            self._pending_tasks[task_id] = future
            return await future
        future = asyncio.run_coroutine_threadsafe(do_call(), self.loop)
        return future.result(MAX_TIMEOUT)
    
    def call_no_wait(self, method, *args, **kwargs):
        """Just schedules task, returns task id"""
        if not self.session or not self.session.active:
            raise Exception('Missing or inactive sesssion')
        async def do_call():
            task_id =  await self.session.execute(method, *args, **kwargs)
            self._pending_tasks[task_id] = Ignore
            return task_id
        future = asyncio.run_coroutine_threadsafe(do_call(), self.loop)
        return future.result(MAX_TIMEOUT)
