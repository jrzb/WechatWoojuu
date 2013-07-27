# -*- coding: utf-8 -*-
#!/usr/bin/python
##-------------------------------------------------------------------
## @copyright 2013
## File : chat.py
## Author : filebat <markfilebat@126.com>
## Description :
## --
## Created : <2013-04-11 00:00:00>
## Updated: Time-stamp: <2013-07-14 08:20:59>
##-------------------------------------------------------------------
from expense import Expense
import const_message as MSG
import config
import util
import random
from aiml_chat import chat_aiml

CHAT_REPLY_DICT = {
	# "attach_extra_msg":{
	# 	# 系统箴言型
	# 	"7":"\n小莴说: 还有啥钱花了，却没记的呢？/:?",
	# 	"8":"\n小莴说: 这位爷，您最近吃饭呀，打车呀之类的，都不花钱的吗？/:?",
	# 	"11":"\n小莴说: 记账，记下生活中的欢乐时光。",
	# 	"12":"\n小莴说: 记账最关键的是记录现金的支出，其它的都不那么重要。",
	# 	"13":"\n小莴说: 每当你记账时，告诉自己正在做一件伟大的事情。",
	# 	"19":"\n小莴说: 记账让我们不盲目地节省，也不盲目地投资。",

	# 	# 网友箴言型
	# 	"5":"\n小莴说: 我只要一记账，各种不必要消费就会大大的减少，每个月钱都会多出来。",
	# 	"9":"\n小莴说: 对我而言，记账未必是为了控制花钱，而是排除那种不知道钱花到哪里的恐惧感。。",
	# 	"10":"\n小莴说: 记账绝对是一件好事情，说明一个人有很好的自律性，有规划，有远见，同时有的放矢。",
	# 	"6":"\n小莴说: 我是个懒人，平时不管买什么，都把发票塞兜里。无聊时，一并录入。",
	# 	"15":"\n小莴说: 记账难坚持。一旦变成习惯了就坚持下来了，然后已经变成'不记账不舒服'了..",
	# 	"18":"\n小莴说: 有时花的时候没感觉，回顾一下还比较惊人，这样下个月会在某些方面注意一点。",
	# 	"26":"\n小莴说: 哦耶！我已经坚持记了10天了，fighting~~",
	# 	"29":"\n小莴说: 我感觉这个莴苣还行。自动识别消费类别，以前老麻烦了。",

	# 	# 中性论点
	# 	"20":"\n小莴说: 每日一记，发现钱真太不经花了！",
	# 	"17":"\n小莴说: 我也不想记账，主要是不记账的话,真的无法做到有计划性的花钱",
	# 	"23":"\n小莴说: 做事情缺乏毅力和坚持，如何才能把提升自己落到实处。坚持记账，能对这有帮助不？",
	# 	"24":"\n小莴说: 不要相信一些貌似正确的合理的支出配比，你花的钱，你觉得值得，才是最重要的。",
	# 	"25":"\n小莴说: 让所有的开销都刷信用卡，消费记录就都有了。不过，刷信用卡不疼呀。纠结！",
	# 	"27":"\n小莴说: 呃，我记账的目的是，提醒自己不要乱花钱。身边朋友，我就不知道了。",

	# 	# 反面论点：起引导性和平衡作用
	# 	"14":"\n小莴说: 记账是否会让一个人形成斤斤计较的坏脾气，影响交友等人际关系？",
	# 	"28":"\n小莴说: 特佩服能坚持记账的人！碰到了假期，花钱如流水；闲下来就想休息，哪还理账呀。",

	# 	# 功能介绍性
	# 	"1":"\n小莴说: 有问题，就给我们发语音吧。/:8*",
	# 	"2":"\n小莴说: 向朋友们推荐一下俺吧，输入：二维码 /:handclap",
	# 	"30":"\n小莴说: 向朋友们推荐一下俺吧，输入：二维码 /:handclap",
	# 	"31":"\n小莴说: 向朋友们推荐一下俺吧，输入：二维码 /:handclap",
	# 	"3":"\n小莴说: 搜索记录是可以的，试下输入这个呗：搜索",
	# 	"32":"\n小莴说: 搜索记录是可以的，试下输入这个呗：搜索",
	# 	"33":"\n小莴说: 搜索记录是可以的，试下输入这个呗：搜索",
	# 	"4":"\n小莴说: 记录是可以删除的，功能藏得很深的，你找得不/:@>",
	# 	"34":"\n小莴说: 记录是可以删除的，功能藏得很深的，你找得不/:@>",

	# 	"16":"\n小莴说: 俺们也支持语音输入的哟/::d",
	# 	"21":"\n小莴说: 俺们也支持语音输入的哟/::d",
	# 	"22":"\n小莴说: 俺们也支持语音输入的哟/::d",
	# 	"35":"\n小莴说: 俺们也支持语音输入的哟/::d",
	# 	"36":"",
	# 	"37":"",
	# 	"38":"",
	# 	"39":"",
	# 	"40":"",
	# 	"41":"",
	# 	"42":"",
	# 	"43":"",
	# 	"44":"",
	# },

	"?":{
		"1":"带问号结尾的提问性质的输入, 会被当成问题转发给我们小二的。/::d",
		"2":"小的听不懂呀，我家掌柜听得懂的。这位爷，您的问题我已经帮您转达给我家掌柜了。/::d",
		"3":"有问题，就给我们发语音吧。/:8*",
	},

	"multiple_record":{
		"1":"稍等稍等，咱们一条一条的来哦。/::d",
		"2":"小的记忆力太差，一次只能记一条哟。/::d",
	},

	"voice_input":{
		# "1":"消费记录，暂时还不能语音输入哦。/::'(\n对小莴有啥建议和抱怨，直接微信语音我们吧/:@) ",
		"1":"语音已经收到，客官请稍等。。。新功能刚开张，可能需要久一点时间哟。/:@)",
		"2":"得令，小的去后堂解析一下这个语音。稍等稍等。/:@)",
		"3":"语音已经收到，需要一些时间处理下。有啥建议或抱怨，也给小莴发语音吧。/:@)",
	},

	"image_input":{
		"1":"消费记录，暂时还不能上传图片哦。/::'(\n对小莴有啥建议和抱怨，直接微信语音我们吧/:@) ",
	},

	"pure_alpha":{
		"1":"咋内容都没汉字的勒。加点汉字本土著才看得懂中文耶。/:@) \n",
	},

	"multiple_number":{
		"1":"看不出消费金额哦。我们还是一次只记一条消息吧。",
	},

	"empty_notes":{
		"1":"看样子，这位爷只是在测试俺们哦。/::+消费记录无实质信息，再写详细点吧。/:@) \n",
	},
	"我想":{
		"1":"有想法就去追寻它。/::d",
		"2":"想要你就大声说出来。/::d",
	},
	"我要":{
		"1":"有想法就去追寻它。/::d",
		"2":"想要你就大声说出来。/::d",
	},
	"哈哈":{
		"1":"别笑，小的正在工作，帮您记账呢。/::P",
	},
	"呵呵":{
		"1":"别敷衍我哦，人家会伤心的。/::'(",
	},
	"嘿嘿":{
		"1":"嘻嘻，你有啥开心事呀，说来看看哦。/::D",
	},
	"男朋友":{
		"1":"大人的事，我还不懂耶/::$。",
	},
	"名字":{
		"1":"我的名字叫莴苣账本，你呢？/::+",
	},
	# TODO: define alias
	# "早上好":{
	#	 "1":"你也早上好哦。/::d",
	# },
	# "中午好":{
	#	 "1":"你也下午好哦。/::d",
	# },
	# "下午好":{
	#	 "1":"你也下午好哦。/::d",
	# },
	# "晚上好":{
	#	 "1":"你也晚上好哦。/::d",
	# },
}

