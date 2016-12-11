from flask import Flask
from flask import flash, redirect, render_template, request, session, abort, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView


from forms import *
import random

import os
# from flask.ext.login import LoginManager

# for datetime
from datetime import datetime

# Database Imports
from sqlalchemy.orm import sessionmaker
# from tabledef import *

# # create enginer for database
# engine = create_engine('sqlite:///brs.db', echo=True)

app = Flask(__name__)
# set the secret key
app.secret_key = os.urandom(12)

app.config['RECAPTCHA_USE_SSL'] = False
app.config['RECAPTCHA_PUBLIC_KEY'] = '6LeYIbsSAAAAACRPIllxA7wvXjIE411PfdB2gt2J'
app.config['RECAPTCHA_PRIVATE_KEY'] = '6LeYIbsSAAAAAJezaIq3Ft_hSTo0YtyeFG-JgRtu'
app.config['RECAPTCHA_OPTIONS'] = {'theme': 'white'}

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///brs.db'
db = SQLAlchemy(app)
admin = Admin(app, name='BRS Admin', template_mode='bootstrap3')

global resultnum
resultnum = 0

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

    def get_user_id(self):
        return self.id

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
        # commit deposit to database
        db.session.commit()

    # removing money from account
    def withdraw(self, amount):
        if amount >= self.balance:
            # handle error case
            print("Insufficient Funds to perform this transaction")
        else:
            self.balance -= amount
            db.session.commit()

    #
    # def __repr__(self):
    #     return dict(self)

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
    date = db.Column('date', db.DateTime)
    category = db.Column('category', db.String(120))
    image = db.Column('image', db.String(120))
    isSold = db.Column('isSold', db.Boolean)
    buyer = db.Column('buyer', db.String(120))

    ############################################################################
    ## CONSTRUCTOR
    ############################################################################
    def __init__(self, userid=0, title="", price="", descr="", date=None, category=None, image=""):
        self.userid = userid
        self.title = title
        self.price = price
        self.descr =  descr
        if date is None:
            date = datetime.utcnow()
        self.date = date
        self.category = category
        self.image = image
        self.isSold = False


    ############################################################################
    ## GETTERS
    ############################################################################
    def getPostID(self):
        return self.id

    def getUserID(self):
        return self.userid

    def getTitle(self):
        return self.title

    def getPrice(self):
        return self.price

    def getDesc(self):
        return self.desc

    def getDate(self):
        return self.date

    def getCategory(self):
        return self.category

    def getIsSold(self):
        return self.isSold

    ############################################################################
    ## SETTERS
    ############################################################################
    def setTitle(self, title):
        self.title = title
        db.session.commit()

    def setPrice(self, price):
        self.price = price
        db.session.commit()

    def setDesc(self, desc):
        self.desc = desc
        db.session.commit()

    def setCategory(self, category):
        self.category = category
        db.session.commit()

    def markSold(self):
        self.isSold = True
        db.session.commit()

    ############################################################################
    ## OTHER METHODS
    ############################################################################

##------------------------------------------------------------------------------
## Flag Model
##------------------------------------------------------------------------------
class Flag(db.Model):
    __tablename__ = "Flag"
    flagid = db.Column(db.Integer, primary_key=True)
    userid = db.Column('userid', db.Integer, db.ForeignKey("Users.id"), unique = False)
    reason = db.Column('flag_reason', db.String(120), unique=False)

    ############################################################################
    ## CONSTRUCTOR
    ############################################################################
    def __init__(self,userid=None, reason=""):
        self.userid = userid
        self.reason = reason


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
admin.add_view(ModelView(Flag, db.session))

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
        # if logged in, show index with username
        return redirect(url_for('index',
                        username=session.get('current_user')))

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
            session['current_user'] = result.email
            flash('SUCCESS: Logged In!')
            current_user = session.get('current_user')
        else:
            flash('wrong password!')
            return render_template('login.html')
        return render_template('index.html', username=current_user)
    return render_template('login.html')

# Logging Out
@app.route('/logout')
def logout():
    session['logged_in'] = False
    flash('SUCCESS: Logged Out!')
    return index()

