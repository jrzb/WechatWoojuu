# -*- coding: utf-8 -*-
#!/usr/bin/python
##-------------------------------------------------------------------
## @copyright 2013
## File : server.py
## Author : filebat <markfilebat@126.com>
## Description :
## --
## Created : <2013-05-27 00:00:00>
## Updated: Time-stamp: <2013-06-12 13:25:45>
##-------------------------------------------------------------------
from flask import Flask
from flask import render_template
from flask import make_response
from flask import request
from flask import send_from_directory
import datetime

import config
import util
################### configuration ##############################

################################################################

app = Flask(__name__)

################# public backend api ###########################
@app.route("/get_index_daily_user_line", methods=['GET'])
def get_index_daily_user_line():
	username = request.args.get('username')
	service_name = request.args.get('service_name')
	index_key_list = request.args.get('index_key_list', '')
	if index_key_list == "":
		index_name = request.args.get('index_name')
		days = util.latest_days(7)
		l = map(lambda x: "%s_%s" % (x, index_name) , days)
		index_key_list = ";".join(l)

	url = "http://%s:%d/get_index_userprofile?username=%s&service_name=%s&index_key_list=%s" % \
		  (config.GATEWAY_HOST, config.GATEWAY_PORT, username, service_name, index_key_list)
	print "%s\n" % url

	data = util.request_http_json(url)
	(name, key_list, value_list) = util.parse_daily_index(data)
	key_list = map(lambda x: "'%s-%s'" % (x[4:6], x[6:8]), key_list)

	lineName = name
	title=u"某个用户每日指标统计 -- %s" % (lineName)
	facename= util.username_to_facename(username, service_name)
	if facename != config.EMPTY_FACENAME:
		subtitle = "facename:%s" % (facename)
	else:
		subtitle = "username:%s" % (username)
	xTitle = u"日期/MMDD"
	yTitle = u"数量/个"

	content = render_template('get_index_line.html', \
						title = title, subtitle = subtitle,\
						xTitle = xTitle, yTitle = yTitle, \
						lineName = lineName, \
						key_list = ",".join(key_list), \
						value_list = ",".join(value_list), \
						objs=None)
	resp = make_response(content, 200)
	resp.headers['Content-type'] = 'text/html; charset=utf-8'
	return resp

@app.route("/get_index_daily_users_lines", methods=['GET'])
def get_index_daily_users_lines():
	username_list = request.args.get('username_list').split(";")
	service_name = request.args.get('service_name')
	index_key_list = request.args.get('index_key_list', '')
	if index_key_list == "":
		index_name = request.args.get('index_name')
		days = util.latest_days(10)
		l = map(lambda x: "%s_%s" % (x, index_name) , days)
		index_key_list = ";".join(l)

	lineName_list = []
	value_lists = []
	for username in username_list:
		url = "http://%s:%d/get_index_userprofile?username=%s&service_name=%s&index_key_list=%s" % \
			  (config.GATEWAY_HOST, config.GATEWAY_PORT, username, service_name, index_key_list)
		print "%s\n" % url

		data = util.request_http_json(url)
		(name, key_list, value_list) = util.parse_daily_index(data)
		key_list = map(lambda x: "'%s-%s'" % (x[4:6], x[6:8]), key_list)
		value_lists.append(",".join(value_list))

		facename= util.username_to_facename(username, service_name)
		if facename != config.EMPTY_FACENAME:
			lineName_list.append(facename)
		else:
			lineName_list.append(username)

		title=u"若干用户每日指标统计 -- %s" % (name)

	# facename= util.username_to_facename(username, service_name)
	# if facename != config.EMPTY_FACENAME:
	#	subtitle = "facename:%s" % (facename)
	# else:
	#	subtitle = "username:%s" % (username)

	subtitle = ""
	xTitle = u"日期/MMDD"
	yTitle = u"数量/个"

	content = render_template('get_index_lines.html', \
				title = title, subtitle = subtitle,\
				xTitle = xTitle, yTitle = yTitle, \
				lineName_list = lineName_list, \
				key_list = ",".join(key_list), \
				line_count = len(lineName_list),\
				value_lists = value_lists, \
				objs=None)
	resp = make_response(content, 200)
	resp.headers['Content-type'] = 'text/html; charset=utf-8'
	return resp

