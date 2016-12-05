import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tabledef import engine, User

engine = create_engine('sqlite:///brs.db', echo=True)

# __init__(self, firstname, lastname, email, password, phone):
#     ''' '''
#     self.firstname = firstname
#     self.lastname = lastname
#     self.email = email
#     self.password = password
#     self.phone = phone

# create a session
Session = sessionmaker(bind=engine)
session = Session()

user = User('akbar@example.com', 'password', 'Akbar', 'Mirza', '5555555555')
session.add(user)

user = User('mike@example.com', 'mikespass', 'Michael', 'Hendrickson', '5555555555')
session.add(user)

user = User('joseph@example.com', 'savage', 'Joseph', 'Park', '5555555555')
session.add(user)

posts = Posts('Rubik\'s Cube', 13.99, False, "2016-12-05", False)
session.add(posts)

# commit the record to the database
session.commit()
