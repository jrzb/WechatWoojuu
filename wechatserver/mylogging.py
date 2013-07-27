# -*- coding: utf-8 -*-
#!/usr/bin/python
##-------------------------------------------------------------------
## @copyright 2013
## File : mylogging.py
## Author : filebat <markfilebat@126.com>
## Description :
## --
## Created : <2013-04-11 00:00:00>
## Updated: Time-stamp: <2013-05-25 15:09:57>
##-------------------------------------------------------------------
import logging
from logging.handlers import RotatingFileHandler
format = "%(asctime)s %(filename)s:%(lineno)d - %(levelname)s: %(message)s"
formatter = logging.Formatter(format)

##################### common logging ###########################
log = logging.getLogger('myapp')
Rthandler = RotatingFileHandler('log/woojuu_weixin.log', maxBytes=5*1024*1024,backupCount=5)
Rthandler.setLevel(logging.INFO)
Rthandler.setFormatter(formatter)

consoleHandler = logging.StreamHandler()
consoleHandler.setLevel(logging.INFO)
consoleHandler.setFormatter(formatter)
# log.setLevel(logging.INFO)
log.setLevel(logging.WARNING)
log.addHandler(consoleHandler)
log.addHandler(Rthandler)
################################################################

##################### audit log ################################
auditlog = logging.getLogger('myapp_audit')
audit_rthandler = RotatingFileHandler('log/woojuu_weixin_audit.log', maxBytes=5*1024*1024,backupCount=5)
audit_rthandler.setLevel(logging.INFO)
audit_rthandler.setFormatter(formatter)

auditlog.setLevel(logging.INFO)
auditlog.addHandler(audit_rthandler)
################################################################
## File : mylogging.py
