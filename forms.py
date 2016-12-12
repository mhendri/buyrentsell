from flask_wtf import Form, RecaptchaField
from wtforms import TextField, IntegerField, TextAreaField, SubmitField, RadioField, SelectField, PasswordField, DecimalField

from wtforms.fields.html5 import EmailField

from wtforms import validators, ValidationError

class SignupForm(Form):
	firstname = TextField("First Name", [validators.Required("Please enter your first name.")])
	lastname = TextField("Last Name", [validators.Required("Please enter your last name.")])
	email = TextField("Email", [validators.Required("Please enter your email address."),
		validators.Email("Please enter your email address")])
	password = PasswordField("Passsword", [validators.Required("Please enter a password.")])
	phone = IntegerField("Phone", [validators.Required("Please enter a phone number.")])
	image = TextField("Image", [validators.Required("Please upload an image")])
	submit = SubmitField("Send")
	recaptcha = RecaptchaField()

class PostForm(Form):
	title = TextField("Title", [validators.Required("Please enter the item name.")])
	price = DecimalField("Price", [validators.Required("Please enter a starting price.")])
	descr = TextAreaField("Description", [validators.Required("Please enter a description.")])
	image = TextField("Image", [validators.Required("Please upload an image")])
	category = SelectField("Select Category", choices=[("electronic", "Electronic"), ("furniture", "Furniture"), ("clothing", "Clothing"), ("appliance", "Appliance"), ("sports", "Sports")])
	submit = SubmitField("Send")

class LoginForm(Form):
	email = EmailField("Email", [validators.Required()])
	password = PasswordField("Password", [validators.Required()])
	recaptcha = RecaptchaField()
	submit = SubmitField("Log In")

class ProfileForm(Form):
	deposit = TextField('Deposit', [validators.Required("Please enter deposit amount.")])
	withdraw = TextField('Withdraw', [validators.Required("Please enter withdraw amount.")])
	submit = SubmitField("Send")

class RateForm(Form):
	rating = RadioField("Rating", [validators.Required("Please select a rating.")], choices=[("1", "1"), ("2", "2"), ("3", "3"), ("4", "4"), ("5", "5")])
	comment = TextAreaField("Comment")
	submit = SubmitField("Rate")
