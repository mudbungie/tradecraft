def test_create_connection():
    from tradecraft.db import database
    import sqlalchemy
    assert type(database.create_engine()) == sqlalchemy.engine.base.Engine

