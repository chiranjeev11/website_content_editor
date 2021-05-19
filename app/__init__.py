from flask import Flask, render_template, request, flash, redirect, url_for, jsonify
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf import FlaskForm
import os
import secrets
from PIL import Image
from io import BytesIO
import base64


app = Flask(__name__)


app.config.from_object(Config)

db = SQLAlchemy(app)

migrate = Migrate(app, db)





class Pages(db.Model):

	id = db.Column(db.Integer, primary_key=True)

	page_name = db.Column(db.String(25))

	page_url = db.Column(db.String(55))

	is_model = db.Column(db.Integer)

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

def save_picture(form_picture):

	form_picture = form_picture.split(",")[1]
	form_picture = BytesIO( base64.b64decode(form_picture) )

	random_hex = secrets.token_hex(8)

	f_ext = '.png'

	picture_fn = random_hex + f_ext

	picture_path = os.path.join(app.root_path, 'static/crop_images', picture_fn)

	output_size = (125, 125)

	img = Image.open(form_picture)

	img.thumbnail(output_size)

	img.save(picture_path)

	return picture_fn

@app.route('/admin/og-picture', methods=['GET', 'POST'])
def save_og_image():

	image = request.form['image']

	data  = image.split(';')

	if len(data)>1:

		a = save_picture(image)

		return jsonify({'image_name':a})

	return jsonify({'image_name':None})


@app.route('/')
def index():

	page = Pages.query.filter_by(page_name='Home Page').first()


	meta_obj = page.metaContent[0]

	if meta_obj.og_image:

		image_path = '/static/crop_images/' + meta_obj.og_image

	else:

		image_path = None

	return render_template('index.html', page=meta_obj, image_path=image_path)



@app.route('/admin')
def admin():

	return render_template('admin.html')

@app.route('/admin/pages')
def pages():


	page_names = Pages.query.all()

	return render_template('pages.html', page_names=page_names)

@app.route('/privacy-policy')
def privacy_policy():

	page = Pages.query.filter_by(page_name='Privacy Policy').first()




	meta_obj = page.metaContent[0]

	if meta_obj.og_image:

		image_path = '/static/crop_images/' + meta_obj.og_image

	else:

		image_path = None

	return render_template('privacy_policy.html', page=meta_obj, image_path=image_path)

@app.route('/fees_ISA')
def fees_page():

	page = Pages.query.filter_by(page_name='Fees and ISA').first()

	meta_obj = page.metaContent[0]

	if meta_obj.og_image:

		image_path = '/static/crop_images/' + meta_obj.og_image

	else:

		image_path = None

	return render_template('privacy_policy.html', page=meta_obj, image_path=image_path)

@app.route('/terms_conditions')
def terms_conditions():

	page = Pages.query.filter_by(page_name='Terms and Conditions').first()



	meta_obj = page.metaContent[0]


	if meta_obj.og_image:

		image_path = '/static/crop_images/' + meta_obj.og_image

	else:

		image_path = None

	return render_template('terms_conditions.html', page=meta_obj, image_path=image_path)


@app.route('/admin/pages/edit-request', methods=['GET', 'POST'])
def pages_edit_request():

	if request.form:

		data = request.form['data']



	else:

		data = request.args.get('page_name')


	page = Pages.query.filter_by(page_name=data).first()

	if page.metaContent:

		meta_obj=page.metaContent[0]
	else:

		meta_obj = {}

	if meta_obj:

		formData = {'page_name':page.page_name,
					'page_url':'localhost:5000'+page.page_url,
					'meta_title':meta_obj.title,
					'meta_description':meta_obj.description,
					'meta_keywords':meta_obj.keywords,
					'meta_robots':meta_obj.robots,
					'meta_canonical':meta_obj.canonical,
					'og_type':meta_obj.og_type,
					'og_title':meta_obj.og_title,
					'og_description':meta_obj.og_description,
					'og_image':meta_obj.og_image
					}
	else:

		formData = {'page_name':page.page_name,'page_url':page.page_url}

	return jsonify(formData)

@app.route('/flash_messages')
def flash_messages():

	message = request.args.get('message')

	flash(message)

	return jsonify({'message':'done'})



@app.route('/admin/metaContent/edit', methods=['GET', 'POST'])
def metaContent_edit():


	data = request.form

	page = Pages.query.filter_by(page_name=data['page_name']).first()

	
	if page.metaContent:

		meta_obj = page.metaContent[0]
		
		meta_obj.title = data['meta_title']

		meta_obj.description = data['meta_description']

		meta_obj.keywords = data['meta_keywords']

		meta_obj.robots = data['meta_robots']

		meta_obj.canonical = data['canonical']

		meta_obj.og_type = data['og_type']

		meta_obj.og_title = data['og_title']

		meta_obj.og_description = data['og_description']

		if data['image_name']:

			if meta_obj.og_image:

				image_path = os.path.join(app.root_path, 'static/crop_images', meta_obj.og_image)

				os.remove(image_path)

			meta_obj.og_image = data['image_name']

		db.session.add(meta_obj)

		db.session.commit()

		


	else:


		meta_obj = Meta_Content(title=data['meta_title'], description=data['meta_description'], keywords=data['meta_keywords'], robots=data['meta_robots'], canonical=data['canonical'], og_type=data['og_type'], og_title=data['og_title'], og_description=data['og_description'], page=page)

		db.session.add(meta_obj)

		db.session.commit()

	flash('Your changes have been saved')


	return redirect(url_for('pages'))



@app.context_processor
def inject_pages():

	base_page_names = Pages.query.all()

	return dict(base_page_names=base_page_names)



















