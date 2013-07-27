# -*- coding: utf-8 -*-
#!/usr/bin/python
##-------------------------------------------------------------------
## @copyright 2013
## File : chat_aiml.py
## Author : filebat <markfilebat@126.com>
## Description :
## --
## Created : <2013-01-25 00:00:00>
## Updated: Time-stamp: <2013-06-15 15:51:25>
##-------------------------------------------------------------------
import sys
#sys.path.insert(0, "../")

import aiml

def init_aiml():
	# The Kernel object is the public interface to
	# the AIML interpreter.
	k = aiml.Kernel()
	
	# Use the 'learn' method to load the contents
	# of an AIML file into the Kernel.
	k.learn("./aiml_chat/cn-startup.xml")
	
	k.respond("load aiml cn")
	return k

def respond_msg(input_msg):
	global aiml_kernel
	msg = aiml_kernel.respond(input_msg)
	return msg.replace(" ", "")

aiml_kernel = init_aiml()
##############################################################################
## File : chat_aiml.py