from autobahn.asyncio.wamp import ApplicationSession
import logging
import sys
import os
import asyncio
from asyncio import get_event_loop, set_event_loop
import threading
from autobahn.wamp.types import ComponentConfig
from autobahn.asyncio.websocket import WampWebSocketClientFactory
from urllib.parse import urlparse
from asexor.config import Config as AsexorConfig
import time
from functools import partial
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from common.utils import extract_token
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

log = logging.getLogger('client')

MAX_TIMEOUT = 300
WAIT_TIMEOUT = 5000


class ClientSession(ApplicationSession):

    def __init__(self, realm, user, token, task_cb):
        ApplicationSession.__init__(self, config=ComponentConfig(realm=realm))
        self._on_update = task_cb
        self.user = user
        self.token = token

    def onConnect(self):
        log.debug('Connected')
        self.join(self.config.realm, [u"ticket"], self.user)

    def onChallenge(self, ch):
        if ch.method == 'ticket':
            log.debug('Got challenge %s', ch)
            return self.token
        else:
            raise Exception('Invalid authentication method')

    async def onJoin(self,  details):
        log.debug('Session joined %s', details)

        self.subscribe(
            self.on_task_update, AsexorConfig.UPDATE_CHANNEL)

    def on_task_update(self, task_id, status=None, **kwargs):
        if self._on_update:
            self._on_update(task_id, status, **kwargs)

    def set_update_cb(self, fn):
        self._on_update = fn

    def onLeave(self, details):
        log.debug("Leaving session %s", details)
        self.disconnect()

    def onDisconnect(self):
        log.debug('Disconnected')
        
        

wamp_thread = None
def run_loop_in_thread(loop):
    global wamp_thread
    def _run_loop(loop):
        set_event_loop(loop)
        loop.run_forever()
        
    wamp_thread = threading.Thread(
            target= _run_loop , name='WAMP Thread', args=(loop,))
    wamp_thread.daemon = True
    wamp_thread.start()
    
def join_loop(timeout=None):
        wamp_thread.join(timeout)
        
def stop_loop(loop=None):
    if loop is None:
        loop = get_event_loop()
    loop.call_soon_threadsafe(lambda l: l.stop(), loop)
    

class WAMPClient():

    def __init__(self, token, wamp_url, loop=None):
        self.loop = loop or get_event_loop()
        self._pending_tasks = {}
        user = extract_token(token)['email']
        log.info('Starting client for user %s' % (user,))
        self._ready = threading.Event()

        async def run_client(loop):

            def fact():
                self.session = ClientSession(
                    realm='realm1', user=user, token=token, task_cb=self.task_callback)
                return self.session

            transport_factory = WampWebSocketClientFactory(
                fact, url=wamp_url)

            parsed_url = urlparse(wamp_url)
            ssl = False
            if parsed_url.scheme == 'https':
                ssl = True

            hp = parsed_url.netloc.split(':')
            if len(hp) == 1:
                host, port = hp[0], 8080
            elif len(hp) == 2:
                host, port = hp[0], int(hp[1])
            else:
                raise ValueError('Invalid URL %s' % wamp_url)

            conn = loop.create_connection(
                transport_factory, host, port, ssl=ssl)
            (transport, protocol) = await conn

            self.protocol = protocol
            self.transport = transport
            self._ready.set()
            
        fut = asyncio.run_coroutine_threadsafe(run_client(self.loop), self.loop)
        fut.result(WAIT_TIMEOUT)
        self.wait_ready()
        
        
    def wait_ready(self):
        ok = self._ready.wait(WAIT_TIMEOUT)
        if not ok:
            raise TimeoutError('event timeout')
        start = time.time()
        while not (hasattr(self, 'session') and self.session.is_attached()):
            time.sleep(0.01)
            if time.time() - start > WAIT_TIMEOUT:
                raise TimeoutError('session not ready')
            
    def close(self):
        #leave session
        
        async def leave():
            res = self.session.leave()
            if isinstance(res, asyncio.Future):
                await res
        
        fut = asyncio.run_coroutine_threadsafe(leave(), self.loop)
        fut.result(WAIT_TIMEOUT)


    def task_callback(self, task_id, status=None, **kwargs):
        future = self._pending_tasks.get(task_id)
        if not future:
            log.error('Update for task %s not matched', task_id)
            return
        if status == "success":
            future.set_result(kwargs)
        if status == "error":
            future.set_exception(
                Exception('Remote error: {error}'.format(**kwargs)))

    def call(self, method, *args, **kwargs):
        """Blocks until remote task finishes, returns task results"""
        if not self.session or not self.session.is_attached():
            raise Exception('Missing or inactive sesssion')

        async def do_call():
            future = asyncio.Future()
            task_id = await self.session.call(AsexorConfig.RUN_TASK_PROC, method, *args, **kwargs)
            self._pending_tasks[task_id] = future
            return await future
        loop = self.loop
        future = asyncio.run_coroutine_threadsafe(do_call(), loop)

        return future.result(MAX_TIMEOUT)
    
    def call_no_wait(self, method, *args, **kwargs):
        """Just schedules task, returns task id"""
        if not self.session or not self.session.is_attached():
            raise Exception('Missing or inactive sesssion')
        async def do_call():
            return await self.session.call( AsexorConfig.RUN_TASK_PROC, method, *args, **kwargs)
        loop = self.loop
        future = asyncio.run_coroutine_threadsafe(do_call(), loop)
        return future.result(MAX_TIMEOUT)
