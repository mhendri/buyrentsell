from flask import Flask
from flask import render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask import url_for

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/brs'
db = SQLAlchemy(app)

#Create our database model
class User(db.Model):
    __tablename__ = "useraccounts"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column('name',db.String(120), unique=False)
    email = db.Column('email', db.String(120), unique=True)
    password = db.Column('password', db.String(15), unique=False)
    phone = db.Column('phone_number', db.Integer, unique=False)


    def __init__(self, name, email, phone, password):
        self.email = email
        self.name = name
        self.password = password
        self.phone = phone

    def __repr__(self):
        return '<E-mail %r>' % self.email

# Set "homepage" to index.html
@app.route('/', methods =['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/showSignUp', methods =['GET', 'POST'])
def showSignUp():
    if request.method == 'POST':
        email = request.form['inputEmail']
        name = request.form['inputName']
        password = request.form['inputPassword']
        phone =  request.form['phoneNumber']
        if not db.session.query(User).filter(User.email == email).count():
            user_email = email
            user_name = name
            user_pw = password
            entry = User(user_name,user_email,phone,user_pw)
            db.session.add(entry)
            db.session.commit()
            return redirect('http://127.0.0.1:5000/')
    return render_template('signup.html')



if (__name__)=='__main__':
	app.run(host='local host', port=5555, debug=True)