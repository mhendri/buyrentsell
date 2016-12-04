from flask import Flask
from flask import flash, redirect, render_template, request, session, abort, url_for
from flask_sqlalchemy import SQLAlchemy
from flask import admin
import os
# from flask.ext.login import LoginManager

# Database Imports
from sqlalchemy.orm import sessionmaker
from tabledef import *

# create enginer for database
engine = create_engine('sqlite:///brs.db', echo=True)

app = Flask(__name__)
# set the secret key
app.secret_key = os.urandom(12)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/brs'
db = SQLAlchemy(app)
admin = Admin(app, name='brs', template_mode='bootstrap3')

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
        query = s.query(User).filter(User.email.in_([POST_USERNAME]),
                                     User.password.in_([POST_PASSWORD]))
        result = query.first()
        if result:
            session['logged_in'] = True
            flash('SUCCESS: Logged In!')
        else:
            flash('wrong password!')
        return index()
    return render_template('login.html')

@app.route('/logout')
def logout():
    session['logged_in'] = False
    flash('SUCCESS: Logged Out!')
    return index()

@app.route('/showSignUp', methods =['GET'])
def showSignUp():
    return render_template('signup.html')

if (__name__)=='__main__':
    app.run(host='localhost', port=5000, debug=True)