# REPLY_COMMON_DICT = {
# 		"1":"消费记录里应该有金额个啵。/::d",
# 		"2":"咋没看出来消费记录的金额勒。/::d",
# 		"3":"这个...小的还不大认识... 小莴要多学学，变得更聪明些。/::d",
# 		"4":"要不试着说点简单的？小莴和你聊天时，会越变越聪明的。/::d",
# 		"5":"此句竟有些不解。/::d 但若是换个格式，譬如“128 宫廷御膳房佳肴”。倒也不负恩泽~",
# 		"6":"小莴还不太懂耶。有啥建议和困惑，你直接向我发问或发语音就好了。我回答不了，会转达给我主人的/::d",
# 		"7":"真心听不懂耶，是我太笨了吗？/::d",
# 		"8":"Hi，小的是新来的，现在正专心做好记账功能，成为你的好助手。/::d",
# }

def attach_detected_extra_msg(wechat_user, content, expense):
	if shall_caculate_category_msg(expense) is True:
		category_possiblity = 70
		random_int = random.randint(1, 100)
		if random_int > category_possiblity:
			ret = content + reply_chat(expense, wechat_user)
		else:
			category_msg = generate_expense_msg(expense.userid, expense.category)
			ret = content + category_msg
	else:
		ret = content + reply_chat(expense, wechat_user)

	return ret

