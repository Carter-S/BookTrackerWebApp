from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, EmailField
from wtforms.validators import DataRequired, EqualTo, Email, Length

class loginForm(FlaskForm):
	email = EmailField("Email: ", validators=[DataRequired()])
	password = PasswordField("Password: ", validators=[DataRequired()])
	rememberMe = BooleanField("Remember me")
	submit = SubmitField("Login")

class registerForm(FlaskForm):
	firstName = StringField("First name: ", validators=[DataRequired()])
	lastName = StringField("Last name: ", validators=[DataRequired()])
	email = EmailField("Email: ", validators=[DataRequired()])
	password = PasswordField("Password: ", validators=[DataRequired(), EqualTo("confirmPassword", message="Passwords must match")])
	confirmPassword = PasswordField("Confirm password: ", validators=[DataRequired()])
	submit = SubmitField("Register")

class addBookForm(FlaskForm):
	name = StringField("Name of book: ", validators=[DataRequired()])
	author = StringField("Author: ", validators=[DataRequired()])
	submit = SubmitField("Add book")

class findBooksForm(FlaskForm):
	searchString = StringField(validators=[])
	submit = SubmitField("Search")

class changePasswordForm(FlaskForm):
	currentPassword = PasswordField("Current password: ", validators=[DataRequired()])
	newPassword = PasswordField("New password: ", validators=[DataRequired()])
	confirmPassword = PasswordField("Confirm new password: ", validators=[DataRequired()])
	submit = SubmitField("Change password")