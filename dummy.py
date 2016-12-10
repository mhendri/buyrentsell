from app import db, User, Post
import os
import time

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

# create dummy posts for post.db
# using python time object for date/time value in db field
now = time.strftime('%Y-%m-%d %H:%M:%S')

post = Post(None, 'Rubiks Cube', 13.99, "awesome toy", None, "toys", image= "http://www.goo.gl/ZJCcHQ")
db.session.add(post)

post = Post(None, 'Kitchen Table', 50.00, "Ikea table", None, "furniture", image= "http://www.goo.gl/MXX8WG")
db.session.add(post)

post = Post(None, 'MacBook Pro', 600.00, "lightly used computer", None, "computer", image= "http://www.goo.gl/x89NNm")
db.session.add(post)

post = Post(None, 'Drone', 100.00, "mini drone", None, "electronics", image= "http://www.goo.gl/hBDKTe")
db.session.add(post)


#def __init__(self, userid=0, title="", price="", descr="", date=None, category=None):

# commit the record to the database
db.session.commit()
