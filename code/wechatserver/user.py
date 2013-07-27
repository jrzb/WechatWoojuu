# -*- coding: utf-8 -*-
#!/usr/bin/python
##-------------------------------------------------------------------
## @copyright 2013
## File : user.py
## Author : filebat <markfilebat@126.com>
## Description :
## --
## Created : <2013-01-25 00:00:00>
## Updated: Time-stamp: <2013-06-15 23:24:38>
##-------------------------------------------------------------------
import MySQLdb
import config

class WechatUser:
	def __init__(self, userid, service_id):
		self.userid = ""
		self.service_id = ""
		self.user_dict = { }

	def set_attr(self, index_key, index_value):
		self.user_dict[index_key] = index_value

	def get_attr(self, index_key):
		ret = None
		if self.user_dict.has_key(index_key):
			ret = self.user_dict[index_key]
		return ret

	def dump(self):
		print self.user_dict

############################### HELPER FUNCTIONS #############################
# TODO: will be re-org
def get_user_by_id(userid, service_id = ""):
	if service_id == "":
		service_id = config.WECHAT_SERVICE_ID 
	user = WechatUser(userid, service_id)
	sql_format = "select nickname, gender from userprofile" + \
				 " where username='%s' and service_name ='%s';"
	sql = sql_format % (userid, service_id)

	conn = MySQLdb.connect(config.DB_HOST, config.DB_USERNAME, config.DB_PWD, \
						   config.DB_NAME, charset='utf8mb4', port=config.DB_PORT)
	cursor = conn.cursor()
	cursor.execute(sql)
	out = cursor.fetchall()
	cursor.close()

	if len(out) == 1:
		# TODO: better way
		if out[0][0] is not None:
			user.set_attr('nickname', out[0][0])

		if out[0][1] is not None:
			user.set_attr('gender', out[0][1])

	return user
##############################################################################
## File : expense.py