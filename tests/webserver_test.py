test_email = 'a@b.c'
test_password = '1234'
localhost_string = 'http://127.0.0.1:8000/'

###IMPORTANT
# All tests in this module require the webserver to be running.

# Still gonna need DB connections to validate insertions and regress changes.

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
    db = get_db()
    email = db.get_user_by_email(test_email).email
    db.delete_user_by_email(test_email)
    assert email == test_email


