#!/bin/bash
##-------------------------------------------------------------------
## @copyright 2013 ShopEx Network Technology Co,.Ltd
## File : aiml_chat_test.sh
## Author : filebat <markfilebat@126.com>
## Description :
## --
## Created : <2013-04-20>
## Updated: Time-stamp: <2013-06-15 20:11:43>
##-------------------------------------------------------------------
. $(dirname $0)/utility.sh
port=${1:-5000}

function local_test () {
    request_url_post "http://0.0.0.0:$port/aiml_chat" "msg=你好呀"
    request_url_post "http://0.0.0.0:$port/aiml_chat" "msg=收入怎么删除"
    request_url_post "http://0.0.0.0:$port/aiml_chat" "msg=删除功能"
    request_url_post "http://0.0.0.0:$port/aiml_chat" "msg=记错了"
    request_url_post "http://0.0.0.0:$port/aiml_chat" "msg=这个是怎么一回事呀"
}

echo -e "\nRun aiml_chat_test tests:"

# request_url_get "http://0.0.0.0:$port/add_expense?userid=dennyledger&expense=37,超大杯星巴克焦糖玛奇朵" && \
# request_url_get "http://0.0.0.0:$port/view_history?userid=dennyledger" && \
# request_url_get "http://0.0.0.0:$port/add_expense?userid=dennyledger&expense=37,超大杯星巴克焦糖玛奇朵" && \

# server_test
local_test

echo -e "\nDone"

## File : test.sh ends