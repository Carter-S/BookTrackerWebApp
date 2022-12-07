from app import app, db
from app.models import User, Book, userToBook
from flask import Flask, render_template, request, redirect, flash, url_for, jsonify
from app.forms import loginForm, registerForm, addBookForm, findBooksForm, changePasswordForm
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import or_
import logging
from datetime import datetime

app.config["REMEMBER_COOKIE_DURATION"] = 30

app.config["SECRET_KEY"] = "secret-key"

@app.route("/")
def index():
	app.logger.info('index route request')
	if current_user.is_authenticated:
		return redirect(url_for("myBooks"))
	else:
		return redirect(url_for("login"))

loginManager = LoginManager()
loginManager.init_app(app)

@loginManager.user_loader
def load_user(user_id):
	loginManager._update_remember_cookie = True;
	return User.query.get(int(user_id))

@app.route("/login", methods=["GET", "POST"])
def login():
	form = loginForm()
	if(request.method == "POST"):
		user = User.query.filter_by(email=form.email.data).first()
		if user != None:
			if check_password_hash(user.password_hash, form.password.data):
				if(form.rememberMe.data==True):
					login_user(user, remember=True)
				else:
					login_user(user, remember=False)
				return redirect(url_for("myBooks"))
			else:
				flash("Incorrect password!")
				app.logger.info(str(datetime.now())+": entered incorrect password!")
		else:
			flash("Invalid email!")
			app.logger.info(str(datetime.now())+": User entered incorrect email!")
	return render_template("login.html", title="Login", form=form)

@app.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
	logout_user()
	return redirect(url_for("login"))

@app.route("/register", methods=["GET", "POST"])
def register():
	form = registerForm()
	if request.method == "POST":
		if User.query.filter_by(email=form.email.data).first() == None:
			hashed_pw = generate_password_hash(form.password.data, "sha256")
			user = User(firstName=form.firstName.data, lastName=form.lastName.data, email=form.email.data, password_hash=hashed_pw)
			try:
				db.session.add(user)
				db.session.commit()
			except:
				app.logger.error(str(datetime.now())+": ERROR! Failed to add new user")
			return redirect(url_for("login"))
		else:
			flash("Email already used")
			return render_template("register.html", title="Register", form=form)
	else:
		return render_template("register.html", title="Register", form=form)

@app.route("/myBooks", methods=["GET", "POST"])
@login_required
def myBooks():
	form = findBooksForm()
	user = db.session.query(User).filter(User.id==current_user.id).first()
	books=user.books
	
	if(request.method=="POST"):
		if(form.searchString.data!=""):
			resultBooks=[]
			for b in books:
				if b.name==form.searchString.data or b.author==form.searchString.data:
					resultBooks.append(b)
			return render_template("myBooks.html", title="My Books", data=resultBooks, form=form)
	return render_template("myBooks.html", title="My Books", data=books, form=form)

@app.route("/addBook", methods=["GET", "POST"])
@login_required
def addBook():
	form = addBookForm()
	if request.method == "POST":
		book = Book.query.filter_by(name=form.name.data, author=form.author.data).first()
		if(book == None):
			book = Book(name=form.name.data, author=form.author.data)
			db.session.add(book)
		current_user.books.append(book)
		db.session.commit()
		form.name.data = ""
		form.author.data = ""
	return render_template("addBook.html", title="Add book", form=form)

@app.route("/allBooks", methods=["GET", "POST"])
@login_required
def allBooks():
	form = findBooksForm()
	books = Book.query.all()
	if(request.method=="POST"):
		if(form.searchString.data!=""):
			resultBooks=[]
			for b in books:
				if b.name==form.searchString.data or b.author==form.searchString.data:
					resultBooks.append(b)
			return render_template("allBooks.html", title="My Books", data=resultBooks, form=form)
	return render_template("allBooks.html", title="All books", books=books, form=form)

@app.route("/myAccount", methods=["GET", "POST"])
@login_required
def myAccount():
	form = changePasswordForm()
	if request.method == "POST":
		if check_password_hash(current_user.password_hash, form.currentPassword.data):
			User.query.filter_by(id=current_user.id).update({"password_hash": generate_password_hash(form.newPassword.data)})
			db.session.commit()
		else:
			flash("Current password was entered incorrectly")
			app.logger.error(str(datetime.now()) + ": " + str(current_user.id) + " entered current password incorrectly")
	return render_template("myAccount.html", title="My Account", form=form, user=current_user)