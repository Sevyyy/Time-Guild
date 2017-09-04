#coding:utf-8
import core.baseHandler
import time
from core.sqlHandler import *

# 处理任务列表页请求
class tasklistHandler(core.baseHandler.BaseHandler):
	# TODO: 处理get请求
	def get(self):
		print "request: get task.html"

		# TODO: get task infomation from DB for task.html
		'''
		query = "select id, name, description, credit, publisher, address, startTime, endTime from Task where state = 0"
		'''
		table = 'Task'
		keys = ['id', 'name', 'description', 'credit', 'publisher', 'address', 'startTime', 'endTime']
		conditions = {'state':1}
		query = get_s_sql(table=table,keys=keys,conditions=conditions)
		# 数据库操作
		info = self.db.query(query)
		# need to be repair, random select pic for index.html
		for t in info:
			t['picid'] = "static/img/task/defaultPic_"+str(t['id']%24)+".jpg"
			t['id'] = str(t['id'])
		# get current staus of login
		account = self.get_secure_cookie("account")
		# 如果未登录,重置cookies['account']为'$None$'
		if account == None or account == '$None$':
			account = '$None$'
			self.set_secure_cookie("account",account)

		# 渲染html
		self.render("html/tasklist.html",title="任务栏", info = info, account=account,alert="$None$")

	# 处理post请求
	def post(self):
		pass

# 处理任务详情页请求
class taskinfoHandler(core.baseHandler.BaseHandler):
	# 处理get请求
	def get(self):
		taskid = self.get_argument("taskid")

		print 'request: get taskinfo.html when taskid =' + taskid
		'''
		query = ("select * from Task where ID = %s" % taskid)
		'''
		table = 'Task'
		keys = ['*']
		conditions = {'id':taskid}

		query = get_s_sql(table=table,keys=keys,conditions=conditions)

		# 数据库操作
		info = self.db.get(query)

		# 获取图片地址(伪)
		info['picid'] = "static/img/task/defaultPic_"+str(int(taskid)%24)+".jpg"

		# 获取用户是否登录
		account = self.get_secure_cookie("account")
		# 如果未登录,重置cookies['account']为'$None$'
		if account == None or account == '$None$':
			account = '$None$'
			self.set_secure_cookie("account",account)
		# 渲染html
		self.render("html/taskinfo.html",
			title="任务详情",
			alert="$None$",
			info = info,
			taskid = taskid,
			account= account
		)
	# 处理post请求
	def post(self):
		pass
# 生成任务
class attendtaskHandler(core.baseHandler.BaseHandler):
	# TODO: 处理get请求
	def post(self):
		taskid = self.get_argument("taskid")
		myAccount = self.get_secure_cookie("account")
		#get today as a string
		today = time.strftime('%Y-%m-%d',time.localtime(time.time()))
		#update Task(set state from 1 to 2)
		table = 'Task'
		value = {'state':2}
		conditions = {'ID':taskid}
		query = get_u_sql(table=table, value=value, conditions=conditions)
		self.db.execute(query)
		#insert into Attend
		table = 'Attend'
		today = time.strftime('%Y-%m-%d',time.localtime(time.time()))
		dict = {'individual_account':myAccount, 'task_ID':taskid, 'attendTime':today}
		query = get_i_sql(table=table,dict=dict)
		self.db.execute(query)
		#jump to timeguild
		self.redirect("/timeguild")

	# 处理post请求
	def get(self):
		pass

# 任务完成
class finishtaskHandler(core.baseHandler.BaseHandler):
	# TODO: 处理get请求
	def post(self):
		taskid = self.get_argument("taskid")
		#update Task(set state from 2 to 3)
		table = 'Task'
		value = {'state':3}
		conditions = {'ID':taskid}
		query = get_u_sql(table=table, value=value, conditions=conditions)
		self.db.execute(query)
		#jump to timeguild
		self.redirect("/timeguild")

	# 处理post请求
	def get(self):
		pass
# 放弃任务
class quittaskHandler(core.baseHandler.BaseHandler):
	# TODO: 处理get请求
	def post(self):
		taskid = self.get_argument("taskid")
		myAccount = self.get_secure_cookie("account")
		#update Task(set state from 2 to 1)
		table = 'Task'
		value = {'state':1}
		conditions = {'ID':taskid}
		query = get_u_sql(table=table, value=value, conditions=conditions)
		self.db.execute(query)
		#delete from Attend
		table = 'Attend'
		conditions = {'individual_account':myAccount, 'task_ID':taskid}
		query = get_d_sql(table=table, conditions=conditions)
		self.db.execute(query)
		#jump to timeguild
		self.redirect("/timeguild")

	# 处理post请求
	def get(self):
		pass
