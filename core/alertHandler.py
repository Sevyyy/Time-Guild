#coding:utf-8
import core.baseHandler

class alertHandler(core.baseHandler.BaseHandler):
	def get(self, doc, message):
		print "request: get alert.html"
		doc_dict={
		'login':'html/login.html',
		'signup':'html/signup.html',
		'rootlogin':'html/rootlogin.html'
		}
		title_dict={
		'login':'登录',
		'signup':'注册',
		'rootlogin':'管理员登录'
		}
		message_dict={
		'missid':'账号不存在!',
		'incorrectpassword':'用户名或密码错误!'
		}
		self.render(doc_dict[doc], title=title_dict[doc],account="$None$",alert = message_dict[message])
