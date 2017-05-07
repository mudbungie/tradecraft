from tradecraft.db import database

def test_init_db():
    assert type(database.init_db()) == database.Database
