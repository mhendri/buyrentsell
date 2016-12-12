from flask import Flask
from flask import flash, redirect, render_template, request, session, abort, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_login import LoginManager, login_user, logout_user, login_required, current_user


from forms import *
import random

import os

# for datetime
from datetime import datetime

# Database Imports
from sqlalchemy.orm import sessionmaker

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

# Flask-Login Login Manager
lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'

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
    image = db.Column('image', db.String(220))
    active = db.Column('active', db.Boolean, unique=False)
    # authenticated for flask-login
    authenticated = db.Column(db.Boolean, default=False)

    ############################################################################
    ## CONSTRUCTOR
    ############################################################################
    def __init__(self, email="", password="", firstname="", lastname="", phone="", image=""):
        ''' '''
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.password = password
        self.phone = phone
        self.balance = 0
        self.image = image
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
        db.session.commit()

    def set_phone(self, phone):
        self.phone = phone
        db.session.commit()

    # unsure about this setter / may not be needed
    def set_balance(self, balance):
        self.balance = balance
        db.session.commit()

    def activate_user(self):
        self.active = True
        db.session.commit()

    def suspend_user(self):
        self.active = False
        db.session.commit()

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
            return False
        else:
            self.balance -= amount
            db.session.commit()
            return True

    ############################################################################
    ## Flask-Login Methods
    ############################################################################
    def is_active(self):
        return self.active

    def get_id(self):
        return self.id

    def is_authenticated(self):
        return self.authenticated

    def is_anonymous(self):
        ''' False, as anonymous users aren't supported. '''
        return False

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

    # TODO: Need to add few more things:
    # buyer_id, (is_biddable, current_bid, time_limit), date_posted, is_reported, image


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

    def updateBuyer(self, purchaser):
        self.buyer = purchaser
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
    email = db.Column('email', db.String(120), unique=False)
    reason = db.Column('flag_reason', db.String(120), unique=False)

    ############################################################################
    ## CONSTRUCTOR
    ############################################################################
    def __init__(self,userid, email, reason=""):
        self.userid = userid
        self.email = email
        self.reason = reason

    # def report_user(self, reason, userid):
    #     self.reason = reason
    #     self.userid = userid
    #     db.session.commit()

################################################################################
## FLASK-ADMIN
################################################################################

admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Post, db.session))
admin.add_view(ModelView(Flag, db.session))

################################################################################
## FLASK-LOGIN
################################################################################
#!py
@lm.user_loader
def user_loader(id):
    ''' Given *od*, return the associated User object. '''
    return User.query.filter(User.id==id).first()

# @lm.unauthorized_handler
# def unauthorized_handler():
#     return 'Unauthorized'

################################################################################
## ROUTES
################################################################################

# Set "homepage" to index.html
@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title="Home")

# Logging In
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = str(request.form['email'])
        password = str(request.form['password'])
        query = User.query.filter(User.email==email, User.password==password)
        user = query.first()

        if user:
            if not user.is_active():
                flash ('Account not yet active, please wait for admin')
                return render_template('login.html')
            user.authenticated = True
            db.session.add(user)
            db.session.commit()
            login_user(user, True)
            flash('SUCCESS: Logged In!')
            next = request.args.get('next')

            # # is_safe_url should check if the url is safe for redirects.
            # # See http://flask.pocoo.org/snippets/62/ for an example.
            # if not is_safe_url(next):
            #     return abort(400)

            return redirect(next or url_for('index'))
        else:
            flash('The email address/password you provided were not found!')
            return render_template('login.html')
    return render_template('login.html')

# NOTE: example of login required route
# @app.route('/protected')
# @login_required
# def protected():
#     return 'Logged in as: ' + current_user.firstname

# Logging Out
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('SUCCESS: Logged Out!')
    return redirect(url_for('index'))

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
                image = form.image.data
                entry = User(email, password, firstname, lastname, phone, image)
                db.session.add(entry)
                db.session.commit()
                flash('You have sucessfully signed up and will have access shortly! Thank you for your patience')
                return render_template('index.html')
        else:
            return render_template('signup.html', form=form)
    return render_template('signup.html', form=SignupForm())

@app.route('/post', methods = ['GET', 'POST'])
@login_required
def post():
    if request.method == 'POST':
        form = PostForm(request.form)
        if form.validate():
            userid = current_user.email
            title = form.title.data
            price = form.price.data
            descr = form.descr.data
            image = form.image.data
            date = datetime.utcnow()
            category = form.category.data
            entry = Post(userid,title, price, descr, date, category, image)
            db.session.add(entry)
            db.session.commit()
            flash('Item Posted!')
            return render_template('index.html')
        else:
            flash('Item failed to post')
            return render_template('post.html', form=form)
    return render_template('post.html', form=PostForm())

# User profile pages accessible by /user/id
@app.route('/user/<id>', methods=['GET', 'POST'])
def user(id):

    user = User.query.filter_by(id=id).first()
    post = Post.query.filter_by(userid=user.id)
    # TODO: update so this form so that it only shows up on the current_user's
    # profile
    if request.method == 'POST':
        form = ProfileForm(request.form)
        if form.validate():
            deposit = form.deposit.data
            withdraw = form.withdraw.data
            user_profile = User.query.filter(User.id==user.id).first()
            user_profile.deposit(int(deposit))
            user_profile.withdraw(int(withdraw))
            flash("Done")
            return render_template('index.html')
        else:
            flash("Try again")
    return render_template('user_profile.html', user=user, post=post, form=ProfileForm())

@app.route('/item/<id>', methods=['GET', 'POST'])
def item(id):
    item = Post.query.filter_by(id=id).first()
    item_userid = User.query.filter_by(id=item.userid).first()
    current_user = session.get('current_user')
    if request.method == 'POST':
        if not session.get('logged_in'):
            flash('ERROR: You must be logged in to buy an item!')
            return render_template('item.html', item=item, item_userid=item_userid)
        query = User.query.filter(User.email==current_user)
        buyer = query.first()
        if buyer.withdraw(int(item.getPrice())) == True:
            # get seller
            seller = User.query.filter(User.id==item.getUserID()).first()
            # deposit money to seller
            seller.deposit(int(item.getPrice()))
            # mark item as sold
            item.markSold()
            item.updateBuyer(buyer.email)
            flash(item.title + ' succesfully purchased!')
            return redirect(url_for('show_entries'))
        else:
            flash('Insufficient funds to purchase ' + item.title + '. Try selling some stuff! ')
            return redirect(url_for('show_entries'))
    return render_template('item.html', item=item, item_userid=item_userid)

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
                                )
    entries = Post.query.order_by(Post.date.desc())
    if not session.get('logged_in'):
        return render_template('show_entries.html', entries=entries)
    return render_template('show_entries.html', entries=entries)

# NOTE: may want to make this logged_in only
@app.route('/item/<id>/reportUser', methods=['GET', 'POST'])
@login_required
def reportUser(id):
    item = Post.query.filter_by(id=id).first()
    if request.method == 'POST':
        seller = User.query.filter(User.id==item.getUserID()).first()
        reason = request.form['reason']
        flag = Flag(seller.id, seller.email, reason)
        db.session.add(flag)
        db.session.commit()
        check_ban = Flag.query.filter(User.id==seller.id)
        if check_ban.count() > 2:
            seller.active = False
            db.session.commit()
        flash('Your flagging of '+ seller.email + ' is under review!')
        return redirect(url_for('show_entries'))
    return render_template('report_user.html')
