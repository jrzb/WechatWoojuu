# -*- coding: utf-8 -*-
#---------------------------
# File : app.py
# Author : liki
# Description : Flask App
# Created : 5/17/13
#---------------------------
from os import path
from base64 import urlsafe_b64encode, b64decode
from flask import Flask, render_template, url_for, request
from mailgun import Mailgun
from const import *
from mylogging import mylog


## Add timestamp to static css/js files loaded by url_for to prevent from caching
def static(filename):
	file_path = path.join(path.abspath('ui'), 'app', filename)
	last_modification = '%d' % path.getmtime(file_path)
	return url_for('.static', filename=filename) + '?' + last_modification


def create_app():
	root_path = path.dirname(path.dirname(path.abspath(__file__)))
	template_path = path.join(root_path, 'ui', 'app', 'templates')
	app = Flask(__name__, static_path='/ui/app', static_url_path='/static', template_folder=template_path)
	app.config.from_pyfile('config.py')

	# overriding default jinja2 template tags, to avoid conflicts with angularjs
	app.jinja_env.variable_start_string = '{['
	app.jinja_env.variable_end_string = ']}'

	@app.context_processor
	def inject_static():
		return dict(static=static)
	return app

# Init app
app = create_app()
mailgun = Mailgun(app)


@app.route('/')
@app.route('/applied')
def home():
	"""single page"""
	return render_template('index.html')


@app.route('/confirm_email/<email_hash>')
def confirm_email(email_hash):
	try:
		mylog.info(b64decode(email_hash))
	except TypeError:
		pass
	return render_template('index.html')


@app.route('/register', methods=['POST'])
def register():
	if request.method == 'POST':
		email = request.json["email"]
		name = email.split('@')[0]
		hashurl = urlsafe_b64encode(email)
		mailgun.send_email(
			to=email,
			subject=MAIL_SUBJECT,
			text=MAIL_TEXT % (name, hashurl)
		)
		return email
	return "sending email failed."


## bypass cross domain security
@app.after_request
def after_request(response):
	response.headers.add('Access-Control-Allow-Origin', '*')  # TODO: to be more secured
	response.headers.add('Access-Control-Allow-Methods', 'POST')
	# response.headers.add('Access-Control-Allow-Headers', 'X-Requested-With')
	return response

def run():
	app.run()

if __name__ == '__main__':
	# app.run(host='0.0.0.0', debug=True)
	app.run()
