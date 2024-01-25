import db
from sqlalchemy import Column, Integer, String, ForeignKey

class User(db.Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    password = Column(String(200), nullable=False)
    email = Column(String(200), nullable=False)

    def __init__(self, name, password, email):
        self.name = name
        self.password = password
        self.email = email

    def __repr__(self):
        return f"User {self.id}: {self.name} {self.email}"

    def __str__(self):
        return f"User {self.id}: {self.name} {self.email}"


class Token(db.Base):
    __tablename__="token"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    token = Column(String(200))

    def __init__(self, user_id, token):
        self.user_id = user_id
        self.token = token

    def __repr__(self):
        return f"Token {self.user_id}: {self.token}"

    def __str__(self):
        return f"Token {self.user_id}: {self.token}"