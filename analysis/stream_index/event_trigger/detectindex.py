# -*- coding: utf-8 -*-
#!/usr/bin/python
##-------------------------------------------------------------------
## @copyright 2013 ShopEx Network Technology Co,.Ltd
## File : detectindex.py
## Author : filebat <markfilebat@126.com>
## Description :
## --
## Created : <2013-05-25>
## Updated: Time-stamp: <2013-06-22 18:27:26>
##-------------------------------------------------------------------
import commands
import MySQLdb

import config
import util

def detect_user_last_visit_time(msg, msg_dict):
	if not (msg_dict['MsgType'] == 'text' and msg_dict.has_key('MsgId')):
		return True
	username = msg_dict['FromUserName']
	service_name = msg_dict['ToUserName']
	index_key = "user_visit_time"
	index_value = "%s" % msg_dict['CreateTime']
	util.update_userprofile(username, service_name, index_key, index_value)

def detect_user_daily_visit_count(msg, msg_dict):
	if not (msg_dict['MsgType'] == 'text' and msg_dict.has_key('MsgId')):
		return True

	username = msg_dict['FromUserName']
	service_name = msg_dict['ToUserName']
	index_key = "%s_visit_count" % (util.seconds_to_date(msg_dict['CreateTime']))
	index_value = util.get_userprofile(username, service_name, index_key, 0)

	index_value = int(index_value) + 1
	util.update_userprofile(username, service_name, index_key, index_value)

def detect_user_subscribe_time(msg, msg_dict):
	if not (msg_dict['MsgType'] == 'event' and msg_dict['Event'] == 'subscribe'):
		return True
	username = msg_dict['FromUserName']
	service_name = msg_dict['ToUserName']
	index_key = "user_subscribe_time"
	index_value = "%s" % msg_dict['CreateTime']
	util.update_userprofile(username, service_name, index_key, index_value)

def detect_daily_subscribe_count(msg, msg_dict):
	if not (msg_dict['MsgType'] == 'event' and msg_dict['Event'] == 'subscribe'):
		return True

	username = ""
	service_name = msg_dict['ToUserName']
	index_key = "%s_subscribe_count" % (util.seconds_to_date(msg_dict['CreateTime']))
	index_value = util.get_serviceprofile(service_name, index_key, 0)

	index_value = int(index_value) + 1
	util.update_serviceprofile(service_name, index_key, index_value)

def detect_daily_unsubscribe_count(msg, msg_dict):
	if not (msg_dict['MsgType'] == 'event' and msg_dict['Event'] == 'unsubscribe'):
		return True

	username = ""
	service_name = msg_dict['ToUserName']
	index_key = "%s_unsubscribe_count" % (util.seconds_to_date(msg_dict['CreateTime']))
	index_value = util.get_serviceprofile(service_name, index_key, 0)

	index_value = int(index_value) + 1
	util.update_serviceprofile(service_name, index_key, index_value)

def detect_daily_record_count(msg, msg_dict):
	if not (msg_dict['MsgType'] == 'text' and msg_dict.has_key('MsgId')):
		return True
	username = ""
	service_name = msg_dict['ToUserName']
	index_key = "%s_record_count" % (util.seconds_to_date(msg_dict['CreateTime']))
	index_value = util.get_serviceprofile(service_name, index_key, 0)

	index_value = int(index_value) + 1
	util.update_serviceprofile(service_name, index_key, index_value)

def detect_daily_valid_record_count(msg, msg_dict):
	if not (msg_dict['MsgType'] == 'text' and msg_dict.has_key('MsgId') is False):
		return True

	content = msg_dict['Content']
	if content.find("记好了") == -1:
		return True

	print "======= here ===="
	username = ""
	service_name = msg_dict['FromUserName']
	index_key = "%s_valid_record_count" % (util.seconds_to_date(msg_dict['CreateTime']))
	index_value = util.get_serviceprofile(service_name, index_key, 0)

	index_value = int(index_value) + 1
	util.update_serviceprofile(service_name, index_key, index_value)

def detect_daily_uniq_user_count(msg, msg_dict):
	if not (msg_dict['MsgType'] == 'text' and msg_dict.has_key('MsgId')):
		return True

	conn = MySQLdb.connect(config.DB_HOST, config.DB_USERNAME, \
		config.DB_PWD, config.DB_NAME, charset = 'utf8mb4', port = config.DB_PORT)

	date = util.seconds_to_date(msg_dict['CreateTime'])
	username = ''
	service_name = msg_dict['ToUserName']
	index_key = "%s_uniq_user_count" % (date)

	# TODO: need to improve performance, instead of query the whole dataset
	sql_format = "select count(1) from userprofile " + \
				 "where index_key = '%s_visit_count' and service_name = '%s';"
	sql = sql_format % (date, service_name)
	out = util.query_sql(conn, sql)

	if len(out) == 0:
		index_value = 0
	else:
		index_value = out[0][0] + 0

	util.update_serviceprofile(service_name, index_key, index_value)

def detect_user_count(msg, msg_dict):
	if not (msg_dict['MsgType'] == 'event'):
		return True

	username = ""
	service_name = msg_dict['ToUserName']
	index_key = "user_count"
	index_value = util.get_serviceprofile(service_name, index_key, 0)

	if (msg_dict['Event'] == "subscribe"):
		index_value = int(index_value) + 1
	if (msg_dict['Event'] == "unsubscribe"):
		index_value = int(index_value) - 1

	util.update_serviceprofile(service_name, index_key, index_value)

def detect_daily_record_pattern(msg, msg_dict):
	if not (msg_dict['MsgType'] == 'text' and msg_dict.has_key('MsgId')):
		return True

	record_pattern = get_record_pattern(msg_dict['Content'])
	username = ""
	service_name = msg_dict['ToUserName']
	index_key = "%s_record_pattern_%s" % (util.seconds_to_date(msg_dict['CreateTime']), record_pattern)
	index_value = util.get_serviceprofile(service_name, index_key, 0)

	index_value = int(index_value) + 1
	util.update_serviceprofile(service_name, index_key, index_value)

def alert_voice_input(msg, msg_dict):
	if not (msg_dict['MsgType'] == 'voice' and msg_dict.has_key('MsgId')):
		return True
	mail_list = "249950670@qq.com,pitaru@qq.com"
	cmd =  "echo \"%s\" | mail -s \"[Alert] Some voice input is given\" %s" % (str(msg), mail_list)
	status, output = commands.getstatusoutput(cmd)
	if(status == 0):
		print "Successfully run cmd:%s" % (cmd)
	else:
		# TODO: log error
		print "Fail to run cmd:%s. output:%s" % (cmd, output)

################################################################
def get_record_pattern(content):
	if content == "h":
		return "h"
	if content == "1":
		return "1"
	if content == "s" or content == u"搜索":
		return "s"
	if content == u"安静":
		return "quite"
	if content == u"删除":
		return "delete"

	return "other"
################################################################
## File : detectindex.py ends