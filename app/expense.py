# -*- coding: utf-8 -*-
#!/usr/bin/python
##-------------------------------------------------------------------
## @copyright 2013
## File : expense.py
## Author : filebat <markfilebat@126.com>
## Description :
## --
## Created : <2013-01-25 00:00:00>
## Updated: Time-stamp: <2013-06-15 02:14:29>
##-------------------------------------------------------------------
import MySQLdb
from mylogging import log

import config
from datetime import datetime

from const_emoji import get_emoji

class Expense:
	def __init__(self):
		self.userid = ""
		self.source_expenseid = ""
		self.amount = -1
		self.branding = ""
		self.category = ""
		self.date = ""
		self.createtime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
		self.latitude = 0.0
		self.longitude = 0.0
		self.notes = ""
		self.memo =""

	def init_with_sqlite(self, userid, expenseid, amount, categoryid, \
						 date, notes, latitude, longitude, branding=""):
		self.userid = userid
		self.source_expenseid = expenseid.strip()
		self.amount = amount
		self.category = categoryid  # TODO make conversion
		self.date = date.strip()  # TODO defensive code
		self.latitude = latitude
		self.longitude = longitude
		self.branding = branding
		self.notes = my_strip(notes)

	def init_with_ledger(self, userid, amount, category, date, notes):
		self.userid = userid
		self.amount = amount
		self.category = category  # TODO make conversion
		self.date = date.strip()  # TODO defensive code
		self.notes = my_strip(notes)

	def init_with_mysql(self, userid, amount, category, branding, date, notes, memo):
		self.userid = userid
		self.amount = amount
		self.category = category  # TODO make conversion
		self.branding = branding
		self.date = date.strip()  # TODO defensive code
		self.notes = my_strip(notes)
		self.memo = memo

	@staticmethod
	def print_obj(obj):
		print "userid:%s, amount:%f, category:%s, branding:%s, date:%s, latitude:%f, longitude:%f, notes:%s\n" % \
			(obj.userid, obj.amount, obj.category, obj.branding,\
			 obj.date, obj.latitude, obj.longitude, obj.notes)

	@staticmethod
	def generate_insert_sql(obj):
		sql_format = "insert into expenses(userid, source_expenseid, amount, category, date, " + \
					 "latitude, longitude, notes, branding, createtime, memo) " + \
					 "values (\"%s\", \"%s\", %f, \"%s\", \"%s\", %f, %f, \"%s\", \"%s\", \"%s\", \"%s\");"
		sql = sql_format % (obj.userid, obj.source_expenseid, obj.amount, \
							obj.category, obj.date, obj.latitude, \
							obj.longitude, obj.notes, obj.branding, obj.createtime, obj.memo)
		return sql

	@staticmethod
	def query_obj_by_category(userid, category, limit):
		sql = "select date, category, branding, notes, amount, memo from expenses" + \
			  " where userid='" + userid +"' and category = '" +\
			  category + "' order by date desc limit " + str(limit)
		conn = MySQLdb.connect(config.DB_HOST, config.DB_USERNAME, config.DB_PWD, \
							   config.DB_NAME, charset='utf8mb4', port=config.DB_PORT)
		cursor = conn.cursor()
		cursor.execute(sql)
		out = cursor.fetchall()
		cursor.close()
		objs = []
		for o in out:
			expense = Expense()
			expense.init_with_mysql(userid, amount=o[4], category=o[1], \
				branding = o[2], date=o[0], notes=o[3], memo=o[5])
			objs.append(expense)
		return objs

	@staticmethod
	def query_obj_by_notes(userid, notes, limit):
		sql = "select date, category, branding, notes, amount, memo from expenses" + \
			  " where userid='" + userid +"' and notes like '%" +\
			  notes + "%' order by date desc limit " + str(limit)
		conn = MySQLdb.connect(config.DB_HOST, config.DB_USERNAME, config.DB_PWD, \
							   config.DB_NAME, charset='utf8mb4', port=config.DB_PORT)
		cursor = conn.cursor()
		cursor.execute(sql)
		out = cursor.fetchall()
		cursor.close()
		objs = []
		for o in out:
			expense = Expense()
			expense.init_with_mysql(userid, amount=o[4], category=o[1], \
				branding = o[2], date=o[0], notes=o[3], memo=o[5])
			objs.append(expense)
		return objs

	@staticmethod
	def query_obj_by_date(userid, fromdate, enddate):
		sql = "select expenseid, category, date, amount, notes, memo from expenses" + \
			  " where userid='" + userid +"' and date >='" +\
			  fromdate + "' and date<='" + enddate + "' order by date desc"
		conn = MySQLdb.connect(config.DB_HOST, config.DB_USERNAME, config.DB_PWD, \
							   config.DB_NAME, charset='utf8mb4', port=config.DB_PORT)
		cursor = conn.cursor()
		log.info(sql)
		cursor.execute(sql)
		out = cursor.fetchall()
		cursor.close()
		return out

	@staticmethod
	def query_obj_by_date2(userid, searchdate, limit):
		sql = "select date, category, branding, notes, amount, memo from expenses" + \
			  " where userid='" + userid +"' and left(date, 10) like'%" +\
			  searchdate + "%' order by date desc limit " + str(limit)
		#print sql
		conn = MySQLdb.connect(config.DB_HOST, config.DB_USERNAME, config.DB_PWD, \
							   config.DB_NAME, charset='utf8mb4', port=config.DB_PORT)
		cursor = conn.cursor()
		log.info(sql)
		cursor.execute(sql)
		out = cursor.fetchall()
		cursor.close()
		objs = []
		for o in out:
			expense = Expense()
			expense.init_with_mysql(userid, amount=o[4], category=o[1], \
				branding = o[2], date=o[0], notes=o[3], memo=o[5])
			objs.append(expense)
		return objs

	@staticmethod
	def delete_obj_by_id(userid, expenseid):
		if expenseid != "":
			sql = "delete from expenses where userid='" + userid +"' and expenseid=" + expenseid
		else:
			sql = "delete from expenses where userid='" + userid + "'"
		conn = MySQLdb.connect(config.DB_HOST, config.DB_USERNAME, config.DB_PWD, \
							   config.DB_NAME, charset='utf8mb4', port=config.DB_PORT)

		log.info(sql)
		cursor = conn.cursor()
		# TODO: report error 
		try:
			cursor.execute(sql)
			conn.commit()
		except MySQLdb.Error:
			log.error("ERROR delete mysql fail")
			conn.rollback()

		cursor.close()
		return True

	@staticmethod
	def query_sql(sql):
		conn = MySQLdb.connect(config.DB_HOST, config.DB_USERNAME, config.DB_PWD, \
							   config.DB_NAME, charset='utf8mb4', port=config.DB_PORT)
		cursor = conn.cursor()
		print sql
		cursor.execute(sql)
		out = cursor.fetchall()
		cursor.close()
		return out

	@staticmethod
	def objs_to_str(objs):
		msg = ""
		for obj in objs:
			msg = "%s[%s %s] %s%s %s\n" % (msg, obj.date[0:10], obj.category, str(obj.amount), u"元", obj.notes)
		if msg == "":
			msg = u"没有符合条件的记录"
		msg = msg.rstrip("\n")
		return msg

	@staticmethod
	def get_expense_msg(userid, category):
		sql = "select count(1), avg(amount) from expenses " + \
			  "where date > DATE_ADD(CURDATE(), INTERVAL -30 DAY) " +\
			  "and userid='" + userid + "' and category='" + category + "'";

		conn = MySQLdb.connect(config.DB_HOST, config.DB_USERNAME, config.DB_PWD, \
							   config.DB_NAME, charset='utf8mb4', port=config.DB_PORT)
		cursor = conn.cursor()
		log.info(sql)
		cursor.execute(sql)
		out = cursor.fetchall()

		user_count = out[0][0]
		user_amount = out[0][1]

		sql = "select count(1)/count(distinct userid), avg(amount) from expenses " + \
			  "where userid not in ('obF30jhXJFKf9ak6_KlhF84WhmKc', 'obF30jlR2x9xmh6a5pMF-ZIYtzQY') and " + \
			  "date > DATE_ADD(CURDATE(), INTERVAL -30 DAY) and category='" + category + "'";

		conn = MySQLdb.connect(config.DB_HOST, config.DB_USERNAME, config.DB_PWD, \
							   config.DB_NAME, charset='utf8mb4', port=config.DB_PORT)
		cursor = conn.cursor()
		log.info(sql)
		cursor.execute(sql)
		out = cursor.fetchall()
		avg_count = out[0][0]
		avg_amount = out[0][1]

		cursor.close()
		return (user_count, user_amount, avg_count, avg_amount)

	@staticmethod
	def print_objs(objs):
		for obj in objs:
			obj.print_obj(obj)


############################### HELPER FUNCTIONS #############################
def my_strip(string):
	string = string.strip()
	string = string.replace("\n", "")
	return string

##############################################################################

## File : expense.py