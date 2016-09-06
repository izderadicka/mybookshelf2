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
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from app.utils import extract_token
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

log = logging.getLogger('client')

MAX_TIMEOUT = 300


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
        get_event_loop().stop()


class WAMPClient():

    def __init__(self, token, opts):
        self._pending_tasks = {}
        self.opts = opts
        user = extract_token(token)['email']
        log.info('Starting client for user %s' % (user,))
        self._ready = threading.Event()

        def run_client(loop):
            set_event_loop(loop)

            def fact():
                self.session = ClientSession(
                    realm='realm1', user=user, token=token, task_cb=self.task_callback)
                return self.session

            transport_factory = WampWebSocketClientFactory(
                fact, url=opts.wamp_url)

            parsed_url = urlparse(opts.wamp_url)
            ssl = False
            if parsed_url.scheme == 'https':
                ssl = True

            hp = parsed_url.netloc.split(':')
            if len(hp) == 1:
                host, port = hp[0], 8080
            elif len(hp) == 2:
                host, port = hp[0], int(hp[1])
            else:
                raise ValueError('Invalid URL %s' % opts.wamp_url)

            conn = loop.create_connection(
                transport_factory, host, port, ssl=ssl)
            (transport, protocol) = loop.run_until_complete(conn)

            self.protocol = protocol
            self.transport = transport
            self._ready.set()
            loop.run_forever()
            if protocol._session:
                loop.run_until_complete(protocol._session.leave())

        self.wamp_thread = threading.Thread(
            target=run_client, name='WAMP Thread', args=(get_event_loop(),))
        self.wamp_thread.start()

    def join(self, timeout=None):
        self.wamp_thread.join(timeout)
        
    def wait_ready(self):
        ok = self._ready.wait(5)
        if not ok:
            raise TimeoutError()
        start = time.time()
        while not (hasattr(self, 'session') and self.session.is_attached()):
            time.sleep(0.01)
            if time.time() - start > 5:
                raise TimeoutError()

    def stop(self):
        loop = get_event_loop()
        loop.call_soon_threadsafe(lambda l: l.stop(), loop)

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
        if not self.session or not self.session.is_attached():
            raise Exception('Missing or inactive sesssion')

        async def do_call():
            future = asyncio.Future()
            task_id = await self.session.call(AsexorConfig.RUN_TASK_PROC, method, *args, **kwargs)
            self._pending_tasks[task_id] = future
            return await future
        loop = get_event_loop()
        future = asyncio.run_coroutine_threadsafe(do_call(), loop)

        return future.result(MAX_TIMEOUT)
