# -*- coding: utf-8 -*-
#!/usr/bin/python
##-------------------------------------------------------------------
## @copyright 2013
## File : util.py
## Author : filebat <markfilebat@126.com>
## Description :
## --
## Created : <2013-05-25 00:00:00>
## Updated: Time-stamp: <2013-05-30 15:17:28>
##-------------------------------------------------------------------
import pika
import MySQLdb
import config

def query_sql(sql):
	conn = MySQLdb.connect(config.DB_HOST, config.DB_USERNAME, \
		config.DB_PWD, config.DB_NAME, charset = 'utf8mb4', port = config.DB_PORT)
	cursor = conn.cursor()
	cursor.execute(sql)
	out = cursor.fetchall()
	cursor.close()
	return out

def smarty_remove_extra_comma(content):
	if len(content) < 4:
		return content

	if content[-4] == ',':
		content = content[0:-4] + content[-3:]
	return content

def build_mq_connection(queue_name):
	connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
	channel = connection.channel()

	channel.queue_declare(queue=queue_name, durable=True)
	return (channel, connection)

def insert_message(queue_name, message):
	global channel
	channel.basic_publish(exchange='',
						  routing_key=queue_name,
						  body=message,
						  properties=pika.BasicProperties(
							  delivery_mode = 2, # make message persistent
						  ))
	print " [x] Sent %r" % (message,)

	# connection.close() # TODO

def fill_missing_data(data, index_key_list, default_value = '0'):
	for key in index_key_list:
		found = False
		for item in data:
			if key == item[0]:
				found = True
				break
		if found is False:
			print (key, default_value)
			data = data + ((key, default_value),)
	return data

################################################################
# TODO: temporarily disable here
# conn = MySQLdb.connect(config.DB_HOST, config.DB_USERNAME, \
# 					   config.DB_PWD, config.DB_NAME, charset = 'utf8mb4', port = config.DB_PORT)

(channel, connection) = build_mq_connection(config.QUEUE_NAME)
################################################################
## File : util.py