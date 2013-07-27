#!/usr/bin/python
##-------------------------------------------------------------------
## @copyright 2013 ShopEx Network Technology Co,.Ltd
## File : eventtrigger.py
## Author : filebat <markfilebat@126.com>
## Description :
## --
## Created : <2013-05-25>
## Updated: Time-stamp: <2013-06-19 13:24:34>
##-------------------------------------------------------------------
import pika
import sys
import xml.etree.ElementTree as ET

import config
import storemsg
import detectindex
import util

import logging
logging.getLogger('pika').setLevel(logging.DEBUG) # TODO set to other level

default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
	reload(sys)
	sys.setdefaultencoding(default_encoding)

def get_message(queue_name, mq_host = config.MQ_HOST):
	connection = pika.BlockingConnection(pika.ConnectionParameters(host=mq_host))
	channel = connection.channel()

	channel.queue_declare(queue=queue_name, durable=True)
	#print ' [*] Waiting for messages. To exit press CTRL+C'

	channel.basic_qos(prefetch_count=1)
	channel.basic_consume(callback, queue=queue_name)

	channel.start_consuming()
	#connection.close()		

def callback(ch, method, properties, body):
	print " [x] Received %r" % (body,)
	# time.sleep( body.count('.') )
	print " [x] Done"

	hooks = [
			storemsg.store_raw,
			storemsg.store_mysql,
			detectindex.detect_user_last_visit_time,
			detectindex.detect_user_daily_visit_count,
			detectindex.detect_daily_subscribe_count,
			detectindex.detect_daily_unsubscribe_count,
			detectindex.detect_daily_record_count,
			detectindex.detect_daily_valid_record_count,
			detectindex.detect_user_count,
			detectindex.detect_daily_record_pattern,
			detectindex.detect_user_subscribe_time,
			detectindex.detect_daily_uniq_user_count,
			detectindex.alert_voice_input,
	]

	apply_hooks(body, hooks)
	ch.basic_ack(delivery_tag = method.delivery_tag)

def apply_hooks(msg, hooks):
	msg_dict = util.parse_msg(msg)
	for hook in hooks:
		print hook
		hook(msg, msg_dict)

################################################################
## File : eventtrigger ends
