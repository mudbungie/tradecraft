#!/usr/bin/env python3

# Actual application server. Answers calls from clients, according to API.

import bottle
from tradecraft import api

@bottle.route('/')
def index():
    return 'True'

# Registration functions.
@bottle.post('/register')
def register():
    email = bottle.request.forms.get('email')
    return json.dumps(api.account_exists(email))

@bottle.post('/register/new')
def register_new():
    email = bottle.request.forms.get('email')
    password = bottle.request.forms.get('password')
    registered = api.register(email, password): # Does validity checking.
    if registered:
        api.send_confirmation(email)
    return registered
    
def run_server():
    bottle.run(host='127.0.0.1', port=8000)

if __name__ == '__main__':
    run_server()
