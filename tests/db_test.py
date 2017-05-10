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
    from tradecraft.db import user, database
    db = database.Database('sqlite:///:memory:')
    assert db.e.table_names() == ['users']

#def test_user_creation():
#    from tradecraft.db import user, database
#    e = database.create_engine('memory')
#    database.create_tables(e)
#    s = database.get_session(e)
#    email = 'test@test.com'
#    user.add_user(s, email, '1234')
#    s.commit()
#    assert user #FIXME actuall test
#    s.close()
