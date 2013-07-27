# -*- coding: utf-8 -*-
##-------------------------------------------------------------------
## @copyright 2013
## File : weixin_unittest.py
## Author : filebat <markfilebat@126.com>
## Description :
## --
## Created : <2013-04-11 00:00:00>
## Updated: Time-stamp: <2013-06-02 20:45:53>
##-------------------------------------------------------------------
import unittest
import sys
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
	reload(sys)
	sys.setdefaultencoding(default_encoding)

from expense import Expense
from data import add_expense, view_history, search_record, delete_last_record
from mylogging import consoleHandler, logging
consoleHandler.setLevel(logging.WARNING)
# consoleHandler.setLevel(logging.INFO)

UNITTEST_USERID = "unittest"
class WeixinTestCase(unittest.TestCase):
	def setUp(self):
		self.userid = UNITTEST_USERID
	
	def tearDown(self):
		i = 1

	def testSearchRecord(self):
		self._assert_search_record("星巴克", "星巴克", False)
		self._assert_search_record("联通", "搜索出的最近记录", False)
		self._assert_search_record("吃饭", "搜索出的最近记录", False)
		self._assert_search_record("咖啡", "搜索出的最近记录", False)
		self._assert_search_record("26", "搜索出的最近记录", False)
		self._assert_search_record("2013-04", "搜索出的最近记录", False)

	def testAddExpense1(self):
		self._assert_add_expense("30 永和大王", "消费30元", False)
		self._assert_add_expense("26日 37 星巴克大杯焦糖玛奇朵", "消费37元", False)
		self._assert_add_expense("26 37 星巴克大杯焦糖玛奇朵", "消费37元", False)
		self._assert_add_expense("37 26 星巴克大杯焦糖玛奇朵", "消费37元", False)
		self._assert_add_expense("25星巴克咖啡", "消费25元", False)
		self._assert_add_expense("100 帮伟智充手机,13427579369", "数码家电", False)
		self._assert_add_expense("17 丰裕吃饭", "早午晚餐", False)
		self._assert_add_expense("101 味千拉面,同事中午聚餐", "消费101元", False)
		self._assert_add_expense("83 威宁路青年餐厅", "消费83元", False)
		self._assert_add_expense("56 本周早饭,每次按8元计", "消费56元", False)
		self._assert_add_expense("17 招商卡在田林路被呑了，打车回去", "消费17元", False)
		self._assert_add_expense("23 subway吃饭", "早午晚餐", False)
		self._assert_add_expense("16.5 23 subway吃饭", "消费16.5元", False)
		self._assert_add_expense("96.5 联通手机充值", "消费96.5元", False)
		self._assert_add_expense("25 早上打车到公司来加班", "消费25元", False)
		self._assert_add_expense("25 ", "再写详细点吧", False)
		self._assert_add_expense("abc ", "记账的格式", False)
		self._assert_add_expense(" abc ", "记账的格式", False)
		self._assert_add_expense("味千拉面 25。 ", "味千拉面", False)
		self._assert_add_expense("37打麻将输", "休闲玩乐", False)
		self._assert_add_expense("23 东方既白小鸡蘑菇饭", "早午晚餐", False)
		self._assert_add_expense("34必胜客下午茶", "消费34元", False)
		self._assert_add_expense("106纸 兴趣爱好", "休闲玩乐", False)
		self._assert_add_expense("25 中山公园家有好面,黄鱼面 ", "家有好面", False)
		self._assert_add_expense("23 subway吃饭", "早午晚餐", False)
		self._assert_add_expense("对不对呀?", "问题", False)
		self._assert_add_expense("37 超大杯星巴克焦糖玛奇朵 23 21.5", "一条", False)

	def testAddExpense2(self):
		self._assert_add_expense("3。5 烧饼", "消费3.5元", False)
		self._assert_add_expense("10 圣女果", "零食水果", False)
		self._assert_add_expense("100 裤子", "衣服裤子", False)
		self._assert_add_expense("40 樱桃", "零食水果", False)
		self._assert_add_expense("100	今天给别人冲话费", "网络通信", False)
		self._assert_add_expense("288 波波乐高玩具", "休闲玩乐", False)
		self._assert_add_expense("2000.8 收入", "赚了2000.8元", False)
		self._assert_add_expense("22 88 ", "消费记录无实质信息", False)
		self._assert_add_expense("2 公共汽车票", "公共交通", False)
		self._assert_add_expense("12 苦瓜炒蛋烧饼栗子", "早午晚餐", False)
		self._assert_add_expense("32.2 振鼎鸡", "早午晚餐", False)
		self._assert_add_expense("30 牛津面", "早午晚餐", False)
		self._assert_add_expense("63 披萨", "早午晚餐", False)
		self._assert_add_expense("30 日本料理", "早午晚餐", False)
		self._assert_add_expense("30 烧鸭饭", "早午晚餐", False)
		self._assert_add_expense("30 西北菜", "早午晚餐", False)
		self._assert_add_expense("收入", "收入", False)
		self._assert_add_expense("前天 20 吃饭", "20元", False)
		self._assert_add_expense("昨天 20 吃饭", "20元", False)
		# self._assert_add_expense("25 测试 ", "多加一些信息", False)

	def testDeleteLastRecord(self):
		msg = delete_last_record(self.userid)
		## print msg
		self.assertNotEqual(msg, "")

	def _assert_add_expense(self, original_content, part_result_content, print_content = False):
		content = add_expense(self.userid, original_content)
		if print_content is True:
			print content
		self.assertNotEqual(content.find(part_result_content), -1)

	def _assert_search_record(self, search_content, part_result_content, print_content = False):
		content = search_record(self.userid, search_content)
		if print_content is True:
			print content
		self.assertNotEqual(content.find(part_result_content), -1)
	
def suite():
	suite = unittest.TestSuite()
	suite.addTest(WeixinTestCase("testAddExpense1"))
	suite.addTest(WeixinTestCase("testAddExpense2"))
	suite.addTest(WeixinTestCase("testSearchRecord"))
	suite.addTest(WeixinTestCase("testDeleteLastRecord"))
	return suite

if __name__ == "__main__":
	Expense.delete_obj_by_id(UNITTEST_USERID, "")
	unittest.TextTestRunner().run(suite())
## File : weixin_unittest.py
