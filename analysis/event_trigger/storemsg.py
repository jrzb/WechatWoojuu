# -*- coding: utf-8 -*-
#!/usr/bin/python
##-------------------------------------------------------------------
## @copyright 2013
## File : storemsg.py
## Author : filebat <markfilebat@126.com>
## Description :
## --
## Created : <2013-05-25 00:00:00>
## Updated: Time-stamp: <2013-06-09 14:35:30>
##-------------------------------------------------------------------
import logging
from logging.handlers import RotatingFileHandler
import config

import util

accesslog = logging.getLogger('myapp_access')
access_rthandler = RotatingFileHandler('data/access_msg.log', maxBytes=5*1024*1024,backupCount=5, encoding="utf-8")
access_rthandler.setLevel(logging.INFO)
access_format = "%(message)s"
access_formatter = logging.Formatter(access_format)

access_rthandler.setFormatter(access_formatter)

accesslog.setLevel(logging.INFO)
accesslog.addHandler(access_rthandler)

################################################################
def store_raw(msg, msg_dict):
	accesslog.info("%s\n\n" % msg)

def store_mysql(msg, msg_dict):
	if msg_dict['MsgType'] == 'text':
		util.insert_mysql_usertext(msg_dict)
	if msg_dict['MsgType'] == 'voice':
		msg_dict['Content'] = config.VOICE_CONTENT
		msg_dict['Memo'] = "MediaId:%s;Format:%s;Recognition:%s" % \
						   (msg_dict['MediaId'], msg_dict['Format'], msg_dict['Recognition'])
		util.insert_mysql_usertext(msg_dict)
	if msg_dict['MsgType'] == 'event':
		util.insert_mysql_userevent(msg_dict)

################################################################
## File : mylogging.py
