test_email = 'a@b.c'
test_password = '1234'

# Creates a database connection.
def get_db():
    from tradecraft.db import Database, read_engine_string
    conn_string = read_engine_string()
    return Database(conn_string)

# Creates a connection to the psql database. 
def test_create_connection():
    from tradecraft.db import Database, read_engine_string
    from sqlalchemy.engine.base import Connection
    conn_string = read_engine_string()
    db = Database(conn_string)
    with db.get_session() as s:
        assert type(s.connection()) == Connection

def add_test_user(db):
    db.add_user(test_email, test_password)

def test_in_memory_connection():
    from tradecraft.db import Database
    from sqlalchemy.engine.base import Connection
    db = get_db()
    with db.get_session() as s:
        assert type(s.connection()) == Connection

def test_table_create():
    db = get_db()
    assert 'users' in db.e.table_names()

def test_user_creation():
    db = get_db()
    add_test_user(db)
    assert db.get_user_by_email(test_email).email == test_email

def test_user_token():
    import re
    db = get_db()
    add_test_user(db)
    uuidre = re.compile(r'^[0-9a-f]{32}$')
    assert uuidre.match(db.get_user_token(test_email, test_password))
