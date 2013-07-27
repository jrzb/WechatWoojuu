#!/bin/bash
##-------------------------------------------------------------------
## @copyright 2013
## File : crontab.sh
## Author : filebat <markfilebat@126.com>
## Description : 
## --
## Created : <2013-02-01>
## Updated: Time-stamp: <2013-06-09 14:53:20>
##-------------------------------------------------------------------
# WECHAT_HOME="/home/wwwroot/wechat.woojuu.cc/"

email_list=${1:-"markfilebat@126.com,249950670@qq.com,pitaru@qq.com"}

$WECHAT_HOME/tool/gen_report.sh $email_list
#$WECHAT_HOME/tool/mail.sh $email_list

find $WECHAT_HOME/app/static/img/R -name "*.png" -mtime +3 -exec /bin/rm {} \;
## File : crontab.sh ends
