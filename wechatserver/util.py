# -*- coding: utf-8 -*-
#!/usr/bin/python
##-------------------------------------------------------------------
## @copyright 2013
## File : util.py
## Author : filebat <markfilebat@126.com>
## Description :
## --
## Created : <2013-04-11 00:00:00>
## Updated: Time-stamp: <2013-06-06 23:12:47>
##-------------------------------------------------------------------
import xml.etree.ElementTree as ET
import const_message as MSG
import time
import calendar
import datetime as datetime1
from datetime import datetime
from datetime import timedelta
from mylogging import log

import config
import pika

from pymmseg import mmseg

mmseg.dict_load_defaults()
mmseg.dict_load_words("dict_conf/woojuu.dic")

################################################################
# python -c "import util; util.word_split('37,超大杯星巴克焦糖玛奇朵', 2)"
def word_split(sentence, shall_print=0):
	# python word split is incorrect for float, for example,"16.5 中午吃饭",
	# will be splited as "16 5 中午吃饭", instead of "16.5 中午 吃饭"
	SPECIAL_CHARACTER_FOR_FLOAT='a'
	sentence=sentence.replace('。', SPECIAL_CHARACTER_FOR_FLOAT)
	sentence=sentence.replace('.', SPECIAL_CHARACTER_FOR_FLOAT)
	algor = mmseg.Algorithm(sentence)
	token_list = []
	for tok in algor:
		if tok.text.replace(SPECIAL_CHARACTER_FOR_FLOAT, '0').isdigit():
			token_list.append((tok.text.replace(SPECIAL_CHARACTER_FOR_FLOAT, '.'), \
				tok.start, tok.end))
		else:
			token_list.append((tok.text, tok.start, tok.end))

	# temporarily print
	for text, start, end in token_list:
		if shall_print == 1:
			log.info("%s, %d, %d" % (text, start, end))
		else:
			if shall_print == 2:
				print "%s, %d, %d" % (text, start, end)

	return token_list

def wash_sentence(sentence):
	sentence = sentence.replace("  ", " ")
	sentence = sentence.strip(" ")
	if sentence.endswith("."):
		sentence = sentence[0:-1]
	if sentence.endswith("。"):
		sentence = sentence[0:-len("。")]
	# sentence = sentence.replace(u"""？""", "?")
	# sentence = sentence.replace(u"""，""", ",")
	return sentence

def _parse_msg(raw_msg):
	"""
	http://docs.python.org/2/library/xml.etree.elementtree.html#xml.etree.ElementTree.XML
	"""
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

def _response_new_subscription(msg):
	return _response_text_msg(msg, MSG.REPLY_WELCOME)

def _response_new_unsubscription(msg):
	return _response_text_msg(msg, MSG.REPLY_WELCOME)

def _response_text_msg(msg, content):
	"""
	Sample:
	---
	<xml>
	<ToUserName><![CDATA[toUser]]></ToUserName>
	<FromUserName><![CDATA[fromUser]]></FromUserName>
	<CreateTime>1348831860</CreateTime>
	<MsgType><![CDATA[text]]></MsgType>
	<Content><![CDATA[this is a test]]></Content>
	<MsgId>1234567890123456</MsgId>
	</xml>
	"""
	s = _to_xml(to_user_name=msg['FromUserName'],
				from_user_name=msg['ToUserName'],
				create_time=str(int(time.time())),
				msg_type='text',
				content=content,
				func_flag='0')
	return s


