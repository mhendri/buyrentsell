from flask_wtf import Form, RecaptchaField
from wtforms import TextField, IntegerField, TextAreaField, SubmitField, RadioField, SelectField, PasswordField

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
