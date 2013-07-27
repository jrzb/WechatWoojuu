# -*- coding: utf-8 -*-
##-------------------------------------------------------------------
## @copyright 2013
## File : const_message.py
## Author : liki
## Description :
## --
## Created : <2013-04-11 00:00:00>
## Updated: Time-stamp: <2013-07-14 08:15:40>
##-------------------------------------------------------------------
__author__ = 'denny/liki'

CODE_MANUAL = u"1"
CODE_MANUAL2 = u"l"
CODE_MANUAL3 = u"１"
CODE_MORE = u"2"
CODE_MORE2 = u"２"
CODE_MORE_MORE = u"3"
CODE_MORE_MORE2 = u"３"
CODE_HISTORY = u"h"
CODE_QRCODE = u"二维码"
CODE_SEARCH = u"搜索"
CODE_SEARCH2 = u"s"
CODE_SEARCH3 = u"S"
CODE_DELETE = u"删除"
CODE_MUTE = u"安静"

REPLY_WELCOME = \
u"""Hi，欢迎使用莴苣账本微信助手！微信记账，同样只要三秒！马上来试试吧 /:sun

回复「1」查看使用说明
回复「h」查看历史记录

莴苣账本iPhone应用：
http://woojuu.cc

使用中有问题或建议，请回复，莴苣账本有问必答 /:,@-D
"""

REPLY_MANUAL = \
u"""输入你的支出或收入金额，附加简单说明我就可以记下了。比如“37 午饭 味千拉面”。

回复「1」查看使用说明
回复「h」查看历史记录
回复「s」搜索记录
回复「2」查看更多说明
"""

REPLY_MUTE = \
u"""小莴：好嘀，收到。我们会很安静的/:,@-D"""

REPLY_MANUAL_MORE = \
u"""回复「1」查看使用说明

回复「?」提问和反馈
回复「删除」删除上一条
回复「安静」少推些消息
回复「二维码」推荐莴苣
回复「3」查看全部说明
"""

REPLY_MANUAL_MORE_MORE = \
u"""回复「1」查看使用说明

记收入: '200 收入 工资'
按日期搜索: 's 2013-05'
按日期搜索: 's 05-24'
按日期搜索: 's 24'
记历史: '昨天 37 午饭 味千拉面'
iphone客户端: http://www.woojuu.cc
"""

REPLAY_HISTORY = \
u"""最近消费
------
今日消费：%s元
本周消费：%s元
本月消费：%s元
当前余额:  %s元

点击查看明细：
"""

REPLY_EXPENSE_ADDED = \
u"""记好了: 在%s上消费%s元。

"""

REPLY_EXPENSE_ADDED_WITH_CATEGORY = \
u"""记好了: 在%s上消费%s元。

"""

REPLY_EXPENSE_ADDED_WITH_BRANDING = \
u"""记好了: 在%s上消费%s元。

"""

REPLY_EXPENSE_ADDED_SIMPLE = \
u"""记好了: %s月%s号，消费%s元。备注: %s。%s

"""

REPLAY_SEARCH = \
u"""搜索出的最近记录 '%s':
------
%s

查看更多详细信息：
http://h.woojuu.cc/u/%s
"""

# TODO: Keyword matching
REPLY_FUN = u""

REPLY_EXPENSE_FAILED = \
u"""%s记账的格式“35 肯德基早餐”。"""

REPLY_OTHER = \
u"""Hi，我是新来的，现在正专心做好记账功能，成为你的好助手。/:@) 不如马上来试试？

回复「1」查看使用说明
"""