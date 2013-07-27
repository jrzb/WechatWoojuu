#!/bin/bash
##-------------------------------------------------------------------
## @copyright 2013
## File : mail.sh
## Author : filebat <markfilebat@126.com>
## Description : 
## --
## Created : <2013-02-01>
## Updated: Time-stamp: <2013-06-09 14:52:33>
##-------------------------------------------------------------------
# WECHAT_HOME="/home/wwwroot/wechat.woojuu.cc/"

email_list=${1:-"markfilebat@126.com,249950670@qq.com,pitaru@qq.com"}

function ensure_variable_isset() {
    # TODO support sudo, without source
    if [ -z "$WECHAT_HOME" ]; then
        echo "Error: Global variable($XZB_HOME) is not set, which is normally github's checkout path."
        echo "       Please make necessary changes to /etc/profile, then reboot."
        exit 1
    fi
}

function monitor_log_for_error() {
    (cd $WECHAT_HOME/app && make logcheck)
}

ensure_variable_isset

date=`date +%Y-%m-%d_%H:%M`
# monitor error
log_errmsg=$(monitor_log_for_error) || (echo "$log_errmsg" | mail -s "[$date] Woojuu Server Alerts" $email_list)

## File : mail.sh ends
