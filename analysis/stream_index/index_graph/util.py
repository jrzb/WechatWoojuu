# -*- coding: utf-8 -*-
#!/usr/bin/python
##-------------------------------------------------------------------
## @copyright 2013
## File : util.py
## Author : filebat <markfilebat@126.com>
## Description :
## --
## Created : <2013-05-25 00:00:00>
## Updated: Time-stamp: <2013-06-12 13:27:37>
##-------------------------------------------------------------------
import MySQLdb
import config
# conn = MySQLdb.connect(config.DB_HOST, config.DB_USERNAME, \
# 					   config.DB_PWD, config.DB_NAME, charset = 'utf8mb4', port = config.DB_PORT)

import json
import urllib2
import datetime
from datetime import datetime
from datetime import timedelta

def request_http_json(url):
	data = json.load(urllib2.urlopen(url))
	#print data
	return data

def parse_daily_index(data):
	if len(data) == 0:
		return ("No data", [], [])

	data.sort(lambda x,y: int(x['key'][0:8]) - int(y['key'][0:8]))
	name = data[0]['key'][9:]

	#print data
	key_list = []
	value_list = []
	for item in data:
		key_list.append(item['key'][0:8])
		value_list.append(item['value'])
	return (name, key_list, value_list)

def latest_days(num=5):
	date = datetime.now()
	l = list(range(1, num + 1, 1))
	return map(lambda x: (date + timedelta(days=x-num)).strftime('%Y%m%d'), l)

def query_sql(sql, conn = None):
	if conn is None:
		conn = MySQLdb.connect(config.DB_HOST, config.DB_USERNAME, \
							   config.DB_PWD, config.DB_NAME, charset = 'utf8mb4', port = config.DB_PORT)
	cursor = conn.cursor()
	cursor.execute(sql)
	out = cursor.fetchall()
	cursor.close()
	return out

def get_userprofile(username, service_name, index_key, default_value):
	sql_format = "select index_value from userprofile where username=\"%s\" " + \
				 " and service_name=\"%s\" and index_key = \"%s\";"

	sql = sql_format % (username, service_name, index_key)
	print sql
	out = query_sql(sql)
	# TODO error handling
	if len(out) == 0:
		value = default_value			
	else:
		value = out[0][0]
	return value

def get_serviceprofile(service_name, index_key, default_value):
	sql_format = "select index_value from serviceprofile where " + \
				 "service_name=\"%s\" and index_key = \"%s\";"

	sql = sql_format % (service_name, index_key)
	print sql
	out = query_sql(sql)
	# TODO error handling
	if len(out) == 0:
		value = default_value			
	else:
		value = out[0][0]
	return value
################################################################
def username_to_facename(username, service_name):
	# TODO: cache the request
	facename = get_userprofile(username, service_name, "username", config.EMPTY_FACENAME)
	return facename
################################################################
## File : util.py