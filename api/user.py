# Functions for managing user logins and registration.
# All dummy for now

from uuid import uuid4 as uuid

def account_exists(email):
    return False

def register_new(email, password):
    return True

def login(email, password):
    return str(uuid)