def _response_single_picture_msg(msg, title, description, picurl, url):
	"""
	Sample:
	---
	<xml>
	<ToUserName><![CDATA[toUser]]></ToUserName>
	<FromUserName><![CDATA[fromUser]]></FromUserName>
	<CreateTime>12345678</CreateTime>
	<MsgType><![CDATA[news]]></MsgType>
	<ArticleCount>1</ArticleCount>
	<Articles>
	<item>
	<Title><![CDATA[title1]]></Title> 
	<Description><![CDATA[description1]]></Description>
	<PicUrl><![CDATA[picurl]]></PicUrl>
	<Url><![CDATA[url]]></Url>
	</item>
	</Articles>
	<FuncFlag>1</FuncFlag>
	</xml>
	"""
	msg["MsgType"] = "news"
	FromUserName = msg["ToUserName"]
	msg["ToUserName"] = msg["FromUserName"]
	msg["FromUserName"] = FromUserName
	xml = '<xml>'
	for k in ['ToUserName', 'FromUserName', 'CreateTime', 'MsgType']:
		xml += '<%s>%s</%s>' % (k, _cdata(msg[k]), k)

	# add article
	s = u"""%s
	<ArticleCount>1</ArticleCount>
	<Articles>
	<item>
	<Title>%s</Title>
	<Description>%s</Description>
	<PicUrl>%s</PicUrl>
	<Url>%s</Url>
	</item>
	</Articles>
	</xml>
""" % (xml, title, description, picurl, url)

	log.info(s.encode('utf-8', 'ignore'))
	return s


def _is_new_subscription(msg):
	"""
	New subscription
	"""
	return msg['MsgType'] == 'event' and msg['Event'] == 'subscribe'

def _is_new_unsubscription(msg):
	"""
	New subscription
	"""
	return msg['MsgType'] == 'event' and msg['Event'] == 'unsubscribe'

def _is_code(msg):
	code = msg['Content'].lower()
	return code in [MSG.CODE_MANUAL, MSG.CODE_HISTORY]

def smarty_remove_extra_comma(content):
	if content[-2] == ',':
		content = content[0:-2] + content[-1]
	return content

def get_date_list(fromdate, enddate):
	fromdate = fromdate[0:10]
	enddate = enddate[0:10]
	date_list = []
	date_object = datetime.strptime(fromdate, "%Y-%m-%d")

	while date_object.strftime("%Y-%m-%d") <= enddate:
		date_list.append(date_object.strftime("%Y-%m-%d"))
		date_object = date_object + timedelta(days=1)

	return date_list

def remove_amount_from_comment(comment, amount):
	amount_str = str(amount).replace(".0", "")
	if amount != -1:
		comment = comment.replace(amount_str+"元", "")
		comment = comment.replace(amount_str+"块", "")
		comment = comment.replace(amount_str, "")
		comment = wash_sentence(comment)
	return comment

def format_float_str(amount_str):
	amount_f = "%.1f" % float(amount_str)
	return str(amount_f).replace(".0", "")

def predict_amount(current_amount, current_date = None):
	if current_date is None:
		current_date = datetime1.date
	return current_amount * calendar.mdays[current_date.today().month]/current_date.today().day

def caculate_date_by_daynum(num):
	current_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	current_year = int(current_date[0:4])
	current_month = int(current_date[5:7])
	current_day = int(current_date[8:10])
	date_ret = ""
	if num <= int(current_day):
			date_ret = "%s-%s-%s 00:00:00" % (str(current_year).zfill(4), \
														  str(current_month).zfill(2), str(num).zfill(2))
	else:
			month = current_month - 1
			if month <= 0:
					month = 12
					year = current_year - 1
			else:
					year = current_year
			date_ret = "%s-%2s-%s 00:00:00" % (str(year).zfill(4),\
											   str(month).zfill(2), str(num).zfill(2))
	return date_ret

def connect_to_queue(mq_server, queue_name):
	connection = pika.BlockingConnection(pika.ConnectionParameters(host=mq_server))
	channel = connection.channel()

	channel.queue_declare(queue=queue_name, durable=True)
	return connection, channel

def message_to_queue(queue_channel, queue_name, message):
	if config.SHOULD_LOG_MQ == False:
		return
	# TODO: return status
	queue_channel.basic_publish(exchange='',
		routing_key=queue_name, body=message,
		properties=pika.BasicProperties(
			delivery_mode = 2, # make message persistent
			))

def disconnect_queue(queue_connection):
	queue_connection.close()

################################################################
## File : util.py