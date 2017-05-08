def test_create_connection():
    from tradecraft.db import database
    from sqlalchemy.engine.base import Connection
    assert type(database.session().connection()) == Connection

