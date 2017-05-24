#!/usr/bin/env python3

# Actual application server. Answers calls from clients, according to API.

from bottle import get, post, request, run
import json

from tradecraft.db import Database, read_engine_string

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
@post('/register')
def register():
    email, password = get_values(request, ['email'])
    try:
        db.add_user(email, password)
    except InvalidEmail:
        return 'invalid_email'
    except EmailAlreadyRegistered:
        return 'already_registered'
    return 'success'

@post('/register/new')
def register_new():
    email, password = get_values(request, ['email', 'password'])
    try:
        db.add_user(email, password)
    except InvalidEmail:
        return json.dumps('invalid_email')
    except EmailAlreadyRegistered:
        return json.dumps('email_already_registered')
    registered = user.register(email, password) # Does validity checking.
    if registered:
        user.send_confirmation(email)
    return json.dumps(registered)

@post('/login')
def login():
    email, password = get_values(request, ['email', 'password'])
    try:
        token = db.get_email_token(email, password)
    except IncorrectPassword:
        return json.dumps(False)
    return db.get_user_token(email, password) # Gives a token

@get('/')
def server_online():
    return json.dumps(True)

def run_server():
    run(host='127.0.0.1', port=8000)

if __name__ == '__main__':
    db = Database(read_engine_string())
    run_server()
