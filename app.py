from flask import Flask
from flask import flash, redirect, render_template, request, session, abort, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
import os
# from flask.ext.login import LoginManager

# Database Imports
from sqlalchemy.orm import sessionmaker
from tabledef import *

# # create enginer for database
# engine = create_engine('sqlite:///brs.db', echo=True)

app = Flask(__name__)
# set the secret key
app.secret_key = os.urandom(12)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///brs.db'
db = SQLAlchemy(app)
admin = Admin(app, name='BRS Admin', template_mode='bootstrap3')
admin.add_view(ModelView(User, db.session))

#Create our database model
class User(db.Model):
    __tablename__ = "Users"
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column('Firstname',db.String(120), unique=False)
    lastname = db.Column('Lastname', db.String(120))
    email = db.Column('email', db.String(120), unique=True)
    password = db.Column('password', db.String(15), unique=False)
    phone = db.Column('phone', db.Integer, unique=False)


    def __init__(self, firstname,lastname,email,password,phone):
        ''' '''
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.password = password
        self.phone = phone

# Set "homepage" to index.html
@app.route('/')
@app.route('/index')
def index():
    if not session.get('logged_in'):
        return render_template('index.html')
    else:
        return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        POST_USERNAME = str(request.form['email'])
        POST_PASSWORD = str(request.form['password'])

        Session = sessionmaker(bind=engine)
        s = Session()
        query = s.query(User).filter(User.email==POST_USERNAME,
                                     User.password==POST_PASSWORD)
        result = query.first()
        if result:
            session['logged_in'] = True
            flash('SUCCESS: Logged In!')
            data_dict = dict(username=POST_USERNAME)
        else:
            flash('wrong password!')
            return render_template('login.html')
        return render_template('index.html',**data_dict)
    return render_template('login.html')

@app.route('/logout')
def logout():
    session['logged_in'] = False
    flash('SUCCESS: Logged Out!')
    return index()

@app.route('/showSignUp', methods =['GET'])
def showSignUp():
    return render_template('signup.html')

@app.route('/success', methods =['GET', 'POST'])
def success():
    if request.method == 'POST':
        firstname = request.form['inputFirstName']
        lastname = request.form['inputLastName']
        email = request.form['inputEmail']
        password = request.form['inputPassword']
        phone =  request.form['phoneNumber']
        if not db.session.query(User).filter(User.email == email).count():
            entry = User(firstname,lastname,email,password,phone)
            db.session.add(entry)
            db.session.commit()
            return render_template('success.html')
    return render_template('success.html')

if (__name__)=='__main__':
    app.run(host='localhost', port=5000, debug=True)

#Rendering pages for testing purposes delete when finished
@app.route('/post')
def post():
    return render_template('post.html')

@app.route('/profile')
def profile():
    return render_template('user_profile.html')