# -*- coding: utf-8 -*-
#!/usr/bin/python
##-------------------------------------------------------------------
## @copyright 2013
## File : data.py
## Author : filebat <markfilebat@126.com>
## Description :
## --
## Created : <2013-01-25 00:00:00>
## Updated: Time-stamp: <2013-07-14 08:15:59>
##-------------------------------------------------------------------
import MySQLdb
from datetime import datetime
from datetime import timedelta

from const_brand import brand_category_dict
from mylogging import log, auditlog
import util
from util import format_float_str
import config
from expense import Expense
import const_message as MSG
from const_emoji import get_emoji
import chat
import user

def add_expense(userid, content):
	wechat_user = user.get_user_by_id(userid)

	content = content.encode('utf-8', 'ignore').strip()
	# bypass word split
	#content = util.wash_sentence(content)
	(code, date, category, amount, brand, comment, token_list) \
			= split_expense_word(" %s " % (content))
	expense = Expense()
	expense.init_with_mysql(userid, amount, category, \
							brand, date, content, config.DEFAULT_COMMENT)

	if code == config.RECORD_STATE_QUESTION:
		return chat.response_fail(expense, "?")

	if code == config.RECORD_STATE_MULTIPLE_RECORDS:
		return chat.response_fail(expense, "multiple_record")

	# print "====== Before (%s, %s, %d; %s) ====" % (category, brand, amount, expense.memo)
	# store tokens, if detection fail
	if category == "" or brand == "" or amount == -1:
		expense.memo = ""
		for text, start, end in token_list:
			expense.memo = "%s; %s" % (expense.memo, text)
	expense.memo = expense.memo.strip("; ")
	# print "====== After (%s, %s, %d; %s) ====" % (category, brand, amount, expense.memo)

	if chat.is_comment_meaningless(comment) is True:
		return chat.response_fail(expense, "empty_notes")

	if chat.is_comment_pure_alpha(comment) is True:
		return chat.response_fail(expense, "pure_alpha")

	if expense.amount == -1:
		return chat.reply_chat(expense, wechat_user)

	if expense.amount != -1:
		if insert_expense(expense) is False:
			rep_content = MSG.REPLY_EXPENSE_FAILED % comment
			log.error("user(%s) add_expense fail, content:%s" % (userid, content))

		if (expense.category != config.DEFAULT_CATEGORY) and (expense.branding != config.DEFAULT_BRANDING):
			tips = ""  # TODO to be implemented
			rep_content = MSG.REPLY_EXPENSE_ADDED % (
					category + get_emoji(category, "category"), str(amount))
			rep_content = chat.attach_detected_extra_msg(wechat_user, rep_content, expense)
		else:
			if expense.category != config.DEFAULT_CATEGORY:
				tips = ""  # TODO to be implemented
				rep_content = MSG.REPLY_EXPENSE_ADDED_WITH_CATEGORY % (\
						category + get_emoji(category, "category"), str(amount))
			else:
				if expense.branding != config.DEFAULT_BRANDING:
					tips = ""  # TODO to be implemented
					rep_content = MSG.REPLY_EXPENSE_ADDED_WITH_BRANDING % (\
							brand + get_emoji(brand, "brand"), str(amount))
				else:
					tips = ""  # TODO to be implemented
					rep_content = MSG.REPLY_EXPENSE_ADDED_SIMPLE % (\
							str(date[5:7]).lstrip("0"), str(date[8:10]).lstrip("0"), \
							str(amount), comment, tips)
			rep_content = chat.attach_undetected_extra_msg(wechat_user, expense, rep_content)

	if expense.category == config.CATEGORY_INCOMING:
		rep_content = rep_content.replace("消费", "赚了")

	return rep_content

def view_history(userid):
	(asset_amount, day_expense, week_expense, month_expense) = user_summary(userid)
	#print asset_amount, day_expense, week_expense, month_expense
	content = MSG.REPLAY_HISTORY % \
			  (format_float_str(str(day_expense)), \
			   format_float_str(str(week_expense)), \
			   format_float_str(str(month_expense)), \
			  format_float_str(str(asset_amount)), \
	   )
	return content.encode('utf-8', 'ignore')

def delete_last_record(userid):
	sql_format = "select expenseid, notes from expenses" + \
				 " where userid='%s' order by expenseid desc limit 1"
	sql = sql_format % (userid)

	out = Expense.query_sql(sql)

	if len(out) == 0:
		content = "坑爹呀，你都没数据，删除啥？"
	else:
		expenseid = out[0][0]
		notes = out[0][1]
		if Expense.delete_obj_by_id(userid, str(expenseid)) is True:
			content = "上一条记录删除好了: %s。/:sun\n查看最近记录，输入: 搜索" % (notes)
		else:
			content = "Oops, 删除失败了。"
	return content.encode('utf-8', 'ignore')

