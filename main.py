# lib import
import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.options
import os.path
import torndb
import re
from tornado.options import define, options

# project core code import
from core.indexHandler import indexHandler
from core.taskHandler import *
from core.timeguildHandler import timeguildHandler,userinfoHandler
from core.loginHandler import loginHandler,logoutHandler,signUpHandler
from core.alertHandler import alertHandler
from core.helpcenterHandler import helpcenterHandler,helpHandler
from core.rootHandler import rootloginHandler,rootHandler,rootlogoutHandler
# sql connect infomation
define("port", default = 9999, help = "http connect port", type = int)
define("mysql_password", default = "6997", help = "password of mysql")

class Application(tornado.web.Application):
	def __init__(self):
		handler = [
			# index.html
			(r"/", indexHandler),
			# alert infomation in index.html
			(r"/alert\$(\w+)\$(\w+)", alertHandler),
			# login.html
			(r"/login", loginHandler),
			# signup.html
			(r"/signup", signUpHandler),
			# logout to current html
			(r"/logout", logoutHandler),
			# tasklist.html
			(r"/tasklist",tasklistHandler),
			# taskinfo.html
			(r"/taskinfo",taskinfoHandler),
			# publishtask.html
			(r"/taskpublish", taskpublishHandler),
			# timeguild.html
			(r"/timeguild",timeguildHandler),
			# fixinfo.html
			(r"/userinfofix",userinfoHandler),
			# redirect to /timeguild
			(r"/taskattend",attendtaskHandler),
			# redirect to /timeguild
			(r"/taskquit",quittaskHandler),
			# redirect to /timeguild
			(r"/taskfinish",finishtaskHandler),
			# redirect to /timeguild
			(r"/taskcredit",credittaskHandler),
			# redirect to /timeguild
			(r"/taskcancel",canceltaskHandler),
			# helpcenter.html
			(r"/helpcenter",helpcenterHandler),
			# help.html
			(r"/helpcenter/help",helpHandler),
			# rootlogin.html
			(r"/rootlogin",rootloginHandler),
			# rootlogin.html
			(r"/rootlogout",rootlogoutHandler),
			# root
			(r"/root",rootHandler),
			# pass a task
			(r"/judgepasstask",judgepasstaskHandler),
			# not pass a task
			(r"/judgenotpasstask",judgenotpasstaskHandler),


		]
		settings = dict(
			template_path = os.path.join(os.path.dirname(__file__), "template"),
			static_path=os.path.join(os.path.dirname(__file__), "static"),
			xsrf_cookies = False,
			cookie_secret = "Pz0YYHXpTTWuHJd4pLyFMXO/lgiy2UYTu7cj09uJgtI=",
			login_url = "/",
		)
		super(Application, self).__init__(handler, **settings)

		# connect with mysql
		self.db = torndb.Connection(
			host = "127.0.0.1:3306", database = "mydb",
			user = "root", password = options.mysql_password)

'''
	main
'''
def main():
	tornado.options.parse_command_line()
	http_server = tornado.httpserver.HTTPServer(Application())
	http_server.listen(options.port)
	tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
	main()
