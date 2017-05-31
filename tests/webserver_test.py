test_email = 'a@b.c'
test_password = '1234'
localhost_string = 'http://127.0.0.1:8000/'


###IMPORTANT
# All tests in this module require the webserver to be running.

# Utility shortcuts
def register_test_user():
    import requests
    r = requests.post(localhost_string + 'register', 
        data={'email':test_email, 'password':test_password})
    return r

def delete_test_user():
    from tradecraft.db import get_db
    db = get_db()
    db.delete_user_by_email(test_email)

# Not actually a test. Just cleaning up in case tests failed earlier.
def test_pre_cleanup():
    delete_test_user()
    assert True

# Verify that the connection is working at all.
def test_server():
    import requests
    r = requests.get(localhost_string)
    assert r.text == 'true'

def test_register():
    from tradecraft.db import get_db
    r = register_test_user()
    assert r.json()['status'] == 'success'
    db = get_db()
    email = db.get_user_by_email(test_email).email
    delete_test_user()
    assert email == test_email

def test_login():
    import requests
    import re
    from tradecraft.db import get_db
    register_test_user()
    r = requests.post(localhost_string + 'login',
        data={'email':test_email, 'password':test_password})
    delete_test_user()
    uuidre = re.compile(r'^[0-9a-f]{32}$')
    assert uuidre.match(r.json()['auth_token'])

'''
def test_confirm_email():
    import requests
    from tradecraft.db import get_db
    register_test_user()
    db = get_db()
    registration_uuid = db.get_registration_key_by_email(test_email)
    r = requests.get(localhost_string + 'confirmation/' + registration_uuid)
    authorized = db.get_user_by_email(test_email).authorized
    delete_test_user()
    assert user.authorized == True
'''