@app.route("/get_index_daily_service_line", methods=['GET'])
def get_index_daily_service_line():
	service_name = request.args.get('service_name')
	index_key_list = request.args.get('index_key_list', '')
	if index_key_list == "":
		index_name = request.args.get('index_name')
		days = util.latest_days(10)
		l = map(lambda x: "%s_%s" % (x, index_name) , days)
		index_key_list = ";".join(l)

	url = "http://%s:%d/get_index_serviceprofile?service_name=%s&index_key_list=%s" % \
		  (config.GATEWAY_HOST, config.GATEWAY_PORT, service_name, index_key_list)
	print "%s\n" % url

	data = util.request_http_json(url)
	(name, key_list, value_list) = util.parse_daily_index(data)
	key_list = map(lambda x: "'%s-%s'" % (x[4:6], x[6:8]), key_list)

	lineName = name
	title=u"服务每日指标统计 -- %s" % (lineName)
	subtitle = u"service:%s" % (service_name)
	xTitle = u"日期/MMDD"
	yTitle = u"数量/个"

	content = render_template('get_index_line.html', \
				title = title, subtitle = subtitle,\
				xTitle = xTitle, yTitle = yTitle, \
				lineName = lineName, \
				key_list = ",".join(key_list), \
				value_list = ",".join(value_list), \
				objs=None)
	resp = make_response(content, 200)
	resp.headers['Content-type'] = 'text/html; charset=utf-8'
	return resp

@app.route("/get_index_daily_service_lines", methods=['GET'])
def get_index_daily_service_lines():
	service_name = request.args.get('service_name')
	index_name_list = request.args.get('index_name_list').split(";")

	lineName_list = []
	value_lists = []

	for index_name in index_name_list:
		days = util.latest_days(10)
		l = map(lambda x: "%s_%s" % (x, index_name) , days)
		index_key_list = ";".join(l)
		# print "\n=====================\n"
		# print index_key_list
		url = "http://%s:%d/get_index_serviceprofile?service_name=%s&index_key_list=%s" % \
			  (config.GATEWAY_HOST, config.GATEWAY_PORT, service_name, index_key_list)
		print "%s\n" % url

		data = util.request_http_json(url)
		(name, key_list, value_list) = util.parse_daily_index(data)
		key_list = map(lambda x: "'%s-%s'" % (x[4:6], x[6:8]), key_list)
		value_lists.append(",".join(value_list))

		lineName_list.append(index_name)

		title=u"服务每日指标统计"

	subtitle = u"service:%s" % (service_name)
	xTitle = u"日期/MMDD"
	yTitle = u"数量/个"

	content = render_template('get_index_lines.html', \
				title = title, subtitle = subtitle,\
				xTitle = xTitle, yTitle = yTitle, \
				lineName_list = lineName_list, \
				key_list = ",".join(key_list), \
				line_count = len(lineName_list),\
				value_lists = value_lists, \
				objs=None)
	resp = make_response(content, 200)
	resp.headers['Content-type'] = 'text/html; charset=utf-8'
	return resp

@app.route("/get_user_latest_inputtext", methods=['GET'])
def get_user_latest_inputtext():
	service_name = request.args.get('service_name')

	url = "http://%s:%d/get_user_latest_inputtext?service_name=%s" % \
		  (config.GATEWAY_HOST, config.GATEWAY_PORT, service_name)
	print "%s\n" % url

	data = util.request_http_json(url)
	content = ""
	for entry in data:
		username = entry["username"]
		facename = util.username_to_facename(username, service_name)
		if facename == config.EMPTY_FACENAME:
			facename = "[%s]" % username
		else:
			facename = "[%s] [%s]" % (facename, username)
		content ="%s[%s] %s %s<br/>" \
				% (content, \
				   datetime.datetime.fromtimestamp(int(entry["createtime"])).strftime('%H:%M:%S'), \
				   facename, entry["content"])

	content = "<font size=4>%s</font>" % (content)
	resp = make_response(content, 200)
	resp.headers['Content-type'] = 'text/html; charset=utf-8'
	return resp

@app.route("/lib/<path:filename>", methods=['GET'])
def static(filename):
	return send_from_directory("./lib", filename)

## bypass cross domain security
@app.after_request
def after_request(response):
	response.headers.add('Access-Control-Allow-Origin', '*') # TODO: to be more secured
	response.headers.add('Access-Control-Allow-Methods', 'GET')
	response.headers.add('Access-Control-Allow-Headers', 'X-Requested-With')
	return response

################################################################

if __name__ == "__main__":
	app.debug = True
	app.run(host="0.0.0.0", port = int(config.FLASK_SERVER_PORT))
## File : server.py
