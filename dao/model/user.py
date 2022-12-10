from marshmallow import fields, Schema

from setup_db import db


class User(db.Model):
	__tablename__ = 'user'
	# id = db.Column(db.Integer, primary_key=True)
	# username = db.Column(db.String)
	# password = db.Column(db.String)
	# role = db.Column(db.String)

	id = db.Column(db.Integer, primary_key=True)
	role = db.Column(db.String)
	username = db.Column(db.String)
	password = db.Column(db.String)
	name = db.Column(db.String)
	surname = db.Column(db.String)
	favorite_genre = db.Column(db.String)

	email = db.Column(db.String, unique=True)


class UserSchema(Schema):
	# id = fields.Int()
	# username = fields.Str()
	# password = fields.Str()
	# role = fields.Str()

	id = fields.Int()
	email = fields.Str()
	password = fields.Str()
	name = fields.Str()
	surname = fields.Str()
	favorite_genre = fields.Str()
	role = fields.Str()
	username = fields.Str()
