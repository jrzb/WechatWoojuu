# -*- coding: utf-8 -*-
##-------------------------------------------------------------------
## @copyright 2013
## File : app.py
## Author : filebat <markfilebat@126.com>
## Description :
## --
## Created : <2013-04-11 00:00:00>
## Updated: Time-stamp: <2013-06-15 20:39:19>
##-------------------------------------------------------------------
import random
import sys
import os
from aiml_chat import chat_aiml

import hashlib
from flask import Flask, request, render_template, url_for
from flask import send_file

from data import view_history, search_record, add_expense
from data import reply_voice, reply_image, delete_last_record
from mylogging import log, auditlog
import util
from util import smarty_remove_extra_comma
import config

from expense import Expense
import const_message as MSG
import const_emoji
import logging
logging.getLogger('pika').setLevel(logging.DEBUG)

default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
	reload(sys)
	sys.setdefaultencoding(default_encoding)

APP_ROOT = os.path.dirname(os.path.realpath(__file__))
# TODO: use exchange, instead of direct queue
if config.SHOULD_LOG_MQ is True:
	(queue_connection, QUEUE_CHANNEL) = util.connect_to_queue(config.MQ_SERVER, config.QUEUE_NAME)
else:
	queue_connection = None
	QUEUE_CHANNEL = None

## Add timestamp to static css/js files loaded by url_for to prevent from caching
def static(filename):
	filepath = os.path.join(os.path.dirname(__file__), 'static', filename)
	last_modification = '%d' % os.path.getmtime(filepath)
	return url_for('.static', filename=filename) + '?' + last_modification

def create_app():
	app = Flask(__name__)
	app.config.from_pyfile('config.py')

	# overriding default jinja template tags, to avoid conflicts with angularjs
	app.jinja_env.variable_start_string = '{['
	app.jinja_env.variable_end_string = ']}'

	# load function
	app.jinja_env.globals.update(format_float_str=util.format_float_str)
	app.jinja_env.globals.update(remove_amount_from_comment=util.remove_amount_from_comment)
	app.jinja_env.globals.update(get_emoji_html_escape=const_emoji.get_emoji_html_escape)

	@app.context_processor
	def inject_static():
		return dict(static=static)
	return app

app = create_app()

@app.route('/')
def home():
	## For release
	# return send_file('templates/index.html')
	# For development:
	# with open(os.path.join(app.config['APP_TEMPLATES'], 'index.html')) as f:
	# 	return make_response(f.read())
	return render_template('index.html')

@app.route('/api', methods=['GET'])
def api_wechat_auth():
	audit_log(request)
	echostr = request.args.get('echostr')
	if _verification(request) and echostr is not None:
		return echostr
	return "access verification fail"

# For WeiXin API verification
@app.route('/api', methods=['POST'])
def api_wechat_msg():
	audit_log(request)
	global QUEUE_CHANNEL
	## try:
	if _verification(request):
		data = request.data
		if data == "":
			auditlog.error("request.data is empty")
		msg = util._parse_msg(data)

		util.message_to_queue(QUEUE_CHANNEL, config.QUEUE_NAME, data)
		
		if util._is_new_subscription(msg):
			ret = util._response_new_subscription(msg)
		else:
			if util._is_new_unsubscription(msg):
				ret = util._response_new_unsubscription(msg)
			else:
				ret = _response_code(msg)

		util.message_to_queue(QUEUE_CHANNEL, config.QUEUE_NAME, ret)
		return ret
	# except Exception, e:
	# 	log.error(str(sys.exc_info()))
	# 	log.error("api_wechat_msg error: " + str(e))
	# 	return "proceed msg fail"


# Total summary
@app.route('/summary', methods=['GET'])
def api_summary():
	userid = request.args.get('userid', '')
	categories = request.args.get('categories', '')
	fromdate = request.args.get('fromdate', '')
	enddate = request.args.get('enddate', '')

	if categories == "":
		category_list = []
	else:
		category_list = categories.split(";")
	if len(category_list) == 0:
		sql = "select 'ALL' as name, sum(amount) as amount from expenses" + \
			" where userid='" + userid +"' and date>='" + fromdate + \
			"' and date<='" + enddate + "'"
	else:
		categories = ",".join(["'%s'" % (k) for k in category_list])
		sql = "select category as name, sum(amount) as amount from expenses" + \
			" where userid='" + userid +"' and date>='" + fromdate + \
			"' and date<='" + enddate + "' and category in ("+ \
			categories +") group by category"

	out = Expense.query_sql(sql)
	if len(out) == 0:
		out = []
	else:
		if len(out) == 1:
			if out[0][1] is None:
				out = []

	content = render_template('summary.json', objs=out)
	content = smarty_remove_extra_comma(content)
	return content

