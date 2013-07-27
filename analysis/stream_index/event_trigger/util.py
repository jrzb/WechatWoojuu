# -*- coding: utf-8 -*-
#!/usr/bin/python
##-------------------------------------------------------------------
## @copyright 2013
## File : util.py
## Author : filebat <markfilebat@126.com>
## Description :
## --
## Created : <2013-05-25 00:00:00>
## Updated: Time-stamp: <2013-06-21 13:42:25>
##-------------------------------------------------------------------
import xml.etree.ElementTree as ET
from datetime import datetime
import time

import MySQLdb
import config

################################################################
def parse_msg(raw_msg):
	"""
	http://docs.python.org/2/library/xml.etree.elementtree.html#xml.etree.ElementTree.XML
	"""
	raw_msg = raw_msg.replace('&', '&amp;')
	root = ET.fromstring(raw_msg)
	msg = {}
	for child in root:
		if child.tag == 'CreateTime':
			value = long(child.text)
		else:
			value = child.text
		msg[child.tag] = value
	return msg

def _to_tag(k):
	return ''.join([w.capitalize() for w in k.split('_')])


def _cdata(data):
	"""
	http://stackoverflow.com/questions/174890/how-to-output-cdata-using-elementtree
	"""
	if type(data) is str:
		return '<![CDATA[%s]]>' % data.replace(']]>', ']]]]><![CDATA[>')
	return data


def _to_xml(**kwargs):
	xml = '<xml>'

	def cmp(x, y):
		""" WeiXin need ordered elements?"""
		ordered = ['to_user_name', 'from_user_name', 'create_time', 'msg_type', 'content', 'func_flag']
		try:
			ix = ordered.index(x)
		except ValueError:
			return 1
		try:
			iy = ordered.index(y)
		except ValueError:
			return -1
		return ix - iy

	for k in sorted(kwargs.iterkeys(), cmp):
		v = kwargs[k]
		tag = _to_tag(k)
		xml += '<%s>%s</%s>' % (tag, _cdata(v), tag)
	xml += '</xml>'
	return xml

################################################################
def current_date():
	date = datetime.now()
	return date.strftime('%Y%m%d')

def seconds_to_date(seconds):
	date = datetime.fromtimestamp(int(seconds))
	return date.strftime('%Y%m%d')

def between_days(seconds):
	date = datetime.fromtimestamp(int(seconds))
	date_str = date.strftime('%Y-%m-%d')
	date_str = date_str + " 00:00:00"
	begin_seconds= int(time.mktime(time.strptime(date_str,"%Y-%m-%d %H:%M:%S")))
	end_seconds= begin_seconds + 24*60*60
	return (begin_seconds, end_seconds)

def query_sql(conn, sql):
	cursor = conn.cursor()
	cursor.execute(sql)
	out = cursor.fetchall()
	cursor.close()
	return out

def insert_mysql_usertext(msg_dict):
	if msg_dict.has_key('Memo') is False:
		msg_dict['Memo'] = ""
	conn = MySQLdb.connect(config.DB_HOST, config.DB_USERNAME, \
		config.DB_PWD, config.DB_NAME, charset = 'utf8mb4', port = config.DB_PORT)

	# try:
	if msg_dict.has_key('MsgId'):
		msgid = msg_dict['MsgId']
	else:
		msgid = ""
	sql_format = "insert into usertext(from_username, to_username, createtime, content, msgid, memo) " + \
				 "values (\"%s\", \"%s\", %d, \"%s\", \"%s\", \"%s\");"
	sql = sql_format % (msg_dict['FromUserName'], msg_dict['ToUserName'], \
		   msg_dict['CreateTime'], msg_dict['Content'], msgid, msg_dict['Memo'])
	print sql
	c = conn.cursor()
	c.execute(sql)
	conn.commit()
	# except:
	# 	print "ERROR insert mysql fail"
	# 	conn.rollback()
	##conn.disconnect()
	return True

def insert_mysql_userevent(msg_dict):
	conn = MySQLdb.connect(config.DB_HOST, config.DB_USERNAME, \
		config.DB_PWD, config.DB_NAME, charset = 'utf8mb4', port = config.DB_PORT)

	sql_format = "insert into userevent(from_username, to_username, createtime, event, eventkey, memo) " + \
				 "values (\"%s\", \"%s\", %d, \"%s\", \"%s\", \"%s\");"
	sql = sql_format % (msg_dict['FromUserName'], msg_dict['ToUserName'], \
		   msg_dict['CreateTime'], msg_dict['Event'], msg_dict['EventKey'],"")
	print sql
	c = conn.cursor()
	c.execute(sql)
	conn.commit()
	# except:
	# 	print "ERROR insert mysql fail"
	# 	conn.rollback()
	##conn.disconnect()
	return True

def update_userprofile(username, service_name, index_key, index_value):
	conn = MySQLdb.connect(config.DB_HOST, config.DB_USERNAME, \
		config.DB_PWD, config.DB_NAME, charset = 'utf8mb4', port = config.DB_PORT)

	sql_format = "replace into userprofile(username, service_name, index_key, index_value) " + \
				 "values (\"%s\", \"%s\", \"%s\", \"%s\");"
	sql = sql_format % (username, service_name, index_key, index_value)
	print sql
	c = conn.cursor()
	c.execute(sql)
	conn.commit()
	# except:
	# 	print "ERROR insert mysql fail"
	# 	conn.rollback()
	##conn.disconnect()
	return True

def update_serviceprofile(service_name, index_key, index_value):
	conn = MySQLdb.connect(config.DB_HOST, config.DB_USERNAME, \
		config.DB_PWD, config.DB_NAME, charset = 'utf8mb4', port = config.DB_PORT)

	sql_format = "replace into serviceprofile(service_name, index_key, index_value) " + \
				 "values (\"%s\", \"%s\", \"%s\");"
	sql = sql_format % (service_name, index_key, index_value)
	print sql
	c = conn.cursor()
	c.execute(sql)
	conn.commit()
	# except:
	# 	print "ERROR insert mysql fail"
	# 	conn.rollback()
	##conn.disconnect()
	return True

def get_userprofile(username, service_name, index_key, default_value):
	conn = MySQLdb.connect(config.DB_HOST, config.DB_USERNAME, \
		config.DB_PWD, config.DB_NAME, charset = 'utf8mb4', port = config.DB_PORT)

	sql_format = "select index_value from userprofile where username=\"%s\" " + \
				 " and service_name=\"%s\" and index_key = \"%s\";"

	sql = sql_format % (username, service_name, index_key)
	print sql
	out = query_sql(conn, sql)
	# TODO error handling
	if len(out) == 0:
		value = default_value			
	else:
		value = out[0][0]
	return value

def get_serviceprofile(service_name, index_key, default_value):
	conn = MySQLdb.connect(config.DB_HOST, config.DB_USERNAME, \
		config.DB_PWD, config.DB_NAME, charset = 'utf8mb4', port = config.DB_PORT)

	sql_format = "select index_value from serviceprofile where " + \
				 "service_name=\"%s\" and index_key = \"%s\";"

	sql = sql_format % (service_name, index_key)
	print sql
	out = query_sql(conn, sql)
	# TODO error handling
	if len(out) == 0:
		value = default_value			
	else:
		value = out[0][0]
	return value
################################################################
## File : util.py