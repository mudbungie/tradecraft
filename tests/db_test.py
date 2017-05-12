# Creates a connection to the psql database. 
def test_create_connection():
    from tradecraft.db import database
    from sqlalchemy.engine.base import Connection
    conn_string = database.read_engine_string()
    db = database.Database(conn_string)
    with db.get_session() as s:
        assert type(s.connection()) == Connection

def test_in_memory_connection():
    from tradecraft.db import database
    from sqlalchemy.engine.base import Connection
    db = database.Database('sqlite:///:memory:')
    with db.get_session() as s:
        assert type(s.connection()) == Connection

def test_table_create():
    from tradecraft.db import database
    db = database.Database('sqlite:///:memory:')
    assert 'users' in db.e.table_names()

def test_user_creation():
    from tradecraft.db import database
    email = 'a@b.c'
    db = database.Database('sqlite:///:memory:')
    db.add_user(email, '1234')
    db.get_user_by_email(email)
    assert db.get_user_by_email(email)
