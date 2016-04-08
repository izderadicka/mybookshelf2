# -*- coding: utf-8 -*-

"""
    Eve Demo
    ~~~~~~~~

    A demostration of a simple API powered by Eve REST API.

    The live demo is available at eve-demo.herokuapp.com. Please keep in mind
    that the it is running on Heroku's free tier using a free MongoHQ
    sandbox, which means that the first request to the service will probably
    be slow. The database gets a reset every now and then.

    :copyright: (c) 2016 by Nicola Iarocci.
    :license: BSD, see LICENSE for more details.
"""

import os
from eve import Eve
from eve.auth import TokenAuth
from flask import current_app, request, abort, json, Response


class TokenAuth(TokenAuth):
    def check_auth(self, token, allowed_roles, resource, method):
        """For the purpose of this example the implementation is as simple as
        possible. A 'real' token should probably contain a hash of the
        username/password combo, which sould then validated against the account
        data stored on the DB.
        """
        # use Eve's own db driver; no additional connections/resources are used
        print('TOKEN raw',token)
        if token.startswith('bearer '):
            
            token=token[7:]
            print('TOKEN',token)
            accounts = app.data.driver.db['accounts']
            return accounts.find_one({'token': token})

# Heroku support: bind to PORT if defined, otherwise default to 5000.
if 'PORT' in os.environ:
    port = int(os.environ.get('PORT'))
    # use '0.0.0.0' to ensure your REST API is reachable from all your
    # network (and not only your computer).
    host = '0.0.0.0'
else:
    port = 6006
    host = '127.0.0.1'

app = Eve(auth=TokenAuth)

cors_headers={
              'Access-Control-Allow-Headers':'Authorization, Content-type',
              'Access-Control-Allow-Methods':'OPTIONS, HEAD, POST, DELETE, GET',
              'Access-Control-Allow-Origin':'*',
              'Access-Control-Expose-Headers':'',
              'Access-Control-Max-Age':'21600',
              }
@app.route('/auth/login', methods=['OPTIONS', 'POST'])
def login(): 
    if request.method=='OPTIONS':
        print('GOT OPTIONS')
        return Response(headers=cors_headers)
    if request.method != 'POST' or request.mimetype != 'application/json':
        abort(400)
        
    credentials=json.loads(request.data)
    
    if credentials and credentials.get('email') and credentials.get('password'):
        resp= json.jsonify(access_token='1234')
        resp.headers.extend(cors_headers)
        return resp
    else:
        print (credentials)
        abort(400,'Provide credentials')
        

if __name__ == '__main__':
    app.run(host=host, port=port, debug=True)
