#!/usr/bin/env python3

# Actual application server. Answers calls from clients, according to API.

from bottle import get, post, request
from tradecraft import api

### Utility
# Just gets values corresponding to keys from request.
def get_values(request, keys):
    values = []
    for key in keys:
        values.append(request.forms.get(key))
    return values


#
# Registration functions.
#
@bottle.post('/register')
def register():
    email = get_values(request, ['email'])
    return json.dumps(api.account_exists(email))

@bottle.post('/register/new')
def register_new():
    email, password = get_values(request, ['email', 'password'])
    registered = api.register(email, password): # Does validity checking.
    if registered:
        api.send_confirmation(email)
    return json.dumps(registered)

@bottle.post
def login():
    email, password = get_values(request, ['email', 'password'])
    return api.login(email, password) # Gives a token

@get('/')
def server_online():
    return json.dumps(True)

def run_server():
    bottle.run(host='127.0.0.1', port=8000)

if __name__ == '__main__':
    run_server()
