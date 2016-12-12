from flask_wtf import Form, RecaptchaField
from wtforms import TextField, IntegerField, TextAreaField, SubmitField, RadioField, SelectField, PasswordField, DecimalField

from wtforms import validators, ValidationError

class SignupForm(Form):
	firstname = TextField("First Name", [validators.Required("Please enter your first name.")])
	lastname = TextField("Last Name", [validators.Required("Please enter your last name.")])
	email = TextField("Email",[validators.Required("Please enter your email address."),
		validators.Email("Please enter your email address")])
	password = PasswordField("Passsword", [validators.Required("Please enter a password.")])
	phone = IntegerField("Phone", [validators.Required("Please enter a phone number.")])
	submit = SubmitField("Send")
	recaptcha = RecaptchaField()

class PostForm(Form):
	title = TextField("Title", [validators.Required("Please enter the item name.")])
	price = DecimalField("Price", [validators.Required("Please enter a starting price.")])
	descr = TextAreaField("Description", [validators.Required("Please enter a description.")])
	image = TextField("Image", [validators.Required("Please upload an image")])
	category = SelectField("Select Category", choices=[("Electronic", "Electronic"), ("Furniture", "Furniture"), ("Clothing", "Clothing"), ("Appliance", "Appliance"), ("Sports", "Sports")])
	submit = SubmitField("Send")

class ProfileForm(Form):
	deposit = DecimalField('Deposit', [validators.Required("Please enter deposit amount.")])
	withdraw = DecimalField('Withdraw', [validators.Required("Please enter withdraw amount.")])
	submit = SelectField("Send")