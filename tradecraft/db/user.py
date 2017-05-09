import sqlalchemy as sqla
from datetime import datetime
from hashlib import sha512

from tradecraft.db.database import Base
from tradecraft.db.database import get_session

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

# Returns the user id
def add_user(s, email, pw):
    now = datetime.now()
    email = email.lower()
    pwhash = sha512(pw.encode()).hexdigest()
    user = User(email=email, pwhash=pwhash, registration_date=now, alias='test')
    try:
        s.add(user)
        s.commit()
    except:
        #FIXME find the error for primary key conflict
        raise

