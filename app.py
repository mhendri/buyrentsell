from flask import Flask
from flask import render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask import url_for
from flask.ext.login import LoginManager

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/brs'
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)

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

    def get_id(self):
        return unicode(self.id)

    def is_active(self):
        return self._user.enabled

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True

    def __repr__(self):
        return '<E-mail %r>' % self.email

@login_manager.user_loader
def load_user(user_id):
    user = User.query.get(user_id)
    if user:
        return User(user)
    else:
        return None

# Set "homepage" to index.html
@app.route('/', methods =['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/showSignUp', methods =['GET'])
def showSignUp():
    return render_template('signup.html')

@app.route('/success', methods =['GET', 'POST'])
def success():
    if request.method == 'POST':
        email = request.form['inputEmail']
        name = request.form['inputName']
        password = request.form['inputPassword']
        phone =  request.form['phoneNumber']
        if not db.session.query(User).filter(User.email == email).count():
            entry = User(name,email,phone,password)
            db.session.add(entry)
            db.session.commit()
            return render_template('success.html')
    return render_template('success.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    next = request.args.get('next')
    if request.method == 'POST':
        username = request.form['inputEmail']
        password = request.form['inputPassword']
        if authenticate(app.config['AUTH_SERVER'], username, password):
            user = User.query.filter_by(username=username) #.first()
            if user:
                if login_user(User(user)):
                    # do stuff
                    flash("You have logged in")
                    return redirect(next or url_for('success', error=error))
        error = "Login failed"
    return render_template('login.html', login=True, next=next, error=error)



if (__name__)=='__main__':
	app.run(host='local host', port=5555, debug=True)