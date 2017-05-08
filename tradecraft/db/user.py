import sqlalchemy as sqla
from datetime import datetime
from hashlib import sha512

from tradecraft.db.database import Base
from tradecraft.db.database import get_session

class User(Base):
    __tablename__ = 'users'

    id = sqla.Column(sqla.BigInteger, primary_key=True)
    email = sqla.Column(sqla.String, unique=True)
    alias = sqla.Column(sqla.String)
    pwhash = sqla.Column(sqla.String)
    registration_date = sqla.Column(sqla.DateTime)

    def __repr__(self):
        return "<User(id='{}', email='{}', alias='{}', registered=\'{}\')>"\
            .format(self.id, self.email, self.alias, self.registration_date)

def add_user(email, pw):
    now = datetime.now()
    email = email.lower()
    pwhash = sha512(pw.encode())
    user = User(email=email, pwhash=pwhash, registration_date=now)
    s = get_session()
    try:
        s.add(user)
        s.commit()
    except:
        #FIXME find the error
        raise()
