def test_create_connection():
    from tradecraft.db import database
    from sqlalchemy.engine.base import Connection
    assert type(database.get_session().connection()) == Connection

def test_in_memory_connection():
    from tradecraft.db import database

