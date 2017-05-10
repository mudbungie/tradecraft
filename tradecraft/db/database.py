# Postgresql connection

import sqlalchemy as sqla
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager

Base = declarative_base()

class Database:

    def __init__(self, connection_string):
        # Take it from the global.
        self.base = Base
        # Engine
        self.e = sqla.create_engine(connection_string, echo=True)
        self.sessionmaker = sessionmaker(self.e)

        # Make tables.
        self.base.metadata.create_all(self.e)
        # Map them for accessibility through Database object.
        self.tablenames = self.e.table_names()
        self.tables = {}
        for tablename in self.tablenames:
            table = sqla.Table(tablename, sqla.MetaData(self.e), 
                autoload=True, autoload_with=self.e)
            self.tables[tablename] = table

    # Always call using a with statement.
    @contextmanager
    def get_session(self):
        s = self.sessionmaker()
        try:
            yield s
        except:
            s.rollback()
            raise
        finally:
            s.close()
    #
    ### SQL abstractions
    #
    def insert(self, tablename, keyvals):
        table = self.tables[tablename]
        q = table.insert(keyvals)
        return self.e.execute(q)

    #
    ### User table functions.
    # 
    def add_user(self, email, pw):
        now = datetime.now()
        email = email.lower()

# Reads a config file's path into a connection string.        
def read_engine_string(cfgpath='db.conf'):
    conf = {}    
    with open(cfgpath) as cfgfile:
        for line in cfgfile.readlines():
            k, v = line.strip().split('=')[0:2]
            conf[k] = v
    
    # Compile a connection string.
    connection_string = '{}://{}:{}@{}/{}'.format(
        conf['engine'],
        conf['user'],
        conf['password'],
        conf['host'],
        conf['dbname']
        )
    return connection_string

def create_engine(connection_string):
    return sqla.create_engine
    if cfg == 'memory':
        connectionString = 'sqlite:///:memory:'
    else:
        # Read the db.conf into a dictionary.
        conf = {}    
        with open(cfg) as cfgfile:
            for line in cfgfile.readlines():
                k, v = line.strip().split('=')[0:2]
                conf[k] = v
        
        # Compile a connection string.
        connectionString = '{}://{}:{}@{}/{}'.format(
            conf['engine'],
            conf['user'],
            conf['password'],
            conf['host'],
            conf['dbname']
            )

    # Return a connection.
    return sqla.create_engine(connectionString, echo=True)

def get_sessionmaker(engine):
    return sessionmaker(bind=engine)

def create_tables(engine):
    Base.metadata.create_all(engine)
