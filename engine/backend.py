import os.path
import sys
import asyncio
import logging
from autobahn.asyncio.wamp import ApplicationSession, ApplicationRunnerRawSocket
from autobahn.wamp.exception import ApplicationError
import time

sys.path.append(os.path.join(os.path.dirname(__file__),'..'))
from app.utils import verify_token
import settings

log = logging.getLogger('engine')


def authenticate(realm, user_id, details):
    log.debug('Got auth request for %s')
    token = details.get('ticket')
    payload = verify_token(token, settings.SECRET_KEY)
    if payload and user_id == payload['email']:
        if 'user' in payload['roles']:
            log.debug('Authenticaticated user %s to role user', user_id)
            return 'user'
    return 'anonymous'


@asyncio.coroutine
def get_time():
    return time.time()


class AppSession(ApplicationSession):

    @asyncio.coroutine
    def onJoin(self, details):

        self.register(authenticate, 'eu.zderadicka.mybookshelf.authenticate')

        while True:
            # PUBLISH an event
            #
            self.publish('eu.zderadicka.mybookshelf2.heartbeat', (yield from get_time()))
            log.debug("Heartbeat")
            yield from asyncio.sleep(5)

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    log.setLevel(logging.DEBUG)
    asyncio.get_event_loop().set_debug(True)
    log.debug('creating application')
    path = os.path.join(os.path.dirname(__file__), '.crossbar/socket1')
    cb_realm = os.environ.get('CB_REALM', 'realm1')
    app = ApplicationRunnerRawSocket(path, realm=cb_realm)
    log.debug('started application')
    app.run(AppSession)
    log.debug('finished application')
