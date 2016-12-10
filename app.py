from flask import Flask
from flask import flash, redirect, render_template, request, session, abort, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
import os
# from flask.ext.login import LoginManager

# Database Imports
from sqlalchemy.orm import sessionmaker
# from tabledef import *

# # create enginer for database
# engine = create_engine('sqlite:///brs.db', echo=True)

app = Flask(__name__)
# set the secret key
app.secret_key = os.urandom(12)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///brs.db'
db = SQLAlchemy(app)
admin = Admin(app, name='BRS Admin', template_mode='bootstrap3')

################################################################################
## MODELS
################################################################################

##------------------------------------------------------------------------------
## User Model
##------------------------------------------------------------------------------
class User(db.Model):
    __tablename__ = "Users"
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column('Firstname', db.String(120), unique=False)
    lastname = db.Column('Lastname', db.String(120), unique=False)
    email = db.Column('email', db.String(120), unique=True)
    password = db.Column('password', db.String(15), unique=False)
    phone = db.Column('phone', db.Integer, unique=False)
    balance = db.Column('balance', db.Integer, unique=False)
    active = db.Column('active', db.Boolean, unique=False)

    ############################################################################
    ## CONSTRUCTOR
    ############################################################################
    def __init__(self, email="", password="", firstname="", lastname="", phone=""):
        ''' '''
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.password = password
        self.phone = phone
        self.balance = 0
        # active is initially False
        # user must be approved by superuser
        self.active = False

    ############################################################################
    ## GETTERS
    ############################################################################
    def get_first_name(self):
        return self.firstname

    def get_last_name(self):
        return self.lastname

    def get_email(self):
        return self.email

    def get_phone(self):
        return self.phone

    def get_balance(self):
        return self.balance

    ############################################################################
    ## SETTERS
    ############################################################################
    def set_email(self, email):
        self.email = email

    def set_phone(self, phone):
        self.phone = phone

    # unsure about this setter / may not be needed
    def set_balance(self, balance):
        self.balance = balance

    def activate_user(self):
        self.active = True

    def suspend_user(self):
        self.active = False

    ############################################################################
    ## OTHER METHODS
    ############################################################################

    # adding money to account
    def deposit(self, amount):
        self.balance += amount

    # removing money from account
    def withdraw(self, amount):
        if amount > self.balance:
            # handle error case
            print("Insufficient Funds to perform this transaction")
        else:
            self.balance -= amount


##------------------------------------------------------------------------------
## Posts Model
##------------------------------------------------------------------------------
class Post(db.Model):
    __tablename__ = "Posts"
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column('userid', db.Integer, db.ForeignKey("Users.id"), unique = False)
    title = db.Column('title', db.String(120), unique=False)
    price = db.Column('price', db.Numeric(12,2), unique=False)
    descr = db.Column('description', db.String(500), unique=False)

    def __init__(self, userid=0, title="", price="", descr=""):
        self.userid = userid
        self.title = title
        self.price = price
        self.descr =  descr

    ############################################################################
    ## GETTERS
    ############################################################################

    ############################################################################
    ## SETTERS
    ############################################################################

    ############################################################################
    ## OTHER METHODS
    ############################################################################

# Need to add few more things:
# buyer_id, (is_biddable, current_bid, time_limit), date_posted, is_reported, image

# Create Database
# db.create_all()

# to add mock data, add entries to dummy.py
# following conventions in that file
# then run `$ python dummy.py` from your shell to commit those changes

################################################################################
## FLASK-ADMIN
################################################################################

admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Post, db.session))

################################################################################
## ROUTES
################################################################################

# Set "homepage" to index.html
@app.route('/')
@app.route('/index')
def index():
    if not session.get('logged_in'):
        return render_template('index.html')
    else:
        #if logged_in, we should display show_entries
        return render_template('index.html')

# Logging In
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        POST_USERNAME = str(request.form['email'])
        POST_PASSWORD = str(request.form['password'])

        # Session = sessionmaker(bind=engine)
        # s = db.session
        query = User.query.filter(User.email==POST_USERNAME,
                User.password==POST_PASSWORD)
        result = query.first()
        if result.active == False:
            flash ('Account not yet active, please wait for admin')
            return render_template('login.html')
        elif result:
            session['logged_in'] = True
            flash('SUCCESS: Logged In!')
            data_dict = dict(username=POST_USERNAME)
        else:
            flash('wrong password!')
            return render_template('login.html')
        return render_template('index.html',**data_dict)
    return render_template('login.html')

# Logging Out
@app.route('/logout')
def logout():
    session['logged_in'] = False
    flash('SUCCESS: Logged Out!')
    return index()

# Signing Up
@app.route('/showSignUp', methods =['GET'])
def showSignUp():
    return render_template('signup.html')

# Success Message
@app.route('/success', methods =['GET', 'POST'])
def success():
    if request.method == 'POST':
        firstname = request.form['inputFirstName']
        lastname = request.form['inputLastName']
        email = request.form['inputEmail']
        password = request.form['inputPassword']
        phone =  request.form['phoneNumber']
        if not db.session.query(User).filter(User.email == email).count():
            entry = User(email, password, firstname, lastname, phone)
            db.session.add(entry)
            db.session.commit()
            return render_template('success.html')
    return render_template('success.html')

@app.route('/posted', methods = ['GET', 'POST'])
def posted():
    if request.method == 'POST':
        title = request.form['title']
        price = request.form['price']
        descr = request.form['descr']
        entry = Post(1,title, price, descr)
        db.session.add(entry)
        db.session.commit()
        return render_template('success.html')
    return render_template('success.html')

if (__name__)=='__main__':
    app.run(host='localhost', port=5000, debug=True)

# User profile pages accessible by /user/id
@app.route('/user/<id>')
#@login_required
def user(id):
    user = User.query.filter_by(id=id).first()
    return render_template('user_profile.html', user=user)

#Rendering pages for testing purposes delete when finished
@app.route('/post')
def post():
    return render_template('post.html')

@app.route('/item/<id>')
def item(id):
    item = Post.query.filter_by(id=id).first()
    return render_template('item.html', item=item)

@app.route('/showPosts')
def show_entries():

    entries = Post.query.order_by(Post.userid)
    return render_template('show_entries.html', entries = entries)



'''
sample code from flaskr.app tutorial
    #main page
    db = get_db()
    cur = db.execute('select title, text from entries order by id desc')
    entries = cur.fetchall()
    return render_template('show_entries.html', entries = entries)


#my code
    allpost = Post.query.filter_by(id).first()
    return render_template('show_entries.html', allpost = allpost)



#joseph's code
@app.route('/add', methods=['POST'])
def posting():
    #adding entries
    if not session.get('logged_in'):
        print("not session.get('logged_in')")
        abort(401)
    db = get_db()
    db.execute('insert into entries (title, text) values (?,?)',
        [request.form['title'], request.form['text']])
    db.commit()
    flash('New entry was sucessfully posted')
    return redirect(url_for('show_entries'))
'''
