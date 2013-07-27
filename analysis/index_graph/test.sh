#!/bin/bash
##-------------------------------------------------------------------
## @copyright 2013 ShopEx Network Technology Co,.Ltd
## File : test.sh
## Author : filebat <markfilebat@126.com>
## Description :
## --
## Created : <2013-04-20>
## Updated: Time-stamp: <2013-06-09 23:28:53>
##-------------------------------------------------------------------
port=${1:-5000}

function request_url_post() {
    url=${1?}
    data=${2?}
    header=${3:-""}
    if [ `uname` == "Darwin" ]; then
        data=$(echo "$data" | sed "s/\'/\\\\\"/g")
    else
        data=$(echo "$data" | sed "s/'/\\\\\"/g")
    fi;
    command="curl $header -d \"$data\" \"$url\""
    echo -e "\n$command"
    eval "$command"
    if [ $? -ne 0 ]; then
        echo "Error: fail to run $command"; exit -1
    fi
}

function request_url_get() {
    url=${1?}
    command="curl \"$url\""
    echo -e "\n$command"
    eval "$command"
    if [ $? -ne 0 ]; then
        echo "Error: fail to run $command"; exit -1
    fi
}

function request_url_head() {
    url=${1?}
    command="curl -I \"$url\" 2>/dev/null"
    echo -e "\n$command"
    eval "$command" || (echo "Error: fail to run $command" ; exit -1)
}

function index_test() {
    request_url_head "http://127.0.0.1:$port/get_index_daily_user_line?username=oOLGTjiMZ2nhEHcMhSP9Tq_kgLUk&service_name=gh_05d5313dea46&index_key_list=20130524_visit_count;20130525_visit_count;20130526_visit_count"
    request_url_head "http://127.0.0.1:$port/get_index_daily_service_line?service_name=gh_05d5313dea46&index_key_list=20130524_record_count;20130525_record_count;20130526_record_count"
}

echo -e "\nRun http request tests:"
index_test

echo "Done"

## File : test.sh ends