test_email = 'a@b.c'
test_password = '1234'

# Creates a connection to the psql database. 
def test_create_connection():
    from tradecraft.db import database
    from sqlalchemy.engine.base import Connection
    conn_string = database.read_engine_string()
    db = database.Database(conn_string)
    with db.get_session() as s:
        assert type(s.connection()) == Connection

def get_memory_db():
    from tradecraft.db import database
    return database.Database('sqlite:///:memory:')

def add_test_user(db):
    db.add_user(test_email, test_password)

def test_in_memory_connection():
    from tradecraft.db import database
    from sqlalchemy.engine.base import Connection
    db = get_memory_db()
    with db.get_session() as s:
        assert type(s.connection()) == Connection

def test_table_create():
    db = get_memory_db()
    assert 'users' in db.e.table_names()

def test_user_creation():
    db = get_memory_db()
    add_test_user(db)
    assert db.get_user_by_email(test_email).email == test_email