@app.route('/list_expense', methods=['GET'])
def api_expense_detail():
	userid = request.args.get('userid', '')
	fromdate = request.args.get('fromdate', '')
	enddate = request.args.get('enddate', '')

	out = Expense.query_obj_by_date(userid, fromdate, enddate)
	content = render_template('list_expense.json', objs=out)
	content = smarty_remove_extra_comma(content)
	return content


@app.route('/topn_category', methods=['GET'])
def api_topn_category():
	userid = request.args.get('userid', '')
	limit = request.args.get('limit', '')
	fromdate = request.args.get('fromdate', '')
	enddate = request.args.get('enddate', '')

	sql_format = "select category, sum(amount) as amount from expenses" + \
				 " where userid='%s' and date >='%s' and date<='%s'" + \
				 " group by category order by sum(amount) desc limit %s;"
	sql = sql_format % (userid, fromdate, enddate, limit)
	out = Expense.query_sql(sql)
	content = render_template('topn_category.json', objs=out)
	content = smarty_remove_extra_comma(content)
	return content


@app.route('/summary_daily', methods=['GET'])
def api_summary_daily():
	userid = request.args.get('userid', '')
	fromdate = request.args.get('fromdate', '')
	enddate = request.args.get('enddate', '')

	sql_format = "select left(date, 10), sum(amount) from expenses" + \
				 " where userid='%s' and date >='%s' and date<='%s' group by left(date, 10) order by left(date, 10) asc;"
	sql = sql_format % (userid, fromdate, enddate)

	out = Expense.query_sql(sql)

	date_list = util.get_date_list(fromdate, enddate)
	date_dict = {}
	for date in date_list:
		date_dict[date] = "0"

	for entry in out:
		date_dict[entry[0]] = entry[1]

	key_list = sorted(date_dict.keys())

	content = render_template('summary_daily.json', key_list=key_list, date_dict=date_dict)
	content = smarty_remove_extra_comma(content)
	return content

@app.route('/category_daily', methods=['GET'])
def api_category_daily():
	userid = request.args.get('userid', '')
	fromdate = request.args.get('fromdate', '')
	enddate = request.args.get('enddate', '')

	sql_format = "select category, left(date, 10), sum(amount) from expenses" + \
				 " where userid='%s' and date >='%s' and date<='%s' group by category, " + \
				 "left(date, 10) order by left(date, 10) asc;"
	sql = sql_format % (userid, fromdate, enddate)

	out = Expense.query_sql(sql)
	content = render_template('category_daily.json', objs=out)
	content = smarty_remove_extra_comma(content)
	return content

@app.route('/delete_expense', methods=['POST'])
def api_delete_expense():
	userid = request.values["userid"]
	expenseid = request.values["expenseid"]
	if Expense.delete_obj_by_id(userid, expenseid) is True:
		content = """
		{
			"errorcode":"200",
			"message":"删除成功"
		}
"""
	else:
		content = """
		{
			"errorcode":"500",
			"message":"删除失败"
		}
"""
	return content

@app.route('/add_expense', methods=['POST'])
def api_add_expense():
	userid = request.values["userid"]
	notes = request.values["notes"]
	msg = add_expense(userid, notes)
	# TODO: report error
	content = """
	{
		"errorcode":"200",
		"message":"%s"
	}
	""" % msg
	return content

@app.route('/aiml_chat', methods=['POST'])
def aiml_chat():
	msg = request.values["msg"]
	# TODO: report error
	content = "%s" % (chat_aiml.respond_msg(msg))
	return content