# python -c "import data; print data.search_record('denny', u'充值')"
def search_record(userid, notes):
	notes = notes.encode('utf-8', 'ignore').strip()

	search_keyword = notes.replace(MSG.CODE_SEARCH, "")
	search_keyword = search_keyword.replace(MSG.CODE_SEARCH2, "")
	search_keyword = search_keyword.replace(MSG.CODE_SEARCH3, "")
	search_keyword = util.wash_sentence(search_keyword)

	expense_list = Expense.query_obj_by_notes(userid, search_keyword, 15)

	(code, date, category, amount, branding, comment, token_list) \
			= split_expense_word(notes)
	if category != config.DEFAULT_CATEGORY:
		expense_list2 = Expense.query_obj_by_category(userid, category.encode("utf8"), 15)
		expense_list = expense_list + expense_list2

	if search_keyword.replace("-", "").isdigit():
		search_date = search_keyword
		if search_keyword.find("-") == -1:
			search_date = "-%s" % (search_keyword)
		expense_list2 = Expense.query_obj_by_date2(userid, search_date, 15)
		expense_list = expense_list + expense_list2

	message = ""
	for obj in expense_list:
		message = "%s %s%s %s\n" % (message, obj.date[5:10].replace('-', '/'), \
									# str(obj.amount).replace(".0", "")+"元", \
									get_emoji(obj.category.encode("utf8"), "category"), obj.notes)

	if message == "" and search_keyword == "":
		return u"系统里一条记录都没有啵。亲，多记账呀，多记账"

	if message == "":
		message = u"无符合条件的记录。试下只输入: 搜索"
	message = message.rstrip("\n")

	content = MSG.REPLAY_SEARCH % (search_keyword, message, userid)
	return content.encode('utf-8', 'ignore')

def reply_voice(msg):
	return chat.pic_random("voice_input")

def reply_image(msg):
	return chat.response_fail(None, "image_input")

def split_expense_word(sentence):
	if sentence.find("?") != -1 or sentence.find("？") != -1:
		return (config.RECORD_STATE_QUESTION, "", "", -1, "", "", [])

	# replace smiley
	sentence = sentence.replace("/:8-)", "")
	token_list = util.word_split(sentence, 1)
	(branding, category) = detect_branding_category(token_list)
	#print "branding:%s, category:%s" % (branding, category)
	date, amount = detect_date_amount(token_list)
	if date == config.RECORD_STATE_MULTIPLE_RECORDS:
		return (config.RECORD_STATE_MULTIPLE_RECORDS, "", "", -1, "", "", [])

	comment = util.remove_amount_from_comment(sentence, amount)

	return (config.RECORD_STATE_NORMAL, date, \
			category, amount, branding, comment, token_list)

def insert_expense(expense):
	conn = MySQLdb.connect(config.DB_HOST, config.DB_USERNAME, config.DB_PWD, \
						   config.DB_NAME, charset='utf8mb4', port=config.DB_PORT)
	cursor = conn.cursor()

	sql = Expense.generate_insert_sql(expense)
	log.info("SQL:" + sql)
	#print sql
	try:
		cursor.execute(sql)
		conn.commit()
	except MySQLdb.Error:
		log.error("SQL fail: %s" % sql)
		conn.rollback()

	cursor.close()
	# TODO: defensive check
	return True


def user_summary(userid):
	# TODO support date is given as parameter
	end_date = datetime.now()
	end_date_str = end_date.strftime('%Y-%m-%d') + " 23:59:59"
	# TODO: pre-calculate below data, if performance is slow
	conn = MySQLdb.connect(config.DB_HOST, config.DB_USERNAME, config.DB_PWD, \
						   config.DB_NAME, charset='utf8mb4', port=config.DB_PORT)
	cursor = conn.cursor()

	from_date = end_date + timedelta(days=-1)
	from_date_str = end_date.strftime('%Y-%m-%d') + " 00:00:00"
	asset_amount = get_asset_amount(cursor, userid)
	day_expense = get_total_amount(cursor, userid, from_date_str, end_date_str)

	from_date = end_date + timedelta(days = 1-(int)(end_date.strftime('%w')))
	from_date_str = from_date.strftime('%Y-%m-%d') + " 00:00:00"
	week_expense = get_total_amount(cursor, userid, from_date_str, end_date_str)

	from_date_str = end_date.strftime('%Y-%m-') + "01 00:00:00"
	month_expense = get_total_amount(cursor, userid, from_date_str, end_date_str)

	cursor.close()
	return asset_amount, day_expense, week_expense, month_expense

