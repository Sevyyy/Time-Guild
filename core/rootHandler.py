#coding:utf-8
import core.baseHandler
from core.sqlHandler import *

class rootloginHandler(core.baseHandler.BaseHandler):
	def get(self):
		print 'request: get rootlogin.html'
		self.render("html/rootlogin.html",title="管理员登录",alert="$None$")
	def post(self):
		print 'request: post root login information'
		root = self.get_argument("account")
		password = self.get_argument("password")
		query = ("select * from Administrator where account = '%s'" % (root))
		print 'query : ' + query
		temp = self.db.get(query)
		if not temp:
			self.redirect("/alert$rootlogin$missid")
		else:
			if password != temp.password:
				self.redirect("/alert$rootlogin$incorrectpassword")
			else:
				self.set_secure_cookie("root", str(temp.account))
				self.set_secure_cookie("name", str(temp.name))
				self.redirect("/root")



class rootHandler(core.baseHandler.BaseHandler):
	def get(self):
		print 'request: get root.html'
		root = self.get_secure_cookie("root")
		if root is None:
			self.redirect("/alert$rootlogin$missid")
			return
		name = self.get_secure_cookie("name")
		# TODO: get task infomation from DB for task.html
		'''
		query = "select id, name, description, credit, publisher, address, startTime, endTime from Task where state = 0"
		'''
		table = 'Task'
		keys = ['id', 'name', 'description', 'credit', 'publisher', 'address', 'startTime', 'endTime']
		conditions = {'state':0}
		query = get_s_sql(table=table,keys=keys,conditions=conditions)
		# 数据库操作
		task = self.db.query(query)


		self.render("html/root.html",root=root,name=name,task=task)
	def post(self):
		pass

class rootlogoutHandler(core.baseHandler.BaseHandler):
	def get(self):
		print 'request: root log out'
		self.clear_cookie("root")
		self.clear_cookie("name")
		self.redirect("/rootlogin")
