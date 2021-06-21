from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from hashlib import md5

class User(db.Model, UserMixin):

	id = db.Column(db.Integer, primary_key=True)

	username = db.Column(db.String(55), unique=True)

	name = db.Column(db.String(55))

	email = db.Column(db.String(255), unique=True)

	phone = db.Column(db.String(25))

	password_hash = db.Column(db.String(255))

	def __repr__(self):

		return "{}".format(self.username)

	def check_password(self, password):

		return check_password_hash(self.password_hash, password)

	def set_password(self, password):

		self.password_hash = generate_password_hash(password)

class Pages(db.Model):

	id = db.Column(db.Integer, primary_key=True)

	page_name = db.Column(db.String(25))

	page_url = db.Column(db.String(55))

	view_function = db.Column(db.String(55))

	slug = db.Column(db.String(55))

	metaContent = db.relationship('Meta_Content', backref='page')

	def __repr__(self):

		return '{}'.format(self.page_name)



class Meta_Content(db.Model):

	id = db.Column(db.Integer, primary_key=True)

	page_id = db.Column(db.Integer, db.ForeignKey('pages.id', ondelete='CASCADE'))
	
	title = db.Column(db.String(55))

	description = db.Column(db.String(255))

	keywords = db.Column(db.String(255))

	og_type = db.Column(db.String(55))

	og_title = db.Column(db.String(55))

	og_description = db.Column(db.String(255))

	og_image = db.Column(db.String(255))

	canonical = db.Column(db.String(255))

	robots = db.Column(db.String(255))



class Elements(db.Model):

	id = db.Column(db.Integer, primary_key=True)

	page_id = db.Column(db.Integer, db.ForeignKey('pages.id'))

	element_type = db.Column(db.String(255))

	text = db.Column(db.Text)

	query_selector = db.Column(db.String(255))

	attributes = db.relationship('Attributes', backref='element')

class Attributes(db.Model):

	id = db.Column(db.Integer, primary_key=True)

	element_id = db.Column(db.Integer, db.ForeignKey('elements.id'))

	attribute = db.Column(db.String(255))

	attribute_value = db.Column(db.String(255))


class Styles(db.Model):

	id = db.Column(db.Integer, primary_key=True)

	element_id = db.Column(db.Integer, db.ForeignKey('elements.id'))

	style_attr = db.Column(db.String(255))

	style_value = db.Column(db.String(255))