# 任务审核通过
class judgepasstaskHandler(core.baseHandler.BaseHandler):
	# TODO:处理post请求
	def post(self):
		taskid = self.get_argument("taskid")
		#update Task(set state from 0 to 1)
		table = 'Task'
		value = {'state':1}
		conditions = {'ID':taskid}
		query = get_u_sql(table=table, value=value, conditions=conditions)
		self.db.execute(query)
		#jump to root
		self.redirect("/root")
# 任务审核通过
class judgepasstaskHandler(core.baseHandler.BaseHandler):
	# TODO:处理post请求
	def post(self):
		print 'request: post from root.html to pass a task'
		taskid = self.get_argument("taskid")
		#update Task(set state from 0 to 1)
		table = 'Task'
		value = {'state':1}
		conditions = {'ID':taskid}
		query = get_u_sql(table=table, value=value, conditions=conditions)
		self.db.execute(query)
		#jump to root
		self.redirect("/root")
# 任务审核未通过
class judgenotpasstaskHandler(core.baseHandler.BaseHandler):
	# TODO:处理post请求
	def post(self):
		print 'request: post from root.html to not pass a task'
		taskid = self.get_argument("taskid")
		#update Task(set state from 0 to 1)
		table = 'Task'
		value = {'state':-1}
		conditions = {'ID':taskid}
		query = get_u_sql(table=table, value=value, conditions=conditions)
		self.db.execute(query)
		#jump to root
		self.redirect("/root")
# 支付报酬
class credittaskHandler(core.baseHandler.BaseHandler):
	# TODO: 处理get请求
	def post(self):
		taskid = self.get_argument("taskid")
		myAccount = self.get_secure_cookie("account")
		#update Task(set state from 3 to 4)
		table = 'Task'
		value = {'state':4}
		conditions = {'ID':taskid}
		query = get_u_sql(table=table, value=value, conditions=conditions)
		self.db.execute(query)
		"""
		#delete from Attend
		table = 'Attend'
		conditions = {'individual_account':myAccount, 'task_ID':taskid}
		query = get_d_sql(table=table, conditions=conditions)
		self.db.execute(query)
		"""
		#update attender's money
		query = ("update Attend, Individual, Task "
				"set Individual.money = Individual.money + Task.credit "
				"where Task.ID = %s and Individual.account = Attend.individual_account and Attend.Task_ID = %s"
				% (taskid, taskid))
		self.db.execute(query)
		#update publisher's money
		query = ("update Individual, Task "
			"set Individual.money = Individual.money-Task.credit "
			"where Task.ID = %s and Individual.account = %s"
			% (taskid, myAccount))
		self.db.execute(query)
		#jump to timeguild
		self.redirect("/timeguild")

	# 处理post请求
	def get(self):
		pass
# 删除任务
class canceltaskHandler(core.baseHandler.BaseHandler):
	# TODO: 处理get请求
	def post(self):
		taskid = self.get_argument("taskid")
		myAccount = self.get_secure_cookie("account")
		#delete Task
		table = 'Task'
		conditions = {'ID':taskid}
		query = get_d_sql(table=table, conditions=conditions)
		self.db.execute(query)
		#jump to timeguild
		self.redirect("/timeguild")

	# 处理post请求
	def get(self):
		pass
# 发布任务
class taskpublishHandler(core.baseHandler.BaseHandler):
	def post(self):

		query = ("insert into Task (publisher, name, credit, startTime, "
			"endTime, leader, phone, address, description, process, "
			"requirement, state) values (%s, '%s', %s, '%s', '%s', '%s', %s, "
			"'%s', '%s', '%s', '%s', %s)" % (
				self.get_secure_cookie("account"),
				self.get_argument("taskname"),
				self.get_argument("credit"),
				self.get_argument("startTime"),
				self.get_argument("endTime"),
				self.get_argument("leader"),
				self.get_argument("phone"),
				self.get_argument("address"),
				self.get_argument("description"),
				self.get_argument("process"),
				self.get_argument("requirement"),
				0))

		self.db.execute(query)
		self.redirect("/timeguild")
