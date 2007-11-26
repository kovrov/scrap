import wsgiref.headers, wsgiref.util


class App:
	def __init__(self, environ, start_response):
		self.environ = environ
		self.start = start_response
		self.appname = wsgiref.util.shift_path_info(environ)

	def __iter__(self):
		ctrl = BlogCtrl(wsgiref.util.request_uri(self.environ))
		if not self.appname:
			status = '200 ok'
			res = ctrl.index()
		elif (self.appname == 'entry'):
			status = '200 ok'
			res = ctrl.entry()
		elif (self.appname == 'create'):
			status = '200 ok'
			res = ctrl.entry()
		else:
			status = '404 not found'
			res = "%s not found" % self.appname
		response_headers = [('Content-type','text/html')]
		self.start(status, response_headers)
		yield res




import models

class BlogCtrl(object):
	def __init__(self, data):
		self.data = data

	def index(self):
		models.BlogEntry.query
		return 'index'

	def entry(self):
		return self.data

	def create(self):
		return self.data

"""
* GET / goes to the homepage showing all blog entries with the newest on top.
* GET /entry/<id> shows a single blog entry with this id.
* GET /create shows a formular for creating blog entries
* POST /create creates a new blog entry 
"""



import genshi
import models

def index(environ, start_response):
    rows = models.entry_table.select().execute()
    return genshi.render(start_response, 'list.html', locals())

def member_get(environ, start_response):
    id = environ['selector.vars']['id']
    row = models.entry_table.select(models.entry_table.c.id==id).execute().fetchone()
    return genshi.render(start_response, 'entry.html', locals())
