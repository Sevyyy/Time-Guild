#coding:utf-8
import core.baseHandler
from core.sqlHandler import *

# 处理主页请求
class indexHandler(core.baseHandler.BaseHandler):
    # TODO: 处理get请求
    def get(self):
        print "request: get index.html"

        # TODO: get task infomation from DB for index
        '''
        query = ("select t.id, t.name, t.credit,t.address, t.startTime, t.endTime "
        "from Task as t limit 8")
        '''

        table = 'Task'
        keys = ['id','name','credit','address','startTime','endTime']
        conditions = {'state':'1'}
        query = get_s_sql(table = table,keys = keys,conditions=conditions)
        query = sql_add_limit(query=query,limit='limit 8')
        # 数据库操作
        print 'query : ' + query

        # need to add other information
        task = self.db.query(query)

        # need to be repair, random select pic for index.html
        for t in task:
            t['picid'] = "static/img/task/defaultPic_"+str(t['id']%24)+".jpg"
            t['id'] = str(t['id'])
        # print type(task)
        # 获取用户是否登录
        account = self.get_secure_cookie("account")

        # 如果未登录,重置cookies['account']为'$None$'
        if account == None or account == '$None$':
            account = '$None$'
            self.set_secure_cookie("account",account)

        # 渲染html
        # self.render("index.html",title="主页" ,task = task,account=account,alert="$None$")
        self.render("index.html",title="主页" ,task = task,account=account,alert="$None$")

    # TODO:处理post请求
    def post(self):
        pass
