#! /usr/bin/env python3
import argparse
import requests
from requests.packages.urllib3.util import Retry
import logging
import sys
import os
import asyncio
from urllib.parse import urljoin
from cli.action import load_actions
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from engine.client import WAMPClient, run_loop_in_thread, stop_loop, join_loop
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
        http.mount('http', requests.adapters.HTTPAdapter(max_retries=Retry(total=5, status_forcelist=[500])))
        http.headers['Authorization'] = 'bearer '+token
        loop = asyncio.get_event_loop()
        run_loop_in_thread(loop)
        client = WAMPClient(token, opts.wamp_url, loop=loop)
        try:
            action = action_class(http, client, opts)
            action.do()
        finally:
            client.close()
            stop_loop(loop)
        try:
            join_loop()
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
