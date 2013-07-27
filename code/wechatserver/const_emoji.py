# -*- coding: utf-8 -*-
#!/usr/bin/python
##-------------------------------------------------------------------
## @copyright 2013 ShopEx Network Technology Co,.Ltd
## File : const_emoji.py
## Author : filebat <markfilebat@126.com>
## Description :
## --
## Created : <2013-05-01>
## Updated: Time-stamp: <2013-06-08 10:44:14>
##-------------------------------------------------------------------
__author__ = 'denny/liki'

from mylogging import log
import config
################### emoji ######################################
# http://www.emoji-cheat-sheet.com
# TODO: Currently manually maintain below dictionary

brand_emoji_dict = {

}

category_emoji_dict = {
	"精神生活":":open_book:",
	"日常支出":":green_book:",
	"日常生活":":house_building:", 
	"日常用品":":house_building:", 
	"个人爱好":":majiang:",
	"网上购物":":happy_person:",
	"早午晚餐":":ramen:",
	"咖啡饮料":":coffee:",
	"零食水果":":red_apple:",
	"香烟酒水":":smoking:",
	"衣服裤子":":womans_clothes:",
	"鞋帽包包":":handbag:",
	"首饰饰品":":ring:",
	"数码家电":":camera:",
	"休闲玩乐":":performing_arts",
	"运动健身":":basketball:",
	"旅游度假":":palm_tree:",
	"宠物":":dog:",
	"书报杂志":":books:",
	"公共交通":":bus:",
	"打车":":taxi:",
	"私车费用":":oncoming_automobile:",
	"美发美容":":nail_care:",
	"医疗保健":":hospital:",
	"母婴用品":":baby_bottle:",
	"房租物业":":house:",
	"水电煤":":electric_plug:",
	"公交卡":":oncoming_bus:",
	"充值卡":":credit_card:",
	"培训进修":":musical_score:",
	"网络通信":":telephone_receiver:",
	"人情送礼":":gift:",
	"收入":":moneybag:",
	"固定支出":":litter:",
	"其他":":memo:",
	"其他花销":":memo:",
}

emoji_encoding_dict={
	":happy_person:":u"\U0001f646",
	":majiang:":u"\U0001f004",
	":green_book:":u"\U0001f4d7",
	":litter:":u"\U0001f6ae",
	":open_book:":u"\U0001f4d6",
	":house_building:":u"\U0001f3e0",
	":bus:":u"\U0001f68c",
	":memo:":u"\U0001f4dd",
	":ramen:":u"\U0001f35c",
	":taxi:":u"\U0001f695",
	":gift:":u"\U0001f381",
	":coffee:":u"\U00002615",
	":red_apple:":u"\U0001f34f",
	":smoking:":u"\U0001f377",
	":womans_clothes:":u"\U0001f457",
	":handbag:":u"\U0001f45c",
	":ring:":u"\U0001f48d",
	":camera:":u"\U0001f4f1",
	":palm_tree:":u"\U0001f334",
	":performing_arts":u"\U0001f3ad",
	":basketball:":u"\U000026bd",
	":dog:":u"\U0001f436",
	":books:":u"\U0001f349",
	":oncoming_automobile:":u"\U0001f698",
	":nail_care:":u"\U0001f485",
	":hospital:":u"\U0001f48a",
	":baby_bottle:":u"\U0001f37c",
	":house:":u"\U0001f3e0",
	":electric_plug:":u"\U0001f50c",
	":oncoming_bus:":u"\U0001f68d",
	":credit_card:":u"\U0001f4b3",
	":musical_score:":u"\U0001f3bc",
	":telephone_receiver:":u"\U0001f4de",
	":moneybag:":u"\U0001f4b0",
}

################### COMMON FUNCTION #############################
def get_emoji(key, type="category"):
	if type == "brand":
		mapping_dict = brand_emoji_dict
	else:
		mapping_dict = category_emoji_dict

	if mapping_dict.has_key(key) is False:
		return ""

	emoji_name = mapping_dict[key]
	if emoji_encoding_dict.has_key(emoji_name) is False:
		log.error("get_emoji('%s', '%s') fail: emoji_encoding_dict doesn't have key of '%s'" \
				  % (key, type, emoji_name))
		return ""

	return emoji_encoding_dict[emoji_name]

def get_emoji_html_escape(key, type="category"):
	key = key.encode('utf-8')
	if type == "brand":
		mapping_dict = brand_emoji_dict
	else:
		mapping_dict = category_emoji_dict

	if mapping_dict.has_key(key) is False:
		return ""

	emoji_name = mapping_dict[key]

	if emoji_encoding_dict.has_key(emoji_name) is False:
		log.error("get_emoji('%s', '%s') fail: emoji_encoding_dict doesn't have key of '%s'" \
				  % (key, type, emoji_name))
		unicode_name = config.DEFAULT_EMOJI
	else:
		unicode_name = emoji_encoding_dict[emoji_name]	

	if emoji_name == ":coffee:":
		ret = "&#x2615;"
	else:
		unicode_str = "%s" % repr(unicode_name)
		ret = "&#x%s;" % unicode_str[7:-1]
	return ret

################################################################
## File : const_emoji.py
