
# GET / goes to the homepage showing all blog entries with the newest on top.
# GET /entry/<id> shows a single blog entry with this id.
# GET /create shows a formular for creating blog entries
# POST /create creates a new blog entry 


import os.path
import wsgiref.headers, wsgiref.util
import genshi.template
import models



loader = genshi.template.TemplateLoader(
		os.path.join(os.path.dirname(__file__), 'templates'),
	    auto_reload=True)



class App:
	def __init__(self, environ, start_response):
		self.environ = environ
		self.start = start_response
		self.appname = wsgiref.util.shift_path_info(environ)

	def __iter__(self):
		ctrl = BlogCtrl(self.environ)
		if not self.appname:
			status = '200 ok'
			res = ctrl.index()
		elif (self.appname == 'entry'):
			status = '200 ok'
			res = ctrl.entry()
		elif (self.appname == 'create'):
			status = '200 ok'
			res = ctrl.create()
		else:
			status = '404 not found'
			res = "%s not found" % self.appname
		response_headers = [('Content-type','text/html')]
		self.start(status, response_headers)
		yield res



class BlogCtrl(object):
	def __init__(self, environ):
		self.environ = environ

	def index(self):
		tmpl = loader.load('index.html')
		return tmpl.generate(entries=models.BlogEntry.query).render('html', doctype='html')

	def entry(self):
		id = self.environ['PATH_INFO'].strip('/').split('/')[0]
		tmpl = loader.load('entry.html')
		return tmpl.generate(entry=models.BlogEntry.query.filter_by(id=id).first()).render('html', doctype='html')

	def create(self):
		if self.environ['REQUEST_METHOD'] == 'POST':
			form = get_post_data(self.environ)
			entry = models.BlogEntry()
			entry.title = form['title'].value
			entry.content = form['content'].value
			entry.save()
			models.session.commit()
			return "/"
		else:
			tmpl = loader.load('create.html')
			return tmpl.generate().render('html', doctype='html')



import cgi

def get_post_data(environ):
    return cgi.FieldStorage(
       fp                = environ['wsgi.input'],
       environ           = environ,
       keep_blank_values = 1)
