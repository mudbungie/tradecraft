#!/usr/bin/env python3

# Actual application server. Answers calls from clients, according to API.

from bottle import get, post, request, run
import json

from tradecraft.db import Database, read_engine_string
from tradecraft.exc import *

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
    email, password = get_values(request, ['email', 'password'])
    if not email or not password:
        return json.dumps({'status':'invalid_submission'})
    try:
        db.add_user(email, password)
    except InvalidEmail:
        return json.dumps({'status':'invalid_email'})
    except EmailAlreadyRegistered:
        return json.dumps({'status':'already_registered'})
    return json.dumps({'status':'success'})

@post('/login')
def login():
    email, password = get_values(request, ['email', 'password'])
    if not email or not password:
        return json.dumps({'status':'invalid_submission'})
    try:
        token = db.get_user_token(email, password)
        return json.dumps({'status':'success', 
            'auth_token':token})
    except IncorrectPassword:
        return json.dumps({'status':'incorrect_password'})
    return db.get_user_token(email, password) # Gives a token

# For approving email accounts, by following links in email.
@get('/confirm/<reg_id>')
def confirm(reg_id):
    uuidre = re.compile(r'[a-f0-9]{32}')
    if uuid.match(reg_id):
        status = db.confirm_email(email)    
        return json.dumps({'status':status})
    # If not, why send a response at all?

@get('/')
def server_online():
    return json.dumps(True)

def run_server():
    run(host='127.0.0.1', port=8000)

if __name__ == '__main__':
    db = Database(read_engine_string())
    run_server()
