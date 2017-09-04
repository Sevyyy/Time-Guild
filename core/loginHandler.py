#coding:utf-8
import core.baseHandler
from core.sqlHandler import *

class loginHandler(core.baseHandler.BaseHandler):
	def get(self):
		print 'request: get index.html after login'
		self.render("html/login.html",title="登录",account="$None$",alert="$None$")

	def post(self):
		print 'request: post login infomation'
		input_role = self.get_argument("role")
		input_account = self.get_argument("account")
		input_password = self.get_argument("password")

		# debug
		# print 'role : ' + input_role
		# print 'id : ' + input_account
		# print 'password : ' + input_password

		query = ("select * from %s where account = '%s'" % (input_role, input_account))
		print 'query : ' + query
		temp = self.db.get(query)
		if not temp:
			self.redirect("/alert$login$missid")
		else:
			if input_password != temp.password:
				self.redirect("/alert$login$incorrectpassword")
			else:
				self.set_secure_cookie("role", input_role)
				self.set_secure_cookie("account", str(temp.account))
				self.redirect("/")


class logoutHandler(core.baseHandler.BaseHandler):
	def get(self):
		print 'logout'
		self.clear_cookie("role")
		self.clear_cookie("account")
		self.redirect("/")


class signUpHandler(core.baseHandler.BaseHandler):
	def get(self):
		print 'get sign up'
		self.render("html/signup.html",title="注册",account="$None$",alert="$None$")

	def post(self):
		print 'post sign up'
		role = self.get_argument('role')
		# TODO : insert into db
		if role == "Individual":
			query = ("insert into %s (account,password,name,birthday,ID,email, money)"
				" values ('%s', '%s', '%s', '%s', '%s', '%s', %d)" % (
					self.get_argument("role"),
					self.get_argument("account"),
					self.get_argument("password"),
					self.get_argument("i_name"),
					self.get_argument("birthday"),
					self.get_argument("ID"),
					self.get_argument("email"),
					10))
		else:
			query = ("insert into %s (account,password,name,leader,address,establishedTime,email,money)"
				" values ('%s', '%s','%s', '%s', '%s', '%s','%s', %d)" % (
					self.get_argument("role"),
					self.get_argument("account"),
					self.get_argument("password"),
					self.get_argument("o_name"),
					self.get_argument("leader"),
					self.get_argument("address"),
					self.get_argument("establishedTime"),
					self.get_argument("email"),
					10))
		print 'query : ' + query
		self.db.execute(query)
		self.set_secure_cookie("account", str(self.get_argument("account")))
		self.set_secure_cookie("role", str(self.get_argument("role")))
		self.redirect("/")
