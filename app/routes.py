from flask import Flask, render_template, request, flash, redirect, url_for, jsonify, Response
from app.models import Pages, Meta_Content, User, Elements, Attributes
from app.utils import save_picture
from app import app, login, db
import os
from flask_login import current_user, login_user, logout_user, login_required
from app.form import LoginForm, ChangePasswordForm, EditProfileForm



@app.route('/sitemap.xml')
def sitemap():

	xml = render_template('sitemap.xml')

	return Response(xml, mimetype='application/xml')

	

@app.route('/robots.txt')
def robots():

	return render_template('robots.txt')

@app.route('/')
def index():

	page = Pages.query.filter_by(page_name='Home Page').first()

	elements = Elements.query.filter_by(page_id=page.id).all()

	query_selectors = {}

	for element in elements:

		query_selectors[element.query_selector] = element.text

	meta_obj = page.metaContent[0]

	if meta_obj.og_image:


		image_path = url_for('static', filename = 'crop_images/{}'.format(meta_obj.og_image))

	else:

		image_path = None

	return render_template('index.html', page=meta_obj, image_path=image_path, query_selectors=query_selectors)


@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():

	if current_user.is_authenticated:

		return redirect(url_for('admin'))

	form = LoginForm()

	if form.validate_on_submit():

		user = User.query.filter_by(username=form.username.data).first()

		if user is None or not user.check_password(form.password.data):

			flash('Incorrect Login Details', 'error')

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

	return render_template('pages.html', page_names=page_names, title="Pages")


@app.route('/privacy-policy')
def privacy_policy():

	page = Pages.query.filter_by(page_name='Privacy Policy').first()




	meta_obj = page.metaContent[0]

	if meta_obj.og_image:

		image_path = url_for('static', filename = 'crop_images/{}'.format(meta_obj.og_image))

	else:

		image_path = None

	return render_template('privacy_policy.html', page=meta_obj, image_path=image_path, title='Privacy Policy')


@app.route('/fees_ISA')
def fees_page():

	page = Pages.query.filter_by(page_name='Fees and ISA').first()

	meta_obj = page.metaContent[0]

	if meta_obj.og_image:

		image_path = url_for('static', filename = 'crop_images/{}'.format(meta_obj.og_image))

	else:

		image_path = None

	return render_template('fees.html', page=meta_obj, image_path=image_path, title="Fees and ISA")

@app.route('/terms_conditions')
def terms_conditions():

	page = Pages.query.filter_by(page_name='Terms and Conditions').first()



	meta_obj = page.metaContent[0]


	if meta_obj.og_image:

		image_path = url_for('static', filename = 'crop_images/{}'.format(meta_obj.og_image))

	else:

		image_path = None

	return render_template('terms_conditions.html', page=meta_obj, image_path=image_path, title="Terms and Conditions")


@app.route('/admin/pages/editContent', methods=['GET', 'POST'])
@login_required
def edit_Content():

	if request.form:

		element_html = request.form['element_html']

		element_selector = request.form['element-selector']

		element = Elements.query.filter_by(query_selector=element_selector).first()

		for attribute in element.attributes:

			attribute.attribute_value = request.form[attribute.attribute]

			db.session.add(attribute)

		element.text = element_html

		db.session.add(element)

		db.session.commit()

		flash('Content updated succesfully', 'message')

	

	return render_template('editContent.html', title="Edit Content")




@app.route('/admin/pages/contentResuest', methods=['GET', 'POST'])
@login_required
def content_Request():

	elements = Elements.query.filter_by(page_id=7).all()

	query_selectors = {}

	for element in elements:

		attributes = {}

		for attribute in element.attributes:

			attributes[attribute.attribute] = attribute.attribute_value

		query_selectors[element.query_selector] = [element.text, attributes]

	return jsonify({'query_selectors':query_selectors})


