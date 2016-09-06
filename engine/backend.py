import os.path
import sys
import asyncio
import logging
import asexor
from asexor.runner import ApplicationRunnerRawSocket
from asexor.executor import Executor
from asexor.config import Config
from asexor.task import load_tasks_from
from autobahn.wamp.exception import ApplicationError
import time
import engine.dal as dal

# sys.path.append(os.path.join(os.path.dirname(__file__),'..'))
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


if __name__ == '__main__':
    import argparse

    load_tasks_from('engine.tasks')

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-d', '--debug', action='store_true', help='enable debug')
    parser.add_argument('--test-tasks', action='store_true', help='Add two test tasks date and sleep')
    opts = parser.parse_args()
    level = 'info'
    if opts.debug:
        level = 'debug'
        
    if opts.test_tasks:
        load_tasks_from('simple_tasks', os.path.join(os.path.dirname(asexor.__file__), '../test/tasks'))

    Config.AUTHENTICATION_PROCEDUTE = authenticate
    Config.AUTHENTICATION_PROCEDURE_NAME = "eu.zderadicka.mybookshelf.authenticate"

    path = os.path.join(os.path.dirname(__file__), '.crossbar/socket1')
    runner = ApplicationRunnerRawSocket(
        path,
        u"realm1",
    )
    dal.init()
    runner.run(Executor, logging_level=level)
    dal.close()
