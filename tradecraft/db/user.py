import sqlalchemy as sqla
from datetime import datetime
from hashlib import sha512

from tradecraft.db.database import Base, Database

class User(Base):
    __tablename__ = 'users'

    id = sqla.Column(sqla.Integer, primary_key=True, autoincrement=True)
    email = sqla.Column(sqla.String, unique=True)
    alias = sqla.Column(sqla.String, nullable=True)
    pwhash = sqla.Column(sqla.String)
    registration_date = sqla.Column(sqla.DateTime)

    def __repr__(self):
        return "<User(id='{}', email='{}', alias='{}', registered=\'{}\')>"\
            .format(self.id, self.email, self.alias, self.registration_date)
