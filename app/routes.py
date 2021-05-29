from flask import Flask, render_template, request, flash, redirect, url_for, jsonify
from app.models import Pages, Meta_Content, User
from app.utils import save_picture
from app import app, login, db
import os
from flask_login import current_user, login_user, logout_user, login_required
from app.form import LoginForm

@login_required
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


		image_path = url_for('static', filename = 'crop_images/{}'.format(meta_obj.og_image))

	else:

		image_path = None

	return render_template('index.html', page=meta_obj, image_path=image_path)


@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():

	if current_user.is_authenticated:

		return redirect(url_for('admin'))

	form = LoginForm()

	if form.validate_on_submit():

		user = User.query.filter_by(username=form.username.data).first()

		if user is None or not user.check_password(form.password.data):

			flash('Incorrect Login Details')

			return redirect(url_for('admin_login'))

		login_user(user, remember=form.remember_me.data)

		return redirect(url_for('admin'))

	return render_template('login.html', form=form)


@app.route('/admin/logout')
def admin_logout():

	logout_user()

	return redirect(url_for('admin_login'))







@app.route('/admin')
@login_required
def admin():

	return redirect(url_for('pages'))


@app.route('/admin/pages')
@login_required
def pages():


	page_names = Pages.query.all()

	return render_template('pages.html', page_names=page_names)


@app.route('/privacy-policy')
def privacy_policy():

	page = Pages.query.filter_by(page_name='Privacy Policy').first()




	meta_obj = page.metaContent[0]

	if meta_obj.og_image:

		image_path = url_for('static', filename = 'crop_images/{}'.format(meta_obj.og_image))

	else:

		image_path = None

	return render_template('privacy_policy.html', page=meta_obj, image_path=image_path)


@app.route('/fees_ISA')
def fees_page():

	page = Pages.query.filter_by(page_name='Fees and ISA').first()

	meta_obj = page.metaContent[0]

	if meta_obj.og_image:

		image_path = url_for('static', filename = 'crop_images/{}'.format(meta_obj.og_image))

	else:

		image_path = None

	return render_template('privacy_policy.html', page=meta_obj, image_path=image_path)

@app.route('/terms_conditions')
def terms_conditions():

	page = Pages.query.filter_by(page_name='Terms and Conditions').first()



	meta_obj = page.metaContent[0]


	if meta_obj.og_image:

		image_path = url_for('static', filename = 'crop_images/{}'.format(meta_obj.og_image))

	else:

		image_path = None

	return render_template('terms_conditions.html', page=meta_obj, image_path=image_path)


@login_required
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

@login_required
@app.route('/flash_messages')
def flash_messages():

	message = request.args.get('message')

	flash(message)

	return jsonify({'message':'done'})


@login_required
@app.route('/admin/metaContent/edit', methods=['GET', 'POST'])
def metaContent_edit():


	data = request.form

	page = Pages.query.filter_by(page_name=data['page_name']).first()

	for key in data:

		print(key, data[key])

	
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


@login.user_loader
def load_user(id):

	return User.query.get(int(id))







