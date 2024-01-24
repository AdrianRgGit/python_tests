from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os

if not os.path.exists('database'):
    os.makedirs('database')

engine = create_engine('sqlite:///database/auth_cookies.db', connect_args={'check_same_thread': False})

Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()