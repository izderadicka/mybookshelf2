import os
import asyncio
import logging
from autobahn.asyncio.wamp import ApplicationSession, ApplicationRunner
from autobahn.wamp.exception import ApplicationError
import time

log=logging.getLogger('engine')


class AppSession(ApplicationSession):
    
    @asyncio.coroutine
    def onJoin(self, details):
        
        while True:

            # PUBLISH an event
            #
            self.publish('eu.zderadicka.mybookshelf2.heartbeat', time.time())
            log.debug("Heartbeat")
            yield from asyncio.sleep(5)
            

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    log.setLevel(logging.DEBUG)
    #asyncio.get_event_loop().set_debug(True)
    log.debug('creating application')
    cb_uri=os.environ.get('CB_URI','ws://localhost:8080/ws' )
    cb_realm=os.environ.get('CB_REALM', 'realm1')
    app=ApplicationRunner(cb_uri, realm=cb_realm)
    log.debug('started application')
    app.run(AppSession)
    log.debug('finished application')