@app.route('/admin/pages/loadContentRequest', methods=['GET', 'POST'])
@login_required
def loadContentRequest():

	selector = request.form['data']

	element = Elements.query.filter_by(query_selector=selector).first()

	text = element.text

	return jsonify({'text':text})

@app.route('/admin/pages/addAttributesRequest', methods=['GET', 'POST'])
@login_required
def add_attributes_request():

	query_selectors = request.json['data']

	for query_selector in query_selectors:

		element = Elements.query.filter_by(query_selector=query_selector).first()

		attributes = query_selectors[query_selector]

		for attribute in attributes:

			attr = Attributes(element_id=element.id, attribute=attribute, attribute_value=attributes[attribute])

			db.session.add(attr)

	db.session.commit()

	return jsonify({'result':'done'})


@app.route('/admin/pages/addelementsRequest', methods=['GET', 'POST'])
@login_required
def add_elements_request():

	query_selectors = request.json['data']

	for query_selector in query_selectors:

		element = Elements.query.filter_by(query_selector=query_selector).first()

		if element:

			element.text = query_selectors[query_selector]

			element.query_selector = query_selector

		else:

			element_type = query_selector.split()[1].split('-')[0]

			element = Elements(element_type=element_type, text=query_selectors[query_selector], query_selector=query_selector, page_id=7)
		
		db.session.add(element)

	db.session.commit()

	return jsonify({'result':'done'})



@app.route('/admin/edit_profile', methods=['GET', 'POST'])
@login_required
def admin_profile():

	form = EditProfileForm()

	user = User.query.filter_by(username=current_user.username).first()

	if form.validate_on_submit():

		user.username = form.username.data

		user.name = form.name.data

		user.phone = form.contact.data 

		user.email = form.email.data

		db.session.add(user)

		db.session.commit()

		flash('Details Edited Successfully', 'message')


	return render_template('admin_profile.html', form=form, user=user, title="Edit Profile")

@app.route('/admin/change_password', methods=['POST', 'GET'])
@login_required
def admin_change_password():

	form = ChangePasswordForm()

	user = User.query.filter_by(username=current_user.username).first()

	if form.validate_on_submit():

		if user.check_password(form.old_password.data):

			if form.new_password.data == form.confirm_new_password.data:

				user.set_password(form.new_password.data)

				db.session.add(user)

				db.session.commit()

				flash('Your password has been updated', 'message')


			else:

				flash('new passwords does not match', 'error')

		else:

			flash('Enter correct password', 'error')

		return redirect(url_for('admin_change_password'))



	return render_template('admin_change_password.html', form=form, title="Change Password")



@app.route('/admin/pages/edit-request', methods=['GET', 'POST'])
@login_required
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
					'url_slug':page.slug,
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

		formData = {'page_name':page.page_name,'url_slug':page.slug}

	return jsonify(formData)




@app.route('/admin/metaContent/edit', methods=['GET', 'POST'])
@login_required
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

		page.slug = data['url_slug']

		if data['image_bin']:

			image = data['image_bin']

			image_name = save_picture(image)

			if meta_obj.og_image:

				image_path = os.path.join(app.root_path, 'static/crop_images', meta_obj.og_image)

				os.remove(image_path)

			meta_obj.og_image = image_name

		db.session.add(meta_obj)

		db.session.commit()

		


	else:


		meta_obj = Meta_Content(title=data['meta_title'], description=data['meta_description'], keywords=data['meta_keywords'], robots=data['meta_robots'], canonical=data['canonical'], og_type=data['og_type'], og_title=data['og_title'], og_description=data['og_description'], page=page)

		db.session.add(meta_obj)

		db.session.commit()

	flash('Your changes have been saved', 'message')


	return redirect(url_for('pages'))



@app.context_processor
def inject_pages():

	base_page_names = Pages.query.all()

	return dict(base_page_names=base_page_names)


@login.user_loader
def load_user(id):

	return User.query.get(int(id))







