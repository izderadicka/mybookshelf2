import os.path
import sys
import asyncio
import logging.handlers
import asexor
from asexor.backend_runner import Runner
from asexor.ws_backend import WsAsexorBackend
from asexor.config import Config, NORMAL_PRIORITY
from asexor.task import load_tasks_from
from asexor.raw_backend import RawSocketAsexorBackend
sys.path.append(os.path.join(os.path.dirname(__file__),'..'))
import engine.dal as dal
from engine.tasks import init
from common.utils import verify_token
from multiprocessing import cpu_count
import settings

log = logging.getLogger('engine')

WS_TIMEOUT = settings.TOKEN_VALIDITY_HOURS * 3600

async def authenticate(token):
    log.debug('Got auth request for with token %s', token)
    payload = verify_token(token, settings.SECRET_KEY)
    if payload and payload['email'] and 'user' in payload['roles']:
        user_id = payload['email']
        role='user'
        # Do roles mapping as we need only one role - most permitting
        for r in ['admin', 'superuser', 'trusted_user']:
            if r  in payload['roles']:
                role = r
                break
        log.debug('Authenticaticated user %s to role %s', user_id, role)
        return user_id, role
    return None, None

async def authenticate_delegated(token):
    log.debug("Authentication delegated session")
    if token.decode('utf-8') == settings.DELEGATED_TOKEN:
        return 'delegated', 'user'
    return None, None

# Not needed now
# async def authorization_not_guest(task_name, role):
#     if role == 'guest':
#         return False
#     return True


if __name__ == '__main__':
    import argparse

    load_tasks_from('engine.tasks')
    loop =  asyncio.get_event_loop()
    
    loop.run_until_complete(init(Config.CONCURRENT_TASKS or cpu_count()))

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-d', '--debug', action='store_true', help='enable debug')
    parser.add_argument('--log-file', help='log file')
    parser.add_argument('--ws-port', type=int, help='WebSocket backend port, default 8080')
    parser.add_argument('--ws-addr', help="Address to listen on for WebSocket backend, default 0.0.0.0")
    parser.add_argument('--ws-heartbeat', type=int, help='Server to send ping in x secs (to keep alive connection and check client status), default is off')
    parser.add_argument('--ws-timeout', type=int, default=WS_TIMEOUT, help="Timeout to close websocket after x secs of inactivity, default is %d"%WS_TIMEOUT)
    parser.add_argument('--delegated-port', type=int, help="Port for delegated calls, default 9080")
    parser.add_argument('--delegated-addr', help="Address to listen for delegated calls, default 127.0.0.1")
    parser.add_argument('--disable-delegated', action="store_true", help="Delegated calls can be done only through trusted connection from trusted source, you may want to disable them")
    parser.add_argument('--test-tasks', action='store_true', help='Add two test tasks date and sleep')
    opts = parser.parse_args()
    
    level = logging.INFO
    if opts.debug:
        level = logging.DEBUG
    if opts.log_file:
        handler = logging.handlers.RotatingFileHandler(opts.log_file, maxBytes=10*1024*1024, 
                                                       backupCount=3)
        handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(name)s %(message)s'))
        root_logger=logging.getLogger()
        root_logger.addHandler(handler)
        root_logger.setLevel(level)
    else:
        logging.basicConfig(level=level)
        logging.getLogger().setLevel(level)
        
    if opts.test_tasks:
        load_tasks_from('simple_tasks', os.path.join(os.path.dirname(asexor.__file__), '../test/tasks'))

    Config.AUTHENTICATION_PROCEDUTE = authenticate
    Config.AUTHENTICATION_PROCEDURE_NAME = "eu.zderadicka.mybookshelf.authenticate"

    ws_port=opts.ws_port if opts.ws_port else \
        int(os.getenv('MBS2_WS_PORT',8080))
    ws_addr=opts.ws_addr if opts.ws_addr else \
        os.getenv('MBS2_WS_ADDR', '0.0.0.0')
    delegated_addr = opts.delegated_addr if opts.delegated_addr else \
        os.getenv('MBS2_DELEGATED_ADDR', '127.0.0.1')
    delegated_port = opts.delegated_port if opts.delegated_port else \
        int(os.getenv('MBS2_DELEGATED_PORT', 9080))
    
        
    # Common ASEXOR configs
    Config.PRIORITY_MAP= {'guest': NORMAL_PRIORITY-1,
                          'user': NORMAL_PRIORITY,
                          'trusted_user': NORMAL_PRIORITY,
                          'superuser': NORMAL_PRIORITY+1,
                          'admin': NORMAL_PRIORITY+2 }
    
    #Config.AUTHORIZATION_PROCEDURE = authorization_not_guest
    
    # t limit queue size, if full next requests will be rejected
    Config.TASKS_QUEUE_MAX_SIZE = 10000
    
    # WS hearbeat and timeout
    Config.WS.HEARTBEAT =  opts.ws_heartbeat
    Config.WS.INACTIVE_TIMEOUT = opts.ws_timeout
    
    # basic code to start aiohttp WS ASEXOR backend
    Config.WS.AUTHENTICATION_PROCEDURE = authenticate
    protocols =[(WsAsexorBackend, {'port': ws_port, 'host': ws_addr})]
    
    if not opts.disable_delegated:
        Config.RAW.AUTHENTICATION_PROCEDURE=authenticate_delegated
        protocols.append((RawSocketAsexorBackend, {'url': 'tcp://%s:%d'% (delegated_addr,delegated_port), 
                                                   'delegated': True,
                                                   'no_update': True}))
        
    runner = Runner(protocols)
    dal.init()
    try:
        runner.run()
    finally:
        dal.close()
