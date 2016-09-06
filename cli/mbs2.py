#! /usr/bin/env python3
import argparse
import requests
from autobahn.asyncio.wamp import ApplicationSession
import logging
import sys
import os
from urllib.parse import urljoin
from cli.action import load_actions
from engine.client import WAMPClient
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

log = logging.getLogger('mbs2')


        
        
class MySession(requests.Session):
    def __init__(self, prefix_url):
        self.prefix_url = prefix_url
        super(MySession, self).__init__()

    def request(self, method, url, *args, **kwargs):
        url = urljoin(self.prefix_url, url)
        return super(MySession, self).request(method, url, *args, **kwargs)


def main():
    p = argparse.ArgumentParser()
    p.add_argument(
        '--api-url', default='http://localhost:6006', help='Base URL for REST API')
    p.add_argument(
        '--wamp-url', default='ws://localhost:8080/ws', help='WAMP Router URL')
    p.add_argument('-u', '--user', help='User name')
    p.add_argument('-p', '--password', help='Password')
    p.add_argument('--debug', action='store_true', help='Debug logging')

    subparsers = p.add_subparsers(help="Available actions", dest='action')

    actions = load_actions()
    for action in actions:
        action_class = actions[action]
        action_class.create_arguments_parser(subparsers)

    opts = p.parse_args()
    
    action_class = actions.get(opts.action)
    if not action_class:
        p.print_help()
        sys.exit(2)
        

    logging.basicConfig(level=logging.DEBUG if opts.debug else logging.INFO)
    if opts.debug:
        log.setLevel(logging.DEBUG)

    resp = requests.post(urljoin(opts.api_url, '/login'),
                         json={'username': opts.user, 'password': opts.password})
    resp.raise_for_status()
    log.debug('Login response %s', resp.json())
    token = resp.json().get('access_token')
    if token:
        http = MySession(prefix_url=opts.api_url)
        http.headers['Authorization'] = 'bearer '+token
        client = WAMPClient(token, opts)
        try:
            client.wait_ready()
            action = action_class(http, client, opts)
            action.do()
        finally:
            client.stop()
        try:
            client.join()
        except KeyboardInterrupt:
            log.debug('Interrupted')
            client.stop()

        log.info('Done')

    else:
        raise Exception('Cannot Log In')


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        log.exception('Program error')
        sys.exit(1)
