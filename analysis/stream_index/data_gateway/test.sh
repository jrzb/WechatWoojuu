#!/bin/bash
##-------------------------------------------------------------------
## @copyright 2013 ShopEx Network Technology Co,.Ltd
## File : test.sh
## Author : filebat <markfilebat@126.com>
## Description :
## --
## Created : <2013-04-20>
## Updated: Time-stamp: <2013-06-09 23:28:40>
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

function wechat_simulate_test() {
    token="?signature=7d0e888df44def04c76084d26e92c59fb15c1a50&timestamp=1369459087&nonce=1369763244"
    request_url_post "http://0.0.0.0:$port/api$token" "<xml><ToUserName><![CDATA[gh_05d5313dea46]]></ToUserName><FromUserName><![CDATA[oOLGTjiMZ2nhEHcMhSP9Tq_kgLUk]]></FromUserName><CreateTime>1369366098</CreateTime><MsgType><![CDATA[text]]></MsgType><Content><![CDATA[20 吃饭]]></Content><MsgId>5881769154217771468</MsgId></xml>" "-H 'Content-Type: text/xml'"
    request_url_post "http://0.0.0.0:$port/api$token" "<xml><ToUserName><![CDATA[gh_2fba4c2ef423]]></ToUserName><FromUserName><![CDATA[obF30jl6D2DOpTK78Irx6oCzIQkM]]></FromUserName><CreateTime>1369357295</CreateTime><MsgType><![CDATA[event]]></MsgType><Event><![CDATA[subscribe]]></Event><EventKey><![CDATA[]]></EventKey></xml>" "-H 'Content-Type: text/xml'"

    request_url_post "http://0.0.0.0:$port/api$token" "<xml><ToUserName><![CDATA[gh_05d5313dea46]]></ToUserName><FromUserName><![CDATA[oOLGTjiMZ2nhEHcMhSP9Tq_kgLUk]]></FromUserName><CreateTime>1369456098</CreateTime><MsgType><![CDATA[text]]></MsgType><Content><![CDATA[20 吃饭]]></Content><MsgId>5881769154217771468</MsgId></xml>" "-H 'Content-Type: text/xml'"
    request_url_post "http://0.0.0.0:$port/api$token" "<xml><ToUserName><![CDATA[gh_2fba4c2ef423]]></ToUserName><FromUserName><![CDATA[obF30jl6D2DOpTK78Irx6oCzIQkM]]></FromUserName><CreateTime>1369457295</CreateTime><MsgType><![CDATA[event]]></MsgType><Event><![CDATA[subscribe]]></Event><EventKey><![CDATA[]]></EventKey></xml>" "-H 'Content-Type: text/xml'"

    request_url_post "http://0.0.0.0:$port/api$token" "<xml><ToUserName><![CDATA[gh_05d5313dea46]]></ToUserName><FromUserName><![CDATA[oOLGTjiMZ2nhEHcMhSP9Tq_kgLUk]]></FromUserName><CreateTime>1369566098</CreateTime><MsgType><![CDATA[text]]></MsgType><Content><![CDATA[20 吃饭]]></Content><MsgId>5881769154217771468</MsgId></xml>" "-H 'Content-Type: text/xml'"
    request_url_post "http://0.0.0.0:$port/api$token" "<xml><ToUserName><![CDATA[gh_2fba4c2ef423]]></ToUserName><FromUserName><![CDATA[obF30jl6D2DOpTK78Irx6oCzIQkM]]></FromUserName><CreateTime>1369557295</CreateTime><MsgType><![CDATA[event]]></MsgType><Event><![CDATA[subscribe]]></Event><EventKey><![CDATA[]]></EventKey></xml>" "-H 'Content-Type: text/xml'"

}

function get_index_test() {
    request_url_get "http://127.0.0.1:$port/get_index_userprofile?username=oOLGTjiMZ2nhEHcMhSP9Tq_kgLUk&service_name=gh_05d5313dea46&index_key_list=20130524_visit_count;20130525_visit_count;20130526_visit_count"
    request_url_get "http://127.0.0.1:$port/get_index_serviceprofile?service_name=gh_05d5313dea46&index_key_list=20130524_record_count;20130525_record_count;20130526_record_count"
}

echo -e "\nRun http request tests:"
wechat_simulate_test
get_index_test

echo "Done"

## File : test.sh ends