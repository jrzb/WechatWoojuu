# Woojuu WeChat Public Platform -- HTTP API
=========
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

