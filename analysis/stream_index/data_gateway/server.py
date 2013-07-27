# -*- coding: utf-8 -*-
#!/usr/bin/python
##-------------------------------------------------------------------
## @copyright 2013
## File : server.py
## Author : filebat <markfilebat@126.com>
## Description :
## --
## Created : <2013-05-27 00:00:00>
## Updated: Time-stamp: <2013-06-11 14:35:31>
##-------------------------------------------------------------------
from flask import Flask
from flask import render_template
from flask import make_response
from flask import request

import hashlib
import json

import config
import util

app = Flask(__name__)

################# public backend api ###########################
@app.route("/api", methods=['POST'])
def insert_data():
	if _verification(request):
		data = request.data
		content = "OK: message is stored correctly."
		# TODO: check return code; reuse mq connection
		util.insert_message(config.QUEUE_NAME, data)
		resp = make_response(content, 200)
		resp.headers['Content-type'] = 'application/text; charset=utf-8'
	else:
		content = "Error: access denied"
		resp = make_response(content, 403)
		resp.headers['Content-type'] = 'application/text; charset=utf-8'
	return resp

@app.route("/get_index_userprofile", methods=['GET'])
def get_index_userprofile():
	# TODO defensive code
	username = request.args.get('username')
	service_name = request.args.get('service_name')
	index_key_list = request.args.get('index_key_list', '')
	if index_key_list != '':
		index_key_list = index_key_list.split(";")

		sql_format = "select index_key, index_value from userprofile " + \
					 "where username='%s' and service_name='%s' and index_key in (%s)"
		sql = sql_format % (username, service_name, ",".join(["'%s'" % (k) for k in index_key_list]))
		print sql
		out = util.query_sql(sql)
		out = util.fill_missing_data(out, index_key_list, '0')
	else:
		sql_format = "select index_key, index_value from userprofile " + \
					 "where username='%s' and service_name='%s'"
		sql = sql_format % (username, service_name)
		print sql
		out = util.query_sql(sql)
	print out

	content = render_template('get_userprofile.json', objs=out)
	content = util.smarty_remove_extra_comma(content)
	resp = make_response(content, 200)
	resp.headers['Content-type'] = 'application/json; charset=utf-8'
	return resp

@app.route("/get_index_serviceprofile", methods=['GET'])
def get_index_serviceprofile():
	service_name = request.args.get('service_name')
	index_key_list = request.args.get('index_key_list')
	index_key_list = index_key_list.split(";")

	sql_format = "select index_key, index_value from serviceprofile " + \
				 "where service_name='%s' and index_key in (%s)"
	sql = sql_format % (service_name, ",".join(["'%s'" % (k) for k in index_key_list]))
	print sql
	out = util.query_sql(sql)
	out = util.fill_missing_data(out, index_key_list, '0')
	print out

	content = render_template('get_serviceprofile.json', objs=out)
	content = util.smarty_remove_extra_comma(content)
	resp = make_response(content, 200)
	resp.headers['Content-type'] = 'application/json; charset=utf-8'
	return resp

@app.route("/get_usertext", methods=['GET'])
def get_usertext():
	# TODO defensive code
	username = request.args.get('username')
	service_name = request.args.get('service_name')
	limit = 50 # TODO: remove hard code here
	sql_format = "select createtime, content from usertext " + \
				 "where from_username in ('%s', '%s')  and to_username in ('%s', '%s') order by id desc limit %d;"
	sql = sql_format % (username, service_name, username, service_name, limit)
	print sql
	out = util.query_sql(sql)

	content = render_template('get_usertext.json', objs=out)
	content = util.smarty_remove_extra_comma(content)
	resp = make_response(content, 200)
	resp.headers['Content-type'] = 'application/json; charset=utf-8'
	return resp

@app.route("/get_user_latest_inputtext", methods=['GET'])
def get_user_latest_inputtext():
	# TODO defensive code
	service_name = request.args.get('service_name')
	limit = 35 # TODO: remove hard code here
	# "where from_username not in ('obF30jr0VD4HUjUq1kYusd5gSCBo', 'obF30jvBV656EFFzbzFoqMGxPivM') and " + \
	sql_format = "select createtime, from_username, content from usertext " + \
				 "where msgid!='' and to_username='%s' order by createtime desc limit %d;"
	sql = sql_format % (service_name, limit)
	print sql
	out = util.query_sql(sql)

	content = render_template('get_user_latest_inputtext.json', objs=out)
	content = util.smarty_remove_extra_comma(content)
	resp = make_response(content, 200)
	resp.headers['Content-type'] = 'application/json; charset=utf-8'
	return resp

## bypass cross domain security
@app.after_request
def after_request(response):
	response.headers.add('Access-Control-Allow-Origin', '*') # TODO: to be more secured
	response.headers.add('Access-Control-Allow-Methods', 'GET')
	response.headers.add('Access-Control-Allow-Headers', 'X-Requested-With')
	return response

################################################################

################# private functions ############################

def _verification(request):
	"""
	http://docs.python.org/2/library/hashlib.html
	"""
	# TODO more universe
	return True

def replace_str(content):
	content = content.replace("\n", " ")
	return content

################################################################
app.jinja_env.globals.update(replace_str=replace_str)

if __name__ == "__main__":
	app.debug = True
	app.run(host="0.0.0.0", port = int(config.FLASK_SERVER_PORT))
## File : server.py
