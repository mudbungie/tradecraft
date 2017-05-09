# Postgresql connection

import sqlalchemy as sqla
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

def create_engine(cfg):
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

def get_session(engine):
    #engine = create_engine(cfg)
    s = sessionmaker(bind=engine)
    return s()

def create_tables(engine):
    Base.metadata.create_all(engine)
