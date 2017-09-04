#coding:utf-8
import core.baseHandler
from core.sqlHandler import *

class timeguildHandler(core.baseHandler.BaseHandler):
	def get(self):
		print 'request: get timeguild.html'
		myAccount = self.get_secure_cookie("account")
		role = self.get_secure_cookie("role")
		#select the info of published task
		table = 'Task'
		keys = ['*']
		conditions = {'publisher':myAccount}
		query = get_s_sql(table=table, keys=keys, conditions=conditions)
		publishedTask = self.db.query(query)
		publishedNum = len(publishedTask)
		#get attender
		for each in publishedTask:
			tid = each["ID"]
			query = ("select individual_account from Attend where Task_ID = %s" % tid)
			ret = self.db.get(query)
			if ret is None:
				each['attender'] = ""
			else:
				each['attender'] = ret['individual_account']

		#select the info of attended task
		query = ("select t.* "
				"from Task as t, Attend as a "
				"where a.Individual_account = %s and t.ID = a.Task_ID" % myAccount)
		attendedTask = self.db.query(query)
		attendedNum = len(attendedTask)
		#preprocess the description column
		for each in attendedTask:
			if len(each["description"]) > 50:
				each["description"] = each["description"][0:50]+"..."
		for each in publishedTask:
			if len(each["description"]) > 50:
				each["description"] = each["description"][0:50]+"..."
		#select the info of this account
		table = role
		keys = ['*']
		conditions = {'account':myAccount}
		query = get_s_sql(table=table, keys=keys, conditions=conditions)
		info = self.db.get(query)
		#render the html
		self.render("html/timeguild.html",
					title="时间公会",
					taskpublish = publishedTask,
					publishnum = publishedNum,
					taskattend = attendedTask,
					attendnum = attendedNum,
					info = info,
					account = myAccount,
					role = role,
					alert="$None$")


class userinfoHandler(core.baseHandler.BaseHandler):
	def post(self):
		print 'post individual info'
		# TODO : update info
		myAccount = self.get_secure_cookie("account")
		query = ("update Individual set name = '%s', birthday = '%s', "
				"email = '%s', password = '%s' where account = %s" % (
					self.get_argument("name"),
					self.get_argument("birthday"),
					self.get_argument("email"),
					self.get_argument("newpassword"),
					myAccount))
		print 'query : ' + query
		self.db.execute(query)
		self.redirect("/timeguild")
