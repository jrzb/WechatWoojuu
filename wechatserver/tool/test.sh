#!/bin/bash
##-------------------------------------------------------------------
## @copyright 2013 ShopEx Network Technology Co,.Ltd
## File : test.sh
## Author : filebat <markfilebat@126.com>
## Description :
## --
## Created : <2013-04-20>
## Updated: Time-stamp: <2013-06-15 15:42:31>
##-------------------------------------------------------------------
. $(dirname $0)/utility.sh

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
    request_url_post "http://0.0.0.0:$port/api$token" "<xml><ToUserName><![CDATA[gh_05d5313dea46]]></ToUserName><FromUserName><![CDATA[oOLGTjiMZ2nhEHcMhSP9Tq_kgLUk]]></FromUserName><CreateTime>1369366098</CreateTime><MsgType><![CDATA[text]]></MsgType><Content><![CDATA[安静]]></Content><MsgId>5881769154217771468</MsgId></xml>" "-H 'Content-Type: text/xml'"

    request_url_post "http://0.0.0.0:$port/api$token" "<xml><ToUserName><![CDATA[gh_05d5313dea46]]></ToUserName><FromUserName><![CDATA[oOLGTjiMZ2nhEHcMhSP9Tq_abcefef]]></FromUserName><CreateTime>1369366098</CreateTime><MsgType><![CDATA[text]]></MsgType><Content><![CDATA[20 吃饭]]></Content><MsgId>5881769154217771468</MsgId></xml>" "-H 'Content-Type: text/xml'"

    request_url_post "http://0.0.0.0:$port/api$token" "<xml><ToUserName><![CDATA[gh_05d5313dea46]]></ToUserName><FromUserName><![CDATA[oOLGTjiMZ2nhEHcMhSP9Tq_kgLUk]]></FromUserName><CreateTime>1369366098</CreateTime><MsgType><![CDATA[text]]></MsgType><Content><![CDATA[20 吃饭]]></Content><MsgId>5881769154217771468</MsgId></xml>" "-H 'Content-Type: text/xml'"
    request_url_post "http://0.0.0.0:$port/api$token" "<xml><ToUserName><![CDATA[gh_2fba4c2ef423]]></ToUserName><FromUserName><![CDATA[obF30jl6D2DOpTK78Irx6oCzIQkM]]></FromUserName><CreateTime>1369357295</CreateTime><MsgType><![CDATA[event]]></MsgType><Event><![CDATA[subscribe]]></Event><EventKey><![CDATA[]]></EventKey></xml>" "-H 'Content-Type: text/xml'"

    request_url_post "http://0.0.0.0:$port/api$token" "<xml><ToUserName><![CDATA[gh_05d5313dea46]]></ToUserName><FromUserName><![CDATA[oOLGTjiMZ2nhEHcMhSP9Tq_kgLUk]]></FromUserName><CreateTime>1369456098</CreateTime><MsgType><![CDATA[text]]></MsgType><Content><![CDATA[20 吃饭]]></Content><MsgId>5881769154217771468</MsgId></xml>" "-H 'Content-Type: text/xml'"
    request_url_post "http://0.0.0.0:$port/api$token" "<xml><ToUserName><![CDATA[gh_2fba4c2ef423]]></ToUserName><FromUserName><![CDATA[obF30jl6D2DOpTK78Irx6oCzIQkM]]></FromUserName><CreateTime>1369457295</CreateTime><MsgType><![CDATA[event]]></MsgType><Event><![CDATA[subscribe]]></Event><EventKey><![CDATA[]]></EventKey></xml>" "-H 'Content-Type: text/xml'"

    request_url_post "http://0.0.0.0:$port/api$token" "<xml><ToUserName><![CDATA[gh_05d5313dea46]]></ToUserName><FromUserName><![CDATA[oOLGTjiMZ2nhEHcMhSP9Tq_kgLUk]]></FromUserName><CreateTime>1369566098</CreateTime><MsgType><![CDATA[text]]></MsgType><Content><![CDATA[h]]></Content><MsgId>5881769154217771468</MsgId></xml>" "-H 'Content-Type: text/xml'"
    request_url_post "http://0.0.0.0:$port/api$token" "<xml><ToUserName><![CDATA[gh_05d5313dea46]]></ToUserName><FromUserName><![CDATA[oOLGTjiMZ2nhEHcMhSP9Tq_kgLUk]]></FromUserName><CreateTime>1369566098</CreateTime><MsgType><![CDATA[text]]></MsgType><Content><![CDATA[20 吃饭]]></Content><MsgId>5881769154217771468</MsgId></xml>" "-H 'Content-Type: text/xml'"
    request_url_post "http://0.0.0.0:$port/api$token" "<xml><ToUserName><![CDATA[gh_2fba4c2ef423]]></ToUserName><FromUserName><![CDATA[obF30jl6D2DOpTK78Irx6oCzIQkM]]></FromUserName><CreateTime>1369557295</CreateTime><MsgType><![CDATA[event]]></MsgType><Event><![CDATA[subscribe]]></Event><EventKey><![CDATA[]]></EventKey></xml>" "-H 'Content-Type: text/xml'"

}
function server_test() {
    request_url_get "http://wechat.woojuu.cc/summary?userid=obF30jr0VD4HUjUq1kYusd5gSCBo&categories=&fromdate=2013-02-29%202012:08:03&enddate=2013-04-29%202012:08:03"
    request_url_get "http://wechat.woojuu.cc/summary?userid=obF30jr0VD4HUjUq1kYusd5gSCBo&categories=早午晚餐;公共交通&fromdate=2013-02-29%202012:08:03&enddate=2013-04-29%202012:08:03"
    request_url_get "http://wechat.woojuu.cc/list_expense?userid=obF30jr0VD4HUjUq1kYusd5gSCBo&fromdate=2013-05-01%202012:08:03&enddate=2013-05-20%202012:08:03"
    request_url_get "http://wechat.woojuu.cc/topn_category?userid=obF30jr0VD4HUjUq1kYusd5gSCBo&fromdate=2013-05-01%202012:08:03&enddate=2013-05-20%202012:08:03&limit=2"
    request_url_get "http://wechat.woojuu.cc/summary_daily?userid=obF30jr0VD4HUjUq1kYusd5gSCBo&fromdate=2013-05-01%202012:08:03&enddate=2013-05-20%202012:08:03"
}