def get_asset_amount(db_cursor, userid):
	# TODO: change to better way, for performance issue
	sql = "select sum(amount) from expenses where category='收入' and userid='%s';" % (userid)
	db_cursor.execute(sql)
	out = db_cursor.fetchall()
	if out[0][0] is None:
		incoming_amount = config.AMOUNT_NONE
	else:
		incoming_amount = float(out[0][0])

	sql = "select sum(amount) from expenses where category!='收入' and userid='%s';" % (userid)
	db_cursor.execute(sql)
	out = db_cursor.fetchall()
	if out[0][0] is None:
		expense_amount = config.AMOUNT_NONE
	else:
		expense_amount = float(out[0][0])

	return incoming_amount - expense_amount

def get_total_amount(db_cursor, userid, from_date_str, end_date_str):
	sql = "select sum(amount) from expenses where userid=\"%s\" and date>='%s' and date<='%s'" \
			% (userid, from_date_str, end_date_str)
	log.info("SQL: get_total_amount: " + sql)
	print sql
	db_cursor.execute(sql)
	out = db_cursor.fetchall()
	if out[0][0] is None:
		return config.AMOUNT_NONE
	else:
		return float(out[0][0])

def detect_date_amount(token_list):
	record_date = ""
	current_date = datetime.now()
	num_list = []
	for text, start, end in token_list:
		if text.replace('.', '').isdigit():
				if text.isdigit():
						num = int(text)
				else:
						num = float(text)
				if num >= 0 and num <= config.AMOUNT_MAX:
						num_list.append(num)

	# Valid record shall contain at least one number
	if len(num_list) == 0:
		return "", -1

	if len(num_list) == 1:
		amount = num_list[0]
		for text, start, end in token_list:
			if text == "昨天":
				record_date = current_date + timedelta(days=-1)
				record_date = record_date.strftime('%Y-%m-%d') + " 00:00:00"
			if text == "前天":
				record_date = current_date + timedelta(days=-2)
				record_date = record_date.strftime('%Y-%m-%d') + " 00:00:00"
			if text == "大前天":
				record_date = current_date + timedelta(days=-3)
				record_date = record_date.strftime('%Y-%m-%d') + " 00:00:00"

	if len(num_list) > 2 :
		return config.RECORD_STATE_MULTIPLE_RECORDS, -1

	if len(num_list) == 2 :
		amount = -1
		record_date = ""
		for num in num_list:
			if str(num).isdigit() is True and num >= 1 and num <= 31 and record_date == "":
					record_date = util.caculate_date_by_daynum(num)
			else:
					if amount == -1:
						amount = num

	if record_date == "":
		record_date = current_date.strftime('%Y-%m-%d %H:%M:%S')

	return record_date, amount

# TODO: rewrite in erlang or golang later
def detect_branding_category(token_list):
	for text, start, end in token_list:
		if text in brand_category_dict:
			return text, brand_category_dict[text]
	return config.DEFAULT_BRANDING, config.DEFAULT_CATEGORY

def refresh_expense(expenseid):
	sql = "select userid, notes, date, createtime from expenses where expenseid=%s;" % (expenseid)
	out = Expense.query_sql(sql)
	if len(out) == 1:
		userid = out[0][0]
		content = out[0][1]
		date = out[0][2]
		createtime = out[0][3]
		if Expense.delete_obj_by_id(userid, expenseid) is True:
			ret_content = add_expense(userid, content)
			conn = MySQLdb.connect(config.DB_HOST, config.DB_USERNAME, config.DB_PWD, \
							   config.DB_NAME, charset='utf8mb4', port=config.DB_PORT)

			cursor = conn.cursor()

			sql_format = "update expenses as a inner join (select expenseid from " + \
						 " expenses where userid='%s' and notes='%s' limit 1) " + \
						 "as b on a.expenseid = b.expenseid set a.date='%s';"
			sql = sql_format % (userid, content, date)
			cursor.execute(sql)
			conn.commit()

			sql_format = "update expenses as a inner join (select expenseid from " + \
						 " expenses where userid='%s' and notes='%s' limit 1) " + \
						 "as b on a.expenseid = b.expenseid set a.createtime='%s';"
			sql = sql_format % (userid, content, createtime)
			cursor.execute(sql)
			conn.commit()
			print content, ret_content

def refresh_not_detected_expense():
	sql = "select expenseid from expenses where memo!='detected';"
	out = Expense.query_sql(sql)
	for obj in out:
		expenseid = str(obj[0])
		refresh_expense(expenseid)

################################################################
## File : data.py
