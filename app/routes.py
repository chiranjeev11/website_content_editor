from app import app
from app.forms import LoginForm
from flask_login import current_user, login_required
from flask import render_template, redirect, url_for
from app.models import Meta_content, pages_url

@app.route('/login')
def login():

	form = LoginForm()

	page = Meta_content.query.filter_by(page_id = pages_url.query.filter_by(page_name='Login Page').first().id).first()

	if form.validate_on_submit():

		return redirect(url_for('index'))

	return render_template('login.html', form=form, page=page)

@login_required
@app.route('/')
def index():

	page = Meta_content.query.filter_by(page_id = pages_url.query.filter_by(page_name='Home Page').first().id).first()
		
	return render_template('index.html', page=page)




@app.route('/abc.htm')
def fees_page():

	page = Meta_content.query.filter_by(page_id = pages_url.query.filter_by(page_name='Fees & ISA').first().id).first()

	return render_template('fees.html', page=page)

@app.route('/privacy.htm')
def privacy_policy():

	page = Meta_content.query.filter_by(page_id = pages_url.query.filter_by(page_name='Privacy Policy').first().id).first()


	return render_template('privacy_policy.html', page=page)

