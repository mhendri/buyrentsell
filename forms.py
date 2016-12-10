from flask_wtf import Form
from wtforms import *

class ContactForm(Form):
    name = TextField("Name Of Student")
