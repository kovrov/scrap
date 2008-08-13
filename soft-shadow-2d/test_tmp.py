import math
import pyglet
from pyglet.gl import *

class Point:
	def __init__(self, x=0., y=0.):
		self.x = x
		self.y = y
	def __imul__(self, val):
		self.x *= val; self.y *= val; return self
	def __mul__(self, val):
		return Point(self.x * val, self.y * val)
	def __sub__(self, other):
		return Point(self.x - other.x, self.y - other.y)
	def __add__(self, other):
		return Point(self.x + other.x, self.y + other.y)
	def cross(self, other):  # cross product
		return self.x * other.y - self.y * other.x
	def dot(self, other):  # dot product
		return self.x * other.x + self.y * other.y
	def normalise(self):
		length = self.length()
		if length != 0.:
			self *= (1. / length)
		return self
	def length(self):  # length of vector
		return math.sqrt(self.x * self.x + self.y * self.y)
	def angle(self, other):  # angle to other vector
		return math.atan2(self.cross(other), self.dot(other))  # angle between segments
	def __iter__(self):
		return iter((self.x, self.y))
	def __eq__(self, other):
		return self.x == other.x and self.y == other.y
	def __ne__(self, other):
		return self.x != other.x or self.y != other.y
	def __repr__(self):
		return "(%g,%g)" % (self.x, self.y)

def draw_circle(position, radius, color=(1.,1.,1.)):
		segments = 32
		increment = math.pi * 2 / segments
		radius = radius
		x, y = position
		glColor3f(*color)
		glBegin(GL_LINE_STRIP)
		for i in xrange(segments + 1):
			glVertex2f(radius*math.cos(i*increment)+x, radius*math.sin(i*increment)+y)
		glEnd()

def debug_point(point, msg):
	x, y = point
	glBegin(GL_POINTS)
	glVertex2f(*point)
	glEnd()
	pyglet.text.Label(msg, x=int(x), y=int(y)).draw()

def debug_line(src, dst, msg):
	glBegin(GL_LINE_STRIP)
	glVertex2f(*src)
	glVertex2f(*dst)
	glEnd()
	#pyglet.text.Label(msg, x=int(point.x), y=int(point.y)).draw()

win = pyglet.window.Window(resizable=True)

@win.event
def on_resize(width, height):
	glViewport(0, 0, width, height)
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	glOrtho(width/-2, width/2, height/-2, height/2, -1, 1)
	glMatrixMode(GL_MODELVIEW)
	return True

@win.event
def on_draw():
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

	src = Point(50., -200.) # blue
	dst = Point(-520, 210.) # green
	#direction = dst - src

	glBegin(GL_LINES)
	glColor3f(0,0,1) # blue
	glVertex2f(0,0)
	glVertex2f(*src)
	glColor3f(0,1,0) # green
	glVertex2f(0,0)
	glVertex2f(*dst)
	#glColor3f(1,1,1)
	#glVertex2f(0,0)
	#glVertex2f(*direction)
	glEnd()

	#cos = src.normalise().dot(dst.normalise())
	#print math.degrees(math.acos(cos))
	#sine = src.normalise().cross(dst.normalise())
	#print "sine", sine
	#print "angle", math.degrees(math.asin(sine))

	light_radius = 50
	light = Point(10,0)
	point = Point(150,0)
	lenght = 140
	draw_circle(point, lenght, (0.3,0.3,0.3))
	debug_point(light, "test")
	#p2 = point - light / 2
	d = light - point
	p2 = Point(point.x + (d.x * a/length), point.y + (d.y * a/length))

	x = p2.x +- h ( light.y - point.y ) / lenght
	y = p2.y -+ h ( light.x - point.x ) / lenght
	debug_point((x,y), "ok?")



pyglet.app.run()
