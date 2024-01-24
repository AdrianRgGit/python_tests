import db
from sqlalchemy import Column, Integer, String

class User(db.Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    password = Column(String(200))
    email = Column(String(200))

    def __init__(self, name, password, email):
        self.name = name
        self.password = password
        self.email = email

    def __repr__(self):
        return f"User {self.id}: {self.name} ({self.email})"

    def __str__(self):
        return f"User {self.id}: {self.name} ({self.email})"
