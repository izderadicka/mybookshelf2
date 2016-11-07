import os.path
import sys
import asyncio
import logging, logging.handlers
import asexor
from asexor.runner import ApplicationRunnerRawSocket
from asexor.executor import Executor
from asexor.config import Config
from asexor.task import load_tasks_from
from autobahn.wamp.exception import ApplicationError
import time
from urllib.parse import urlunsplit
sys.path.append(os.path.join(os.path.dirname(__file__),'..'))
import engine.dal as dal
from engine.tasks import init
from common.utils import verify_token
from multiprocessing import cpu_count
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


if __name__ == '__main__':
    import argparse

    load_tasks_from('engine.tasks')
    loop =  asyncio.get_event_loop()
    
    loop.run_until_complete(init(Config.CONCURRENT_TASKS or cpu_count()))

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-d', '--debug', action='store_true', help='enable debug')
    parser.add_argument('--log-file', help='log file')
    parser.add_argument('--crossbar-uri', help='WAMP router URI - can be tcp://host:port or path to unix socket (depends on router configuration)')
    parser.add_argument('--test-tasks', action='store_true', help='Add two test tasks date and sleep')
    opts = parser.parse_args()
    level = 'info'
    if opts.debug:
        level = 'debug'
    if opts.log_file:
        handler = logging.handlers.RotatingFileHandler(opts.log_file, maxBytes=10*1024*1024, 
                                                       backupCount=3)
        handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(name)s %(message)s'))
        root_logger=logging.getLogger()
        root_logger.addHandler(handler)
        if opts.debug:
            root_logger.setLevel(logging.DEBUG)
        
    if opts.test_tasks:
        load_tasks_from('simple_tasks', os.path.join(os.path.dirname(asexor.__file__), '../test/tasks'))

    Config.AUTHENTICATION_PROCEDUTE = authenticate
    Config.AUTHENTICATION_PROCEDURE_NAME = "eu.zderadicka.mybookshelf.authenticate"

    #path = os.path.join(os.path.dirname(__file__), '.crossbar/socket1')
    if opts.crossbar_uri:
        url=opts.crossbar_uri
    elif os.getenv('MBS2_CROSSBAR_URI'):
        url = os.getenv('MBS2_CROSSBAR_URI')
    else:
        host = os.getenv('MBS2_CROSSBAR_HOST', 'localhost')
        port = int(os.getenv('MBS2_CROSSBAR_PORT', 9080))
        url = 'tcp://%s:%d' % (host,port)
        
    runner = ApplicationRunnerRawSocket(
        url,
        u"realm1",
    )
    dal.init()
    runner.run(Executor, logging_level=level)
    dal.close()
