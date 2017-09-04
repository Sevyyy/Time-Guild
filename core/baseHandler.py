import tornado

class BaseHandler(tornado.web.RequestHandler):
	@property
	def db(self):
		return self.application.db

	def get_current_user(self):
		# 
		# useful for authentication
		# but i still don't know exactly how and why
		# the tornado document ask me to do that :-)
		# 
		user_role = self.get_secure_cookie("role")
		user_id   = self.get_secure_cookie("id")
		if not user_id or not user_role:
			return None
		query = ("select * from %s where id = %s" % (user_role, user_id))
		# print '\n\n' + query + '\n\n\n'
		return self.db.get(query)

	def id2name(self, which, Id):
		query = ""
		if which == 'classroom':
			query = "select location from classroom where id = %s" % Id
		else:
			query = "select name from %s where id = %s" % (which, Id)
		result = self.db.get(query).itervalues.next()
		if result:
			return result.itervalues.next()
		else:
			return None

	def name2id(self, which, name):
		query = ""
		if which == 'classroom':
			query = "select id from classroom where location = '%s'" % name
		else:
			query = "select id from %s where name = '%s'" % (which, name)
		result = self.db.get(query)
		if result:
			return result['id']
		else:
			return None 

	def conflict(self, lessonId, classroom, week, start, end):
		classroomId = self.name2id('classroom', classroom)
		query = "select * from lesson_classroom where classroom = %s" % classroomId
		print query
		result = self.db.query(query)
		if result:
			if isinstance(result, dict):
				result = [result]
			# print 'conflict : result : '
			# print result
			for i in result:
				if i['lesson'] == lessonId:
					continue
				if i['week'] == week:
					if (start <= i['start'] <= end) or (i['start'] <= start <= i['end']):
						return True
		return False