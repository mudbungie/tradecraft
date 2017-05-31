# Postgresql connection

import sqlalchemy as sqla
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
from datetime import datetime
from passlib.hash import pbkdf2_sha512
from uuid import uuid4
import re

from tradecraft.exc import *

Base = declarative_base()

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

def get_db():
    conn_string = read_engine_string()
    return Database(conn_string)

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
    # Returns the insert query, raises InvalidEmail, EmailAlreadyRegistered.
    def add_user(self, email, pw):
        keyvals = {}
        now = datetime.now()
        email = email.lower()
        if not re.match(r'(^[a-z0-9_.+-]+@[a-z0-9-]+\.[a-z0-9-.]+$)', email):
            raise InvalidEmail
        keyvals['email'] = email
        keyvals['pwhash'] = pbkdf2_sha512.hash(pw)
        keyvals['registration_date'] = now
        try:
            return self.insert('users', keyvals)
        except sqla.exc.IntegrityError:
            raise EmailAlreadyRegistered

    def delete_user(self, user_id):
        with self.get_session() as s:
            # Clean up all tokens first.
            tokens = self.tables['tokens']
            q = tokens.delete(tokens.c.user_id==user_id)
            q.execute()

            # Clean up pending email confirmations.
            e_confirm = self.tables['pending_email_confirmations']
            q = e_confirm.delete(e_confirm.c.user_id==user_id)
            q.execute()

            # Delete the user itself.
            users = self.tables['users']
            q = users.delete(users.c.id==user_id)
            q.execute()
    
    def get_user_by_email(self, email):
        users = self.tables['users']
        q = users.select(users.c.email == email)
        return q.execute().first()

    def delete_user_by_email(self, email):
        try:
            user_id = self.get_user_by_email(email).id
            self.delete_user(user_id)
            return True
        except AttributeError: # No such user
            return False

    def verify_credentials(self, email, pw):
        user = self.get_user_by_email(email)
        if not user:
            raise NoSuchUser
        if pbkdf2_sha512.verify(pw, user.pwhash):
            return user.id
        return False
        
    def get_user_token(self, email, pw):
        user_id = self.verify_credentials(email, pw)
        if not user_id:
            raise IncorrectPassword
        uuid = uuid4().hex
        keyvals = {'issue_date':datetime.now(),
            'uuid':uuid,
            'user_id':user_id,
            }
        self.insert('tokens', keyvals)
        return uuid

    def confirm_email(self, uuid):
        pending_confirmations = self.tables['pending_email_confirmations']
        users = self.tables['users']
        with self.get_session() as s:
            confirmation = s.query(pending_confirmations).\
                filter(pending_confirmations.c.uuid==uuid)
            
            
        confirmation = self
        q = pending_confirmations.select(pending_confirmations.c.uuid==uuid)
        confirmation = q.execute().first()
        # No rows: return False.
        if not confirmation:
            return False
        uid = confirmation.user_id
        # Get the user, authorize it.
        q = users.select(users.c.id==uid)
        user = q.execute.first()
        with self.get_session() as s:
            s.add(user)
            user.authorized = True
            s.commit()
        
        return True

###
### Table definitions
###

# User accounts.
class User(Base):
    __tablename__ = 'users'

    id = sqla.Column(sqla.Integer, primary_key=True, autoincrement=True)
    email = sqla.Column(sqla.String, unique=True)
    alias = sqla.Column(sqla.String, nullable=True)
    pwhash = sqla.Column(sqla.String)
    registration_date = sqla.Column(sqla.DateTime)
    authorized = sqla.Column(sqla.Boolean, default=False)

    def __repr__(self):
        return "<User(id='{}', email='{}', alias='{}', registered=\'{}\')>"\
            .format(self.id, self.email, self.alias, self.registration_date)

# Ephemeral authentication tokens for user activity.
class Token(Base):
    __tablename__ = 'tokens'

    id = sqla.Column(sqla.Integer, primary_key=True, autoincrement=True)
    user_id = sqla.Column(sqla.Integer, sqla.ForeignKey('users.id'))
    uuid = sqla.Column(sqla.String)
    issue_date = sqla.Column(sqla.DateTime)

class Email_Confirmation(Base):
    __tablename__ = 'pending_email_confirmations'

    id = sqla.Column(sqla.Integer, primary_key=True, autoincrement=True)
    user_id = sqla.Column(sqla.Integer, sqla.ForeignKey('users.id'))
    uuid = sqla.Column(sqla.String, unique=True)
    creation_date = sqla.Column(sqla.DateTime)
    
