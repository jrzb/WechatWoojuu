# -*- coding: utf-8 -*-
#!/usr/bin/R
##-------------------------------------------------------------------
## @copyright 2013
## File : report.R
## Author : filebat <markfilebat@126.com>
## Description :
## --
## Created : <2013-04-04>
## Updated: Time-stamp: <2013-05-26 08:55:03>
##-------------------------------------------------------------------

source(paste(Sys.getenv(x = "WECHAT_HOME"), "/R/util.R", sep="", collapse=""))

args<-commandArgs(TRUE)
picprefix=""
if (length(args) > 0) {
  picprefix = args[1]
}

###########################################################################
fun1(picprefix=picprefix)
fun2(picprefix=picprefix)
fun3(picprefix=picprefix)
fun4(picprefix=picprefix)
fun5(picprefix=picprefix)
fun6(picprefix=picprefix)

### File : report.R ends
