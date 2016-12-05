from sqlalchemy import *
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

engine = create_engine('sqlite:///brs.db', echo=True)
Base = declarative_base()

################################################################################
## User Model
################################################################################
class User(Base):
    ''' '''
    __tablename__ = 'Users'

    # Fields
    id = Column(Integer, primary_key=True)
    firstname = Column(String)
    lastname = Column(String)
    email = Column(String, unique=True)
    password = Column(String)
    phone = Column(String)

    # Methods
    def __init__(self, email, password, firstname, lastname, phone):
        ''' '''
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.password = password
        self.phone = phone

class Posts(Base):
    __tablename__ = "Posts"
    id          = Column(Integer, primary_key=True)
    user_id     = Column(Integer, ForeignKey(User.id))
    title       = Column(String)
    price       = Column(Float)
    is_biddable = Column(Boolean)
    current_bid = Column(Float)
    date_posted = Column(Date)
    is_flagged  = Column(Boolean)

    def __init__(self, user_id, title="", price="", is_biddable=""):
        self.user_id        = user_id
        self.title          = title
        self.price          = price
        self.is_biddable    = is_biddable
################################################################################

# create tables
Base.metadata.create_all(engine)
