# Creates a connection to the psql database. 
def test_create_connection():
    from tradecraft.db import database
    from sqlalchemy.engine.base import Connection
    e = database.create_engine('db.conf')
    s = database.get_session(e)
    assert type(s.connection()) == Connection
    s.close()

def test_in_memory_connection():
    from tradecraft.db import database
    from sqlalchemy.engine.base import Connection
    e = database.create_engine('memory')
    s = database.get_session(e)
    assert type(s.connection()) == Connection
    s.close()

def test_table_create():
    from tradecraft.db import user, database
    e = database.create_engine('memory')
    s = database.get_session(e)
    database.create_tables(e)
    assert e.table_names() == ['users']
    s.close()

def test_user_creation():
    from tradecraft.db import user, database
    e = database.create_engine('memory')
    database.create_tables(e)
    s = database.get_session(e)
    email = 'test@test.com'
    user.add_user(s, email, '1234')
    s.commit()
    assert user #FIXME actuall test
    s.close()