# # Signing Up
# @app.route('/signup', methods =['GET', 'POST'])
# def signup():
#     global resultnum
#     firstnum = int(random.random() * 10)
#     secondnum = int(random.random() * 10)
#     resultnum = firstnum + secondnum
#     form = SignupForm(request.form)
#     if request.method == 'POST' and int(request.form['captcha']) == int(resultnum):
#         if form.validate():
#             email_exist = User.query.filter_by(email=form.email.data).first()
#             if email_exist:
#                 form.email.errors.append('Email already in use')
#                 return render_template('signup.html', form=form, page_title = "Sign Up")
#             else:
#                 firstname = form.firstname.data
#                 lastname = form.lastname.data
#                 email = form.email.data
#                 password = form.password.data
#                 phone = form.phone.data
#                 entry = User(email, password, firstname, lastname, phone)
#                 db.session.add(entry)
#                 db.session.commit()
#                 return render_template('success.html')
#         else:
#             firstnum = int(random.random() * 10)
#             secondnum = int(random.random() * 10)
#             resultnum = firstnum + secondnum
#             return render_template('signup.html', form=form)
#     return render_template('signup.html', form=SignupForm(), firstnum=firstnum, secondnum=secondnum)


# Signing Up
@app.route('/signup', methods =['GET', 'POST'])
def signup():
    if request.method == 'POST':
        form = SignupForm(request.form)
        if form.validate():
            email_exist = User.query.filter_by(email=form.email.data).first()
            if email_exist:
                form.email.errors.append('Email already in use')
                return render_template('signup.html', form=form, page_title = "Sign Up")
            else:
                firstname = form.firstname.data
                lastname = form.lastname.data
                email = form.email.data
                password = form.password.data
                phone = form.phone.data
                entry = User(email, password, firstname, lastname, phone)
                db.session.add(entry)
                db.session.commit()
                flash('You have sucessfully signed up and will have access shortly! Thank you for your patience')
                return render_template('index.html')
        else:
            return render_template('signup.html', form=form)
    return render_template('signup.html', form=SignupForm())

@app.route('/post', methods = ['GET', 'POST'])
def post():
    if request.method == 'POST':
        form = PostForm(request.form)
        if form.validate():
            title = form.title.data
            price = form.price.data
            descr = form.descr.data
            image = form.image.data
            date = datetime.utcnow()
            category = form.category.data
            entry = Post(1,title, price, descr, date, category, image)
            db.session.add(entry)
            db.session.commit()
            flash('Item Posted!')
            return render_template('index.html')
        else:
            return render_template('post.html', form=form)
    return render_template('post.html', form=PostForm(),
                                username=session.get('current_user'))

if (__name__)=='__main__':
    app.run(host='localhost', port=5000, debug=True)

# User profile pages accessible by /user/id
@app.route('/user/<id>', methods=['GET', 'POST'])
#@login_required
def user(id):
    user = User.query.filter_by(id=id).first()
    post = Post.query.filter_by(userid=user.id)
    # TODO: update so this form so that it only shows up on the current_user's
    # profile
    if request.method == 'POST':
        deposit = request.form['deposit']
        withdraw = request.form['withdraw']
        # profile = User.query.filter_by(id=id).first()
        # profile.deposit(deposit)
        # profile.withdraw(withdraw)
        return render_template('index.html', username=session.get('current_user'))

    user = User.query.filter_by(id=id).first()
    post = Post.query.filter_by(userid=user.id)
    return render_template('user_profile.html',
                            username=session.get('current_user'),
                            user=user, post=post)

@app.route('/item/<id>', methods=['GET', 'POST'])
def item(id):
    item = Post.query.filter_by(id=id).first()
    current_user = session.get('current_user')
    if request.method == 'POST':
        if not session.get('logged_in'):
            flash('ERROR: You must be logged in to buy an item!')
            return render_template('item.html', item=item)
        query = User.query.filter(User.email==current_user)
        buyer = query.first()
        buyer.withdraw(int(item.getPrice()))
        # get seller
        seller = User.query.filter(User.id==item.getUserID()).first()
        # deposit money to seller
        seller.deposit(int(item.getPrice()))
        # mark item as sold
        item.markSold()
        return str(buyer.balance)
    return render_template('item.html', username=session.get('current_user'), item=item)

@app.route('/showPosts', methods=['GET', 'POST'])
def show_entries():
    if request.method == 'POST':
        CATEGORY = str(request.form['filter'])
        flash('Filter: %s Selected!' % CATEGORY)
        entries = Post.query.filter(Post.category==CATEGORY)
        filtered = entries.order_by(Post.date.desc())
        if not session.get('logged_in'):
            return render_template('show_entries.html', entries=filtered)
        return render_template('show_entries.html', entries=filtered,
                                username=session.get('current_user'))
    entries = Post.query.order_by(Post.date.desc())
    if not session.get('logged_in'):
        return render_template('show_entries.html', entries=entries)
    return render_template('show_entries.html', entries=entries,
                            username=session.get('current_user'))
