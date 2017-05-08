impot sqlalchemy as sqla
from datetime import datetime
from hashlib import sha512

from database import Base
from database import Session

class User(Base):
    __tablename__ = 'users'

    id = Column(sqla.BigInteger, primary_key=True)
    email = Column(sqla.String, unique=True)
    alias = Column(sqla.String)
    pwhash = Column(sqla.String)
    registration_date = Column(sqla.DateTime)

    def __repr__(self):
        return "<User(id='{}', email='{}', alias='{}', registered={})>".\
            format(self.id, self.email, self.alias, self.registration_date)

def add_user(email, pw):
    now = datetime.now()
    email = email.lower()
    pwhash = sha512(pw.encode())
    user = User(email=email, pwhash=pwhash, registration_date=now)
    s = Session()
    try:
        s.add(user)
        s.commit()
    
