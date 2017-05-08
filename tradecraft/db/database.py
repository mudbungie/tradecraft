# Postgresql connection

import sqlalchemy as sqla
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

def create_engine(cfgpath='db.conf'):
    # Read the db.conf into a dictionary.
    conf = {}    
    with open(cfgpath) as cfg:
        for line in cfg.readlines():
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

engine = create_engine()
Base = declarative_base()
session = sessionmaker(bind=engine)