@app.route('/qrcode', methods=['GET'])
def api_get_qrcode():
	filename = os.path.join(APP_ROOT, 'static', 'img/qrcode-banner.png')
	# filename = url_for('static', filename='img/sprite.png')
	return send_file(filename, mimetype='image/png')

@app.route('/u/<userid>')
@app.route('/u/<userid>/details')
def report(userid):
	"""main page"""
	return render_template('index.html')

################################################################

## bypass cross domain security
@app.after_request
def after_request(response):
	response.headers.add('Access-Control-Allow-Origin', '*')  # TODO: to be more secured
	response.headers.add('Access-Control-Allow-Methods', 'GET')
	response.headers.add('Access-Control-Allow-Headers', 'X-Requested-With')
	return response
################################################################

################# private functions ############################
def _response_code(msg):
	if msg['MsgType'] == 'voice':
		content = reply_voice(msg)
		return util._response_text_msg(msg, content)

	if msg['MsgType'] == 'image':
		content = reply_image(msg)
		return util._response_text_msg(msg, content)

	code = msg['Content'].lower().strip()
	if code.endswith("。"):
		code = code[:len("。")]

	if code == MSG.CODE_MUTE:
		return util._response_text_msg(msg, MSG.REPLY_MUTE)
	if code == MSG.CODE_MANUAL or code == MSG.CODE_MANUAL2 or code == MSG.CODE_MANUAL3:
		return util._response_text_msg(msg, MSG.REPLY_MANUAL)
	if code == MSG.CODE_MORE or code == MSG.CODE_MORE2:
		return util._response_text_msg(msg, MSG.REPLY_MANUAL_MORE)
	if code == MSG.CODE_MORE_MORE or code == MSG.CODE_MORE_MORE2:
		return util._response_text_msg(msg, MSG.REPLY_MANUAL_MORE_MORE)

	if code == MSG.CODE_HISTORY:
		userid = msg['FromUserName']
		content = view_history(userid)
		url = "http://h.woojuu.cc/u/%s" % (userid)
		picurl = ""
		return util._response_single_picture_msg(msg, "消费历史", content, picurl, url)
	if code == MSG.CODE_QRCODE:
		return util._response_single_picture_msg(msg, "莴苣二维码", "扫扫二维码，添加莴苣微信公众号", "http://wechat.woojuu.cc/qrcode", "")
	if code.find(MSG.CODE_SEARCH) == 0 or code.find(MSG.CODE_SEARCH2) == 0 \
	   or code.find(MSG.CODE_SEARCH3) == 0:
		content = search_record(msg['FromUserName'], msg['Content'])
		return util._response_text_msg(msg, content)
	if code == MSG.CODE_DELETE:
		content = delete_last_record(msg['FromUserName'])
		return util._response_text_msg(msg, content)

	content = add_expense(msg['FromUserName'], msg['Content'])
	return util._response_text_msg(msg, content)

def _verification(request):
	"""
	http://docs.python.org/2/library/hashlib.html
	"""
	token = app.config["API_TOKEN"]
	signature = request.args.get('signature')
	timestamp = request.args.get('timestamp')
	nonce = request.args.get('nonce')
	s = [timestamp, nonce, token]
	s.sort()
	s = ''.join(s)
	if hashlib.sha1(s).hexdigest() == signature:
		return True
	return False

def audit_log(request):
	# from direct http request
	if request.values.has_key("userid"):
		userid = request.values["userid"]
	else:
		userid = "weixin"
		try:
			# from weixin
			data = request.data
			msg = util._parse_msg(data)
			userid = msg["FromUserName"]
		except Exception, e:
			log.error(sys.exc_info())
			log.error("audit_log error: " + str(e))
			log.error("raw_msg: " + str(data))
	
	useragent = request.headers.get('User-Agent')
	auditlog.info("User(%s) request path: %s. User agent: %s" \
						% (userid, request.path, useragent))

################################################################

if __name__ == '__main__':
	#global QUEUE_CHANNEL
	random.seed()
	# app.run(host="0.0.0.0", port = int(config.FLASK_SERVER_PORT))
	#(queue_connection, QUEUE_CHANNEL) = util.connect_to_queue(config.MQ_SERVER,config.QUEUE_NAME)
	app.run()
	#util.disconnect_queue(queue_connection) # TODO release resource

## File : app.py