def attach_undetected_extra_msg(wechat_user, expense, content):
	possibility = 70
	random_int = random.randint(1, 100)
	if random_int > possibility:
		ret = content + reply_chat(expense, wechat_user)
	else:
		ret = content + generate_general_comparision(expense.userid)
	return ret

def pic_random(keyword):
	possible_reply_dict = CHAT_REPLY_DICT[keyword]
	return pic_reply(possible_reply_dict)

def response_fail(expense, fail_type):
	return MSG.REPLY_EXPENSE_FAILED % pic_random(fail_type)

def generate_general_comparision(userid):
	# TODO better performance
	count_threshold = 10
	amount_threshold = 1000
	sql_format = "select left(date, 7) as date, sum(amount) as sum, count(1) as count, avg(amount) as avg" + \
				 " from expenses where userid='%s' " + \
				 "and amount < %d group by left(date, 7) order by left(date, 7) desc limit 2;"
	sql = sql_format % (userid, amount_threshold)
	out = Expense.query_sql(sql)
	if len(out) == 0:
		sum_this = 0
		count_this = 0
	else:
		sum_this = float(out[0][1])
		count_this = int(out[0][2])

	# if count_this > count_threshold:
	# 		msg = "本月共花了%s元。按这速度，本月会花掉%s元。" % \
	# 	  (util.format_float_str(sum_this), \
	# 	   util.format_float_str(util.predict_amount(sum_this)))
	# else:
	msg = "本月共花了%s元。" % \
	  (util.format_float_str(sum_this))

	if len(out) >= 2:
		sum_last = float(out[1][1])
		count_last = int(out[1][2])
		msg = "%s而上月共花了%s元。" % (msg, util.format_float_str(sum_last))
	return msg

def generate_expense_msg(userid, category):
	(user_count, user_amount, avg_count, avg_amount) \
			= Expense.get_expense_msg(userid, category)
	avg_count = avg_count * 3 # TODO: hack here
	category_msg = "你最近30天在'%s'上，一共消费%s元。" % \
				(category, util.format_float_str(user_amount * user_count))

	return category_msg

###################### functions #############################
def reply_chat(expense, wechat_user):
	sentence = expense.notes
	ret = chat_aiml.respond_msg(sentence)
	if ret == "":
		nickname = wechat_user.get_attr("nickname")
		if nickname is not None:
			chat_aiml.respond_msg("MY NAME IS " + nickname)
		else:
			chat_aiml.respond_msg("MY NAME IS " + "")

		gender = wechat_user.get_attr("gender")
		if gender is not None:
			chat_aiml.respond_msg("MY GENDER IS " + gender)
		else:
			chat_aiml.respond_msg("MY GENDER IS " + "")

		ret = chat_aiml.respond_msg("ASK USER A FINANCE QUESTION")

	return ret

	# response = pic_reply(REPLY_COMMON_DICT)
	# if token_list is None:
	# 	token_list = util.word_split(sentence, True)

	# for text, start, end in token_list:
	# 	if CHAT_REPLY_DICT.has_key(text):
	# 		possible_reply_dict = CHAT_REPLY_DICT[text]
	# 		response = pic_reply(possible_reply_dict)
	# 		break
	# return response

# pic a reply from a list of candidates
def pic_reply(possible_reply_dict):
	possible_rep_count = len(possible_reply_dict)
	index = random.randint(1, possible_rep_count)
	return possible_reply_dict[str(index)]

def is_comment_meaningless(comment):
	comment = util.wash_sentence(comment)
	comment = comment.replace("哈哈", " ")
	comment = comment.replace("test", " ")
	comment = comment.replace("测试", " ")
	comment = comment.replace(".", "")
	comment = comment.replace(" ", "")

	return comment == "" or comment.isdigit()

def is_comment_pure_alpha(comment):
	comment = util.wash_sentence(comment)
	return comment.isalpha()

def shall_caculate_category_msg(expense):
	if expense.category in ('incoming', '其他类别', '收入', '其他'):
		return False

	# if expense.category in ('日常支出', '精神生活', '日常生活', \
	# 						'零食水果', '书报杂志', '网络通信', \
	# 						'公共交通', '打车', '私车费用', \
	# 						'其他花销', '固定支出', '房租物业', \
	# 						'水电煤', '公交卡', '充值卡', '其他', \
	# 						'incoming', '其他类别'
	# 						):
	# 	return False

	# amount_filter = 100
	# if expense.category == '咖啡饮料':
	# 	amount_filter = 20

	# if expense.category == '早午晚餐':
	# 	amount_filter = 15

	# if expense.amount < amount_filter:
	# 	return False

	return True

################################################################
## File : chat.py