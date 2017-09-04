#coding:utf-8
import core.baseHandler

class helpcenterHandler(core.baseHandler.BaseHandler):
    # 定义get方法
    def get(self):
        print 'request: get helpcenter.html'
    	# get current staus of login
    	account = self.get_secure_cookie("account")
    	# 如果未登录,重置cookies['account']为'$None$'
    	if account == None or account == '$None$':
    		account = '$None$'
    		self.set_secure_cookie("account",account)
        self.render("html/helpcenter.html",
            title="帮助中心",
            alert="$None$",
            account=account)
    # 定义post方法
    def post(self):
        pass
class helpHandler(core.baseHandler.BaseHandler):
    def get(self):
        print 'request; get help.html'
        self.render("html/help.html")
