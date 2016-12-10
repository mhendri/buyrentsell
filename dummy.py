from app import db, User
import os

# if there is a brs.db, delete it
if os.path.exists('brs.db'):
    os.remove('brs.db')

# create databases
db.create_all()

user = User('akbar@example.com', 'password', 'Akbar', 'Mirza', '5555555555')
db.session.add(user)

user = User('mike@example.com', 'mikespass', 'Michael', 'Hendrickson', '5555555555')
db.session.add(user)

user = User('joseph@example.com', 'savage', 'Joseph', 'Park', '5555555555')
db.session.add(user)

user = User('test@test.com', 'test', 'test', 'test', '5555')
db.session.add(user)
# posts = Posts('Rubik\'s Cube', 13.99, False, "2016-12-05", False)
# session.add(posts)

# commit the record to the database
db.session.commit()