test_email = 'a@b.c'
test_password = '1234'
localhost_string = 'http://127.0.0.1:8000/'

###IMPORTANT
# All tests in this module require the webserver to be running.

# Not actually a test. Just cleaning up in case tests failed earlier.
def test_pre_cleanup():
    from tradecraft.db import get_db
    db = get_db()
    db.delete_user_by_email(test_email)
    assert True

# Verify that the connection is working at all.
def test_server():
    import requests
    r = requests.get(localhost_string)
    assert r.text == 'true'

def test_register():
    import requests
    from tradecraft.db import get_db
    r = requests.post(localhost_string + 'register', 
        data={'email':test_email, 'password':test_password})
    assert r.json()['status'] == 'success'
    db = get_db()
    email = db.get_user_by_email(test_email).email
    db.delete_user_by_email(test_email)
    assert email == test_email

def test_login():
    import requests
    import re
    from tradecraft.db import get_db
    requests.post(localhost_string + 'register', 
        data={'email':test_email, 'password':test_password})
    r = requests.post(localhost_string + 'login',
        data={'email':test_email, 'password':test_password})
    db = get_db()
    db.delete_user_by_email(test_email)
    uuidre = re.compile(r'^[0-9a-f]{32}$')
    assert uuidre.match(r.json()['auth_token'])

