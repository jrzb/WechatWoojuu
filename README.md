
# Woojuu WeChat Public Platform

## Linode Deployment Guide
---

### uwsgi deployment

uwsgi should be installed in its virtualenv, in this case is _wechat.woojuu.cc_ with `pip install uwsgi` command to isolate the cgi container. __DON'T__ install it with `apt-get install`.

To run `uwsgi`, you have to firstly workon its virtualenv:
	
	workon wechat.woojuu.cc
	
For testing, just load up the configuration xml:

	uwsgi -x uwsgi_config.xml

For deployment:

	uwsgi -x /home/wwwroot/wechat.woojuu.cc/uwsgi_config.xml -M -t 30 -A 1 -p 1 -d /var/log/uwsgi.log --vhost


## Installation
---

Flask==0.9
Jinja2==2.6
Werkzeug==0.8.3
elementtree==1.2.7-20070827-preview
hashlib==20081119
mmseg==1.3.0
pymmseg==1.2.0
wsgiref==0.1.2


## WeChat Related
---

### 微信表情代码
[http://www.54575.com/blog/2013/04/11/微信自带表情符号的默认代码/](http://www.54575.com/blog/2013/04/11/微信自带表情符号的默认代码/)

### 分类Emoji
Full list of Emoji and their code: [http://grumdrig.com/emoji-list/](http://grumdrig.com/emoji-list/) (view it under Safari)

| Emoji | Code | Category Name | Code in Woojuu |
:-------|------|---------------|----------------|
| &#x1f35c; |  `&#x1f35c;` | 早午晚餐 | :ramen: |
| &#x2615; |  `&#x2615;` | 咖啡饮料 | :ramen: |
| &#x1f377; |  `&#x1f349;` | 香烟酒水 | :ramen: |
| &#x1f457; |  `&#x1f457;` | 衣服裤子 | :ramen: |
| &#x1f460; |  `&#x1f460;` | 鞋帽包包 | :ramen: |
| &#x1f48d; |  `&#x1f48d;` | 首饰饰品 | :ramen: |
| &#x1f4f1; |  `&#x1f4f1;` | 数码家电 | :ramen: |
| &#x1f3ad; |  `&#x1f3ad;` | 休闲玩乐 | :ramen: |
| &#x26bd; |  `&#x26bd;` | 运动健身 | :ramen: |
| &#x1f334; |  `&#x1f334;` | 旅游度假 | :ramen: |
| &#x1f436; |  `&#x1f436;` | 宠物 | :ramen: |
| &#x1f4da; |  `&#x1f349;` | 书报杂志 | :ramen: |
| &#x1f349; |  `&#x1f349;` | 日常用品 | :ramen: |
| &#x1f68c; |  `&#x1f68c;` | 公共交通 | :ramen: |
| &#x1f695; |  `&#x1f695;` | 打车 | :ramen: |
| &#x1f485; |  `&#x1f485;` | 美发美容 | :ramen: |
| &#x1f48a; |  `&#x1f48a;` | 医疗保健 | :ramen: |
| &#x1f37c; |  `&#x1f37c;` | 母婴用品 | :ramen: |
| &#x1f3e0; |  `&#x1f3e0;` | 房租物业 | :ramen: |
| &#x1f4de; |  `&#x1f4de;` | 网络通信 | :ramen: |
| &#x1f381; |  `&#x1f381;` | 人情送礼 | :ramen: |
| &#x1f4b0; |  `&#x1f4b0;` | 收入 | :ramen: |


	# "固定支出":"",
	"水电煤":":electric_plug:",
	"公交卡":":oncoming_bus:",
	"充值卡":":credit_card:",
	"培训进修":":musical_score:"



### TODO
- 根据用户使用增大数据库。有分词和映射到分类两个部分。
- 开始使用1-7天每日推送图文信息，引导用户一步步使用培养习惯
- 7天以后每天推送最近7天图表。是否能每个用户看到图文信息不同？还是只能通过链接跳转的方式？
- 分词和映射数据库使用MySQL

## HTTP API
---
### Interactive with weixin
`GET api`

Talk with weixin
---

### barcode
`GET barcode`

Return two dimension barcode of weixin
---

### expense summary
`GET summary`

| Name	  |Mandatory | Summary																	  |
:-----------|------|------------------------------------------------------------------------------|
| userid  |Y  | userid of weixin |
| categories | Y | category list(separated by semicolon) to be caculated. If the value is "", all cateogries are sum up. |
| fromdate | Y | start date with format of "2013-04-29 12:08:03" |
| enddate | Y | end date with format of "2013-04-29 12:08:03" |

Return total expense till now.

_Sample:_

	[
		{
			"name": "衣服饰品",
			"amount": 14365
		},
		{
			"name": "早午晚餐",
			"amount": 2500
		},
	]

---

### list expense
`GET list_expense`

| Name	  |Mandatory | Summary																	  |
:-----------|------|------------------------------------------------------------------------------|
| userid  |Y  | userid of weixin |
| fromdate | Y | start date with format of "2013-04-29 12:08:03" |
| enddate | Y | end date with format of "2013-04-29 12:08:03" |

Return expense details filtered by time range

_Sample:_

	[
		{
			"id":"123",
			"category": "衣服饰品",
			"date":" 2013/4/28",
			"amount": 120,
			"notes": "买衣服",
			"emoji": "&#x1f457"
		},
		{
			"id":"124",
			"category": "在外吃饭",
			"date":" 2013/4/29",
			"amount": 52,
			"notes": "麦当劳吃饭",
			"emoji": "&#x1f35c"
		}
	]

---

### summary daily
`GET summary_daily`

| Name	  |Mandatory | Summary																	  |
:-----------|------|------------------------------------------------------------------------------|
| userid  |Y  | userid of weixin |
| fromdate | Y | start date with format of "2013-04-29 12:08:03" |
| enddate | Y | end date with format of "2013-04-29 12:08:03" |

list topn categories, summed up by amount

_Sample:_

	[
		{
			"date": "2013/04/29",
			"totalamount": 520
		}
		{
			"date": "2013/04/29",
			"totalamount": 0
		}
	]
---

### category daily
`GET category_daily`

| Name	  |Mandatory | Summary																	  |
:-----------|------|------------------------------------------------------------------------------|
| userid  |Y  | userid of weixin |
| fromdate | Y | start date with format of "2013-04-29 12:08:03" |
| enddate | Y | end date with format of "2013-04-29 12:08:03" |

list categories, summed up by amount

_Sample:_

	[
		{
			"category": "衣服饰品",
			"date": "2013/04/29",
			"totalamount": 520
		}
		{
			"category": "早午晚餐",
			"date": "2013/04/29",
			"totalamount": 352
		}
	]
---

### topn category
`GET topn_category`

| Name	  |Mandatory | Summary																	  |
:-----------|------|------------------------------------------------------------------------------|
| userid  |Y  | userid of weixin |
| fromdate | Y | start date with format of "2013-04-29 12:08:03" |
| enddate | Y | end date with format of "2013-04-29 12:08:03" |
| limit | Y | How many records shall be returned |

list topn categories, summed up by amount

_Sample:_

	[
		{
			"category": "衣服饰品",
			"totalamount": 520
		}
		{
			"category": "早午晚餐",
			"totalamount": 352
		}
	]
---

### Delete expense
`POST delete_expense`

| Name	  |Mandatory | Summary																	  |
:-----------|------|------------------------------------------------------------------------------|
| userid  |Y  | userid of weixin |
| expenseid | Y | expenseid to specify which record shall be deleted |

Delete exepense by expenseid

_Sample:_

	{
		"errorcode":"200",
		"message":"删除成功"
	}

---

### Add expense
`POST add_expense`

| Name	  |Mandatory | Summary																	  |
:-----------|------|------------------------------------------------------------------------------|
| userid  |Y  | userid of weixin |
| notes | Y | User's input for this expense record, which shall parsed into structed record |

Add an exepense

_Sample:_

	{
		"errorcode":"200",
		"message":"消费101元。类别：早午晚餐。备注：101 味千拉面,同事中午聚餐"
	}


## Installation
---

git clone https://github.com/andelf/PyAIML.git
cd PyAIML && python ./setup.py install

/etc/profile:
export WECHAT_HOME="/Users/mac/backup/essential/Dropbox/private_data/code/wechat.woojuu.cc"