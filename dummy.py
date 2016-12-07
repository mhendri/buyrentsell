from app import db, User

user = User('akbar@example.com', 'password', 'Akbar', 'Mirza', '5555555555')
db.session.add(user)

user = User('mike@example.com', 'mikespass', 'Michael', 'Hendrickson', '5555555555')
db.session.add(user)

user = User('joseph@example.com', 'savage', 'Joseph', 'Park', '5555555555')
db.session.add(user)

# commit the record to the database
db.session.commit()