function local_test () {
    request_url_get "http://0.0.0.0:$port/summary?userid=dennyledger&categories=&fromdate=2013-02-29%2012:08:03&enddate=2013-04-29%2012:08:03"
    request_url_get "http://0.0.0.0:$port/summary?userid=dennyledger&categories=早午晚餐;公共交通&fromdate=2013-02-29%2012:08:03&enddate=2013-04-29%2012:08:03"
    request_url_get "http://0.0.0.0:$port/list_expense?userid=dennyledger&fromdate=2013-04-01%2012:08:03&enddate=2013-04-03%2012:08:03"
    request_url_post "http://0.0.0.0:$port/delete_expense" "userid=dennyledger&expenseid=123"
    request_url_post "http://0.0.0.0:$port/add_expense" "userid=dennyledger&notes=37 超大杯星巴克焦糖玛奇朵"
    request_url_post "http://0.0.0.0:$port/add_expense" "userid=dennyledger&notes=37 一些测试"
    request_url_get "http://0.0.0.0:$port/topn_category?userid=dennyledger&fromdate=2013-01-01%2012:08:03&enddate=2013-05-20%2012:08:03&limit=2"
    request_url_get "http://0.0.0.0:$port/category_daily?userid=dennyledger&fromdate=2013-04-18%2012:08:03&enddate=2013-04-20%2012:08:03"
    request_url_get "http://0.0.0.0:$port/summary_daily?userid=dennyledger&fromdate=2013-04-04%2012:08:03&enddate=2013-04-06%2012:08:03"
}

echo -e "\nRun http request tests:"

# request_url_get "http://0.0.0.0:$port/add_expense?userid=dennyledger&expense=37,超大杯星巴克焦糖玛奇朵" && \
# request_url_get "http://0.0.0.0:$port/view_history?userid=dennyledger" && \
# request_url_get "http://0.0.0.0:$port/add_expense?userid=dennyledger&expense=37,超大杯星巴克焦糖玛奇朵" && \

# server_test
local_test
wechat_simulate_test
echo "Done"

## File : test.sh ends