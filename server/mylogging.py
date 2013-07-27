# -*- coding: utf-8 -*-
#!/usr/bin/python
##-------------------------------------------------------------------
## @copyright 2013
## File : mylogging.py
## Author : filebat <markfilebat@126.com>
## Description :
## --
## Created : <2013-05-22 00:00:00>
## Updated: Time-stamp: <2013-05-22 22:31:53>
##-------------------------------------------------------------------
import logging
from logging.handlers import RotatingFileHandler
format = "%(asctime)s %(message)s"
formatter = logging.Formatter(format)

##################### access log ################################
mylog = logging.getLogger('webchat.io')
mylog_rthandler = RotatingFileHandler('wechat_io.log', maxBytes=5*1024*1024, backupCount=5, encoding="utf-8")
mylog_rthandler.setLevel(logging.INFO)
mylog_rthandler.setFormatter(formatter)

mylog.setLevel(logging.INFO)
mylog.addHandler(mylog_rthandler)
################################################################

################################################################
## File : mylogging.py
