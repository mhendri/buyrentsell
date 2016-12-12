from app import db, User, Post
import os
import time

# if there is a brs.db, delete it
if os.path.exists('brs.db'):
    os.remove('brs.db')

# create databases
db.create_all()

# 1
user = User('akbar@example.com', 'password', 'Akbar', 'Mirza', '5555555555', "https://scontent-lga3-1.xx.fbcdn.net/v/t1.0-9/13423982_969682129817159_8066714001663659613_n.jpg?oh=cab730caafc076a216d031b863948dc8&oe=58B68437")
user.activate_user()
user.deposit(100)
db.session.add(user)

# 2
user = User('mike@example.com', 'mikespass', 'Michael', 'Hendrickson', '5555555555', "https://scontent-lga3-1.xx.fbcdn.net/v/t1.0-9/1535703_10201283474032904_761764383_n.jpg?oh=c1406ed1b4f0f70bdbfb80b5dd857b74&oe=58B1DC4E")
user.activate_user()
user.deposit(500)
db.session.add(user)

# 3
user = User('joseph@example.com', 'savage', 'Joseph', 'Park', '5555555555', "https://scontent-lga3-1.xx.fbcdn.net/v/t1.0-9/11182070_10206317524914398_8942662258543776551_n.jpg?oh=9377d46212e35b1247e8b1c9f79ab03d&oe=58B4BD67")
db.session.add(user)

# 4
user = User('edwin@example.com', 'glnerds', 'Edwin', 'Zhou', '5555555555', "https://scontent-lga3-1.xx.fbcdn.net/v/t1.0-9/314975_2231256194400_1572208950_n.jpg?oh=6893fb6270a43f4aa92fe2e74c003669&oe=58BC2D79")
db.session.add(user)

# 5
user = User('test@test.com', 'test', 'test', 'test', '5555', "")
db.session.add(user)

#6
user = User('tracy@example.com', 'dresser', 'Tracy', 'Miller', '5555', "")
db.session.add(user)

# create dummy posts for post.db
# using python time object for date/time value in db field
now = time.strftime('%Y-%m-%d %H:%M:%S')

# 1
post = Post(1, 'Rubiks Cube', 13.99, "awesome toy", None, "sports", image= "http://www.goo.gl/ZJCcHQ")
db.session.add(post)

# 2
post = Post(1, 'Kitchen Table', 50.00, "Ikea table", None, "furniture", image= "http://www.goo.gl/MXX8WG")
db.session.add(post)

# 3
post = Post(1, 'MacBook Pro', 600.00, "lightly used computer", None, "electronic", image= "http://www.goo.gl/x89NNm")
db.session.add(post)

# 4
post = Post(1, 'Drone', 100.00, "mini drone", None, "electronic", image= "http://www.goo.gl/hBDKTe")
db.session.add(post)

# 5
post = Post(2, 'Basketball', 50.00, "NBA Baseketball", None, "sports", image="https://goo.gl/QcgX0p")
db.session.add(post)

# 5
post = Post(2, 'Dining Table', 100.00, 'New Dining Table from IKEA', None, 'furniture', image="https://goo.gl/E7shvm")
db.session.add(post)

# 6
post = Post(2, 'T-shirt', 25.00, 'Worn once', None, 'clothing', image = "https://goo.gl/nJHXBT")
db.session.add(post)

# 7
post = Post(2, 'Refrigerator', 400.00, 'Used for 2 years and we are moving.', None, 'appliance', image = "https://goo.gl/SlfUdm")
db.session.add(post)


#def __init__(self, userid=0, title="", price="", descr="", date=None, category=None):

# commit the record to the database
db.session.commit()
