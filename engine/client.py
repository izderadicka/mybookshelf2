from autobahn.asyncio.wamp import ApplicationSession
from asyncio import coroutine, get_event_loop
import logging
import requests
import os.path
import sys

sys.path.append(os.path.join(os.path.dirname(__file__),'..'))
from app.utils import extract_token

log=logging.getLogger('client')

class ClientSession(ApplicationSession):
    # must be set before session
    TOKEN=''
    USER=''
    
    def onConnect(self):
        log.debug('Connected')
        self.join(self.config.realm, [u"ticket"], self.USER)
        
    def onChallenge(self, ch):
        if  ch.method=='ticket':
            log.debug('Got challenge %s', ch)
            return self.TOKEN
        else:
            raise Exception('Invalid authentication method')
        
    @ coroutine
    def onJoin(self,  details):
        log.debug('Session joined %s', details)
        
        self.subscribe(lambda t: print('#Notification', t), 'eu.zderadicka.mybookshelf2.heartbeat')
        
    def onLeave(self, details):
        log.debug("Leaving session %s", details)
        self.disconnect()
        
    def onDisconnect(self):
        log.debug('Disconnected')
        get_event_loop().stop()
        
       
        
if __name__=='__main__':
    #logging.basicConfig(level=logging.DEBUG)
    log.setLevel(logging.DEBUG)
    resp=requests.post('http://localhost:6006/login', json={'username':'admin', 'password':'admin'})
    token = resp.json().get('access_token')
    if token:
        ClientSession.TOKEN=token
        ClientSession.USER=extract_token(token)['email']
        print('Starting client for user %s'% (ClientSession.USER))
        from autobahn.asyncio.wamp import ApplicationRunner
        app=ApplicationRunner(url='ws://localhost:8080/ws', realm='realm1')
        app.run(ClientSession)