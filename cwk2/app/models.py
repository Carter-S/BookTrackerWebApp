from app import db
from flask_login import UserMixin

userToBook = db.Table(
				"userToBook",
				db.Column("userId", db.Integer, db.ForeignKey("user.id"), primary_key=True),
				db.Column("bookId", db.Integer, db.ForeignKey("book.id"), primary_key=True)
			)

class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	firstName = db.Column(db.String(30))
	lastName= db.Column(db.String(30))
	email = db.Column(db.String(100), unique=True)
	password_hash = db.Column(db.String(128))
	books = db.relationship("Book", secondary=userToBook, backref="readBy")

class Book(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(100))
	author = db.Column(db.String(100))

class Review(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	firstName = db.Column(db.String(30))
	reviewText = db.Column(db.String(5000))
	rating = db.Column(db.Integer)
	bookTitle = db.Column(db.String(100))