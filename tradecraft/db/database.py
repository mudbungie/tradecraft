# Postgresql connection

import sqlalchemy as sqla

class Database:
    def __init__(self, conf):
        self.dbname = conf['dbname']
        self.host = conf['host']
        self.user = conf['user']
        self.password = conf['password']
        self.reflect = reflect
        connectionString = 'postgresql+psycopg2://{}:{}@{}/{}'.filter(
            conf['user'],
            conf['password'],
            conf['host'],
            conf['dbname']
            )
        self.connection = sqla.create_engine(connectionString)
        self.metadata = sqla.MetaData(self.connection)
        self.metadata.reflect()
        
    def initTable(self, tableName):
        table = sqla.Table(tableName, self.metadata, autoload=True,
            autoload_with=self.connection)
        return table

    def initTables(self, tableNames):
        self.tables = {}
        for tableName in tableNames:
            self.tables[tableName] = self.initTable(tableName)
